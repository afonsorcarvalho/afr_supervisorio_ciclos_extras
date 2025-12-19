"""Extensão do modelo de ciclos para incluir materiais"""
from odoo import models, fields, api


class SupervisorioCiclosExtend(models.Model):
    """Extensão do modelo de ciclos para incluir relação com materiais"""
    
    _inherit = 'afr.supervisorio.ciclos'
    
    # Relação One2many com as linhas de materiais
    material_lines_ids = fields.One2many(
        'afr.supervisorio.cycle.materials.lines',
        'ciclo_id',
        string='Materiais Esterilizados',
        help='Lista de materiais que foram esterilizados neste ciclo'
    )
    
    # Campo computed para contar materiais
    material_count = fields.Integer(
        string='Total de Materiais',
        compute='_compute_material_count',
        store=True
    )
    
    @api.depends('material_lines_ids')
    def _compute_material_count(self):
        """Calcula o total de linhas de materiais"""
        for record in self:
            record.material_count = len(record.material_lines_ids)
    
    def action_view_materials(self):
        """Abre a visão de materiais do ciclo"""
        self.ensure_one()
        return {
            'name': 'Materiais do Ciclo',
            'type': 'ir.actions.act_window',
            'res_model': 'afr.supervisorio.cycle.materials.lines',
            'view_mode': 'tree,form',
            'domain': [('ciclo_id', '=', self.id)],
            'context': {
                'default_ciclo_id': self.id,
                'search_default_active': 1,
            },
        }
    
    def action_print_laudo_wizard(self):
        """Abre o wizard de impressão do laudo"""
        self.ensure_one()
        return {
            'name': 'Gerar Laudo de Liberação',
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.print.laudo',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_ciclo_id': self.id,
                'active_id': self.id,
                'active_model': 'afr.supervisorio.ciclos',
            },
        }

