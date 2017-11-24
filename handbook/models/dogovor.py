# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from num2t4ru import *

class dogovor(models.Model):
    _name = 'tech_directory.dogovor'
    _inherit = ['mail.thread']
    _rec_name = 'date'
    _order= 'date'
    nubmer = fields.Char()
    own_company_id = fields.Many2one(comodel_name="tech_directory.own_company")
    own_company_id_type_os = fields.Boolean(readonly = "True",related='own_company_id.type_os')
    own_company_id_type_lab = fields.Boolean(readonly = "True",related='own_company_id.type_lab')
    type_selection = fields.Selection([("os","Organ po sertificacii"),("lab","laboratoria")])
    date = fields.Date(default=fields.Date.today)
    doc_package_id = fields.Many2one(
        comodel_name="tech_directory.doc_package",
        domain=[('type_komplekt', '=', 'dogovor')],
        string="doc_package_id")

    dop_prosrochka_int = fields.Selection([ ('d1', '1'),
                                            ('d2', '2'),
                                            ('d3', '3'),
                                            ('d4', '4'),
                                            ('d5', '5'),
                                            ('d6', '6'),
                                            ('d7', '7'),
                                            ('d8', '8'),
                                            ('d9', '9'),
                                            ('d10', '10'),
                                            ('d11', '11'),
                                            ('d12', '12'),
                                            ('d13', '13'),
                                            ('d14', '14'),
                                            ('d15', '15'),
                                            ('d16', '16'),
                                            ('d17', '17'),
                                            ('d18', '18'),
                                            ('d19', '19'),
                                            ('d20', '20'),
                                            ('d21', '21'),
                                            ('d22', '22'),
                                            ('d23', '23'),
                                            ('d24', '24'),
                                            ('d25', '25'),
                                            ('d26', '26'),
                                            ('d27', '27'),
                                            ('d28', '28'),
                                            ('d29', '29'),
                                            ('d30', '30')],default='d5')

    max_summ_zadolghosti_int = fields.Float(digits=(10,2),default= '20000')
    kolv_vo_doc_free_int = fields.Integer(default= '5')
    summ_avance_int = fields.Float(digits=(10,2),default= '3')

    @api.onchange("dop_prosrochka_int")
    def _summ_avance_in_onchange_field(self):
        male_units = ((u'день', u'дня', u'дней'), 'm')
        self.dop_prosrochka_char = num2text(self.dop_prosrochka_int, male_units)

    @api.onchange("summ_avance_int")
    def _summ_avance_in_onchange_field(self):
        int_units = ((u'рубль', u'рубля', u'рублей'), 'm')
        exp_units = ((u'копейка', u'копейки', u'копеек'), 'f')
        self.summ_avance_char= decimal2text(decimal.Decimal(self.summ_avance_int),int_units=int_units,exp_units=exp_units)

    @api.onchange("kolv_vo_doc_free_int")
    def _kolv_vo_doc_free_int_onchange_field(self):
        male_units = ((u'документ', u'документа', u'документов'), 'm')
        self.kolv_vo_doc_free_char = num2text(self.kolv_vo_doc_free_int, male_units)

    @api.onchange("max_summ_zadolghosti_int")
    def _max_summ_zadolghosti_int_onchange_field(self):
        int_units = ((u'рубль', u'рубля', u'рублей'), 'm')
        exp_units = ((u'копейка', u'копейки', u'копеек'), 'f')
        self.max_summ_zadolghosti_char= decimal2text(decimal.Decimal(self.max_summ_zadolghosti_int),int_units=int_units,exp_units=exp_units)

    dop_prosrochka_char = fields.Char()
    max_summ_zadolghosti_char = fields.Char()
    kolv_vo_doc_free_char = fields.Char()
    summ_avance_char = fields.Char()

    doc_package_id_type_dogovora = fields.Selection(related='doc_package_id.type_dogovora')

    contractor_id = fields.Many2one('tech_directory.contractor')
    dop_dogovor_ids = fields.One2many('tech_directory.dop_dogovor','dogovor_id')

    active = fields.Boolean(default=True)
    state = fields.Selection([
    ('on_created', 'On created'),
    ('created', 'Created'),
    ],default='on_created')


    @api.one
    def on_created_progressbar(self):
        self.write({
            'state': 'on_created',
        })

    @api.one
    def created_progressbar(self):
        self.write({
    	'state': 'created'
        })
