# -*- coding: utf-8 -*-
"""
Controller para download público do laudo de liberação
"""
from typing import Any, List, Optional, cast

from odoo import http
from odoo.http import request, content_disposition
import hmac
import logging

_logger = logging.getLogger(__name__)


class LaudoLiberacaoController(http.Controller):
    """Controller para acesso público ao laudo de liberação via QR code"""

    def _parse_material_line_ids(self, raw_value: Any) -> Optional[List[int]]:
        """
        Converte o parâmetro `materials` (CSV) em lista de ints ordenada e sem duplicados.

        Ex.: "10,20,20" -> [10, 20]

        Returns:
            list[int] | None: lista válida ou None se inválido/vazio.
        """
        if not raw_value:
            return None
        try:
            parts = [p.strip() for p in str(raw_value).split(',') if p.strip()]
            ids = sorted({int(p) for p in parts})
            return ids or None
        except Exception:
            return None

    @http.route([
        '/laudo/liberacao/public/<int:ciclo_id>',
        '/laudo/liberacao/public/<int:ciclo_id>/',
        '/laudo/liberacao/public/<int:ciclo_id>/<path:token>',
        '/laudo/liberacao/public/<int:ciclo_id>/<path:token>/',
    ], type='http', auth='public', methods=['GET'])
    def download_laudo_publico(self, ciclo_id, token=None, **kwargs):
        """
        Rota pública para download do laudo de liberação
        
        Args:
            ciclo_id: ID do ciclo
            token: Token de autenticação (vindo de kwargs)
            
        Returns:
            Response: PDF do laudo ou erro 404
        """
        try:
            # Obtém o token (query string ou path)
            token = token or kwargs.get('token')
            if not token:
                _logger.warning(f"Token não fornecido para ciclo {ciclo_id}")
                return request.not_found()
            token = str(token)

            # Materiais permitidos (devem vir no QR code, para espelhar o filtro do wizard)
            # Aceitamos `materials` (novo) e `material_line_ids` (compatibilidade).
            materials_raw = kwargs.get('materials') or kwargs.get('material_line_ids')
            material_line_ids = self._parse_material_line_ids(materials_raw)
            if not material_line_ids:
                _logger.warning(f"Lista de materiais não fornecida/ inválida para ciclo {ciclo_id}")
                return request.not_found()
            
            # Ambiente público (auth='public'); usamos sudo apenas nos acessos específicos
            # Odoo é altamente dinâmico; usamos cast(Any) para evitar falsos-positivos do type checker.
            env = cast(Any, request.env)

            # Busca o ciclo
            ciclo = cast(Any, env['afr.supervisorio.ciclos'].sudo().browse(ciclo_id))
            if not ciclo.exists():
                _logger.warning(f"Ciclo {ciclo_id} não encontrado")
                return request.not_found()

            # Segurança: garante que TODOS os IDs pertencem ao ciclo (evita vazamento por tentativa de injeção).
            valid_ids = set(ciclo.material_lines_ids.ids)
            if any(mat_id not in valid_ids for mat_id in material_line_ids):
                _logger.warning(f"Materiais inválidos para ciclo {ciclo_id}: {material_line_ids}")
                return request.not_found()

            # Verifica se o token é válido (token assinado também com os materiais)
            expected_token = str(ciclo._get_laudo_public_token(material_line_ids=material_line_ids))
            if not hmac.compare_digest(expected_token, token):
                _logger.warning(f"Token inválido para ciclo {ciclo_id}")
                return request.not_found()
            
            # Busca o report action e renderiza o PDF usando a API correta
            report_action = env.ref('afr_supervisorio_ciclos_extras.report_laudo_liberacao_action')
            if not report_action:
                _logger.error("Report action não encontrado")
                return request.not_found()
            report_action = cast(Any, report_action).sudo()
            
            # IMPORTANTE: `_render_qweb_pdf` é método do model `ir.actions.report` e espera `report_ref` (string)
            # Se chamarmos direto no recordset, o primeiro argumento vira `report_ref` e quebra (vira list).
            report_service = cast(Any, env['ir.actions.report'].sudo())
            # Passa `data` com os materiais autorizados, para o report aplicar o mesmo filtro do wizard.
            pdf_result = report_service._render_qweb_pdf(
                report_action.report_name,
                [ciclo_id],
                data={'material_line_ids': material_line_ids},
            )
            pdf = cast(bytes, pdf_result[0])
            
            # Nome do arquivo
            filename = f'Laudo_Liberacao_{ciclo.name}.pdf'
            
            # Retorna o PDF
            return cast(Any, request).make_response(
                pdf,
                headers=[
                    ('Content-Type', 'application/pdf'),
                    ('Content-Disposition', content_disposition(filename))
                ]
            )
            
        except Exception as e:
            _logger.error(f"Erro ao gerar laudo público: {str(e)}", exc_info=True)
            return request.not_found()

