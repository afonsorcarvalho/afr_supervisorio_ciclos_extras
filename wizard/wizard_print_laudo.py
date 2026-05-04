"""Wizard para seleção de materiais para impressão do laudo e assinatura."""
from odoo import models, fields, api
from odoo.exceptions import UserError
import base64
import logging

_logger = logging.getLogger(__name__)


class WizardPrintLaudo(models.TransientModel):
    """Wizard para selecionar materiais e assinatura do laudo."""

    _name = 'wizard.print.laudo'
    _description = 'Wizard de Impressão do Laudo de Liberação'

    # --- Ciclo e materiais ---
    ciclo_id = fields.Many2one(
        'afr.supervisorio.ciclos',
        string='Ciclo',
        required=True,
        readonly=True,
    )
    material_line_ids = fields.Many2many(
        'afr.supervisorio.cycle.materials.lines',
        string='Materiais do Ciclo',
        domain="[('ciclo_id','=',ciclo_id)]",
        help='Selecione os materiais que deseja incluir no laudo',
    )
    material_count = fields.Integer(
        string='Materiais Selecionados',
        compute='_compute_material_count',
    )

    # --- Assinatura ---
    signature_type = fields.Selection(
        [
            ('auto', 'Automática (padrão da empresa)'),
            ('upload', 'Enviar imagem (PNG)'),
            ('draw', 'Assinar digitalmente (desenho)'),
        ],
        string='Tipo de assinatura',
        default='auto',
        required=True,
        help='Automática: usa a assinatura configurada na empresa. '
             'Enviar imagem: faça upload de um PNG. '
             'Assinar digitalmente: use o quadro de assinatura e depois envie a imagem.',
    )
    signature_image = fields.Binary(
        string='Imagem da assinatura',
        attachment=False,
        help='PNG da assinatura (upload ou gerado pelo quadro de assinatura).',
    )
    signer_name = fields.Char(
        string='Nome de quem assina',
        help='Nome do responsável pela garantia de qualidade (exibido no laudo).',
    )
    signer_title = fields.Char(
        string='Cargo / Função',
        default='Garantia de qualidade',
        help='Cargo ou função exibido no laudo (ex.: Garantia de qualidade, Responsável técnico).',
    )
    signature_date = fields.Date(
        string='Data da assinatura',
        default=fields.Date.context_today,
        required=True,
    )
    data_liberacao = fields.Date(
        string='Data de liberação',
        required=True,
        help='Data de liberação impressa no laudo. Default: data da assinatura do responsável pelo ciclo.',
    )
    data_emissao = fields.Date(
        string='Data de emissão do laudo',
        default=fields.Date.context_today,
        required=True,
        help='Data de emissão impressa no laudo.',
    )

    @api.depends('material_line_ids')
    def _compute_material_count(self):
        for wizard in self:
            wizard.material_count = len(wizard.material_line_ids)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        ciclo_id = self.env.context.get('active_id')
        if ciclo_id:
            res['ciclo_id'] = ciclo_id
            if 'data_liberacao' in fields_list and not res.get('data_liberacao'):
                ciclo = self.env['afr.supervisorio.ciclos'].browse(ciclo_id)
                sig_date = ciclo.signature_date
                if sig_date:
                    res['data_liberacao'] = fields.Date.to_date(sig_date)
                else:
                    res['data_liberacao'] = fields.Date.context_today(self)
        company = self.env.company
        if company:
            if 'signer_name' in fields_list and not res.get('signer_name'):
                res['signer_name'] = company.laudo_signer_name_default or ''
            if 'signer_title' in fields_list and not res.get('signer_title'):
                res['signer_title'] = company.laudo_signer_title_default or 'Garantia de qualidade'
        return res

    def _get_signature_data_for_report(self):
        """
        Monta o dicionário de dados de assinatura para passar ao relatório.
        Retorna base64 da imagem (ou None) e textos (nome, cargo, data).
        """
        self.ensure_one()
        signer_name = (self.signer_name or '').strip()
        signer_title = (self.signer_title or 'Garantia de qualidade').strip()
        signature_date = self.signature_date

        # Imagem: automática = company; upload/draw = wizard
        signature_image_b64 = None
        if self.signature_type == 'auto':
            img = self.env.company.laudo_signature_default
            if img:
                signature_image_b64 = base64.b64encode(img).decode('utf-8') if isinstance(img, bytes) else img
            if not signer_name and self.env.company.laudo_signer_name_default:
                signer_name = (self.env.company.laudo_signer_name_default or '').strip()
            if not signer_title and self.env.company.laudo_signer_title_default:
                signer_title = (self.env.company.laudo_signer_title_default or 'Garantia de qualidade').strip()
        elif self.signature_image:
            img = self.signature_image
            signature_image_b64 = base64.b64encode(img).decode('utf-8') if isinstance(img, bytes) else img

        return {
            'signature_type': self.signature_type,
            'signature_image_b64': signature_image_b64,
            'signer_name': signer_name,
            'signer_title': signer_title,
            'signature_date': signature_date,
            'data_emissao': self.data_emissao,
            'data_liberacao': self.data_liberacao,
        }

    def action_print_laudo(self):
        """Gera o laudo com os materiais selecionados e dados de assinatura."""
        self.ensure_one()
        if not self.material_line_ids:
            raise UserError('Selecione pelo menos um material para gerar o laudo!')

        material_ids = self.material_line_ids.ids
        report = self.env.ref('afr_supervisorio_ciclos_extras.report_laudo_liberacao_action')
        data = {
            'material_line_ids': material_ids,
            **self._get_signature_data_for_report(),
        }
        return report.report_action(self.ciclo_id.ids, data=data)
