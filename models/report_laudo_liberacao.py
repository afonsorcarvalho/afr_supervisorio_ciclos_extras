# -*- coding: utf-8 -*-
"""Modelo abstrato para processar dados do Laudo de Liberação"""
from odoo import models, api
import logging
import qrcode
from io import BytesIO
import base64

_logger = logging.getLogger(__name__)


class ReportLaudoLiberacao(models.AbstractModel):
    """
    Modelo abstrato para o relatório de Laudo de Liberação.
    
    Processa os dados antes de enviar para o template QWeb.
    """
    _name = 'report.afr_supervisorio_ciclos_extras.report_laudo_liberacao_template'
    _description = 'Relatório de Laudo de Liberação de Produtos'
    _table = 'report_laudo_liberacao'  # Nome curto para evitar erro de tabela muito longa (limite PostgreSQL: 63 caracteres)

    @api.model
    def _get_report_values(self, docids, data=None):
        """
        Retorna os valores para o template do relatório.
        
        Args:
            docids: Lista de IDs dos ciclos de esterilização
            data: Dicionário com material_line_ids (IDs dos materiais selecionados)
        
        Returns:
            dict: Dicionário com 'docs', 'data' e outros valores para o template
        """
        data = data or {}
        
        # Se docids estiver vazio, tenta pegar do contexto (active_ids)
        if not docids:
            active_ids = self.env.context.get('active_ids', [])
            if active_ids:
                docids = active_ids
        
        # Busca os ciclos
        ciclos = self.env['afr.supervisorio.ciclos'].browse(docids) if docids else self.env['afr.supervisorio.ciclos']
        
        # Busca os materiais selecionados (filtrados pelo wizard)
        # Se não houver material_line_ids no data, mostra todos os materiais dos ciclos
        material_line_ids = data.get('material_line_ids', [])
        if material_line_ids:
            # Filtro aplicado pelo wizard - usa apenas os materiais selecionados
            material_lines = self.env['afr.supervisorio.cycle.materials.lines'].browse(material_line_ids)
        else:
            # Sem filtro (rota pública) - mostra todos os materiais de todos os ciclos
            material_lines = self.env['afr.supervisorio.cycle.materials.lines']
            for ciclo in ciclos:
                material_lines |= ciclo.material_lines_ids
        
        # Gera QR code para cada ciclo
        qr_codes = {}
        for ciclo in ciclos:
            try:
                # Gera o QR code apontando para a versão pública EXATA deste laudo.
                # Para garantir que o público veja apenas os materiais selecionados no wizard,
                # incluímos a lista de `material_line_ids` na URL e ela também é assinada no token.
                selected_ids = material_lines.filtered(lambda l: l.ciclo_id.id == ciclo.id).ids
                if not selected_ids:
                    # Sem materiais (ou sem filtro). Não gera QR code para evitar link público ambíguo.
                    qr_codes[ciclo.id] = None
                    continue

                public_url = ciclo.get_laudo_public_url(material_line_ids=selected_ids)
                qr_buffer = BytesIO()
                qrcode.make(public_url.encode(), box_size=4).save(qr_buffer, optimise=True, format='PNG')
                img_str = base64.b64encode(qr_buffer.getvalue()).decode()
                qr_codes[ciclo.id] = img_str
            except Exception as e:
                _logger.error(f"Erro ao gerar QR code para ciclo {ciclo.id}: {str(e)}")
                qr_codes[ciclo.id] = None
        
        # Retorna valores para o template
        return {
            'doc_ids': docids,
            'doc_model': 'afr.supervisorio.ciclos',
            'docs': ciclos,  # ✅ Aqui que popula o 'docs' para o template!
            'data': data,    # ✅ Passa o data para o template também
            'material_lines_filtered': material_lines,  # ✅ Materiais já filtrados
            'qr_codes': qr_codes,  # ✅ QR codes para cada ciclo
        }

