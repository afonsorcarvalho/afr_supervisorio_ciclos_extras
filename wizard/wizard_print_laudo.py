"""Wizard para seleção de materiais para impressão do laudo"""
from odoo import models, fields, api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class WizardPrintLaudo(models.TransientModel):
    """Wizard para selecionar materiais a serem incluídos no laudo"""
    
    _name = 'wizard.print.laudo'
    _description = 'Wizard de Impressão do Laudo de Liberação'
    
    # Referência ao ciclo
    ciclo_id = fields.Many2one(
        'afr.supervisorio.ciclos',
        string='Ciclo',
        required=True,
        readonly=True
    )
    
    # Linhas de materiais disponíveis no ciclo
    material_line_ids = fields.Many2many(
        'afr.supervisorio.cycle.materials.lines',
        string='Materiais do Ciclo',
        help='Selecione os materiais que deseja incluir no laudo'
    )
    
    # Contador de materiais selecionados
    material_count = fields.Integer(
        string='Materiais Selecionados',
        compute='_compute_material_count'
    )
    
    @api.depends('material_line_ids')
    def _compute_material_count(self):
        """Calcula o número de materiais selecionados"""
        for wizard in self:
            wizard.material_count = len(wizard.material_line_ids)
    
    @api.model
    def default_get(self, fields_list):
        """Preenche valores padrão ao abrir o wizard"""
        res = super(WizardPrintLaudo, self).default_get(fields_list)
        
        # Obtém o ciclo do contexto
        ciclo_id = self.env.context.get('active_id')
        if ciclo_id:
            res['ciclo_id'] = ciclo_id
            # Não pré-seleciona materiais - usuário deve marcar manualmente
        
        return res
    
    def action_print_laudo(self):
        """Imprime o laudo com os materiais selecionados"""
        self.ensure_one()
        
        # Validação: pelo menos um material deve ser selecionado
        if not self.material_line_ids:
            raise UserError(
                'Selecione pelo menos um material para gerar o laudo!'
            )
        
        # DEBUG: Log detalhado
        material_ids = self.material_line_ids.ids
        _logger.info("="*80)
        _logger.info("WIZARD DEBUG - action_print_laudo")
        _logger.info(f"Ciclo existe? {bool(self.ciclo_id)}")
        _logger.info(f"Ciclo ID: {self.ciclo_id.id if self.ciclo_id else 'NENHUM'}")
        _logger.info(f"Ciclo Name: {self.ciclo_id.name if self.ciclo_id else 'NENHUM'}")
        _logger.info(f"Materiais selecionados (IDs): {material_ids}")
        _logger.info(f"Total de materiais: {len(self.material_line_ids)}")
        
        # CORREÇÃO: Passa o recordset diretamente, não lista de IDs
        _logger.info(f"DEBUG: Tipo de self.ciclo_id: {type(self.ciclo_id)}")
        _logger.info(f"DEBUG: self.ciclo_id.ids: {self.ciclo_id.ids}")
        
        report = self.env.ref('afr_supervisorio_ciclos_extras.report_laudo_liberacao_action')
        _logger.info(f"DEBUG: Report encontrado: {report.name}")
        _logger.info(f"DEBUG: Report model: {report.model}")
        
        # IMPORTANTE: Passa os IDs para o report_action
        # O AbstractModel _get_report_values vai receber e processar
        action = report.report_action(
            self.ciclo_id.ids,  # ✅ Passa a lista de IDs
            data={'material_line_ids': material_ids}
        )
        
        _logger.info(f"DEBUG: Action retornada: {action}")
        _logger.info(f"DEBUG: Action context: {action.get('context', {})}")
        _logger.info("="*80)
        
        return action
