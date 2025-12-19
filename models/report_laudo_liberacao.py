# -*- coding: utf-8 -*-
"""Modelo abstrato para processar dados do Laudo de Liberação"""
from odoo import models, api
import logging

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
        material_line_ids = data.get('material_line_ids', [])
        material_lines = self.env['afr.supervisorio.cycle.materials.lines'].browse(material_line_ids) if material_line_ids else self.env['afr.supervisorio.cycle.materials.lines']
        
        # Retorna valores para o template
        return {
            'doc_ids': docids,
            'doc_model': 'afr.supervisorio.ciclos',
            'docs': ciclos,  # ✅ Aqui que popula o 'docs' para o template!
            'data': data,    # ✅ Passa o data para o template também
            'material_lines_filtered': material_lines,  # ✅ Materiais já filtrados
        }

