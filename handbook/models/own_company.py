# -*- coding: utf-8 -*-

from odoo import models, fields, api
from rddata import *

class own_company(models.Model):
    _name = 'tech_directory.own_company'
    _rec_name = 'short_org_name'

    own_company_my_button_fill  = fields.Boolean()
    @api.multi
    @api.onchange("own_company_my_button_fill")
    def _onchange_field(self):
        d=rdfast()
        for re in self:
            if re.own_company_my_button_fill:
                re.inn= rdnums(11)
                re.kpp= rdnums(11)
                re.ogrn_ogrnip= rdnums(11)
                re.okpo= rdnums(12)
                re.okved= rdnums(11)
                re.checking_accound
                re.ban= rdnums(7)
                re.bik= rdnums(8)
                re.short_org_name = d['full_company']
                re.full_org_name  = d['full_company']
                re.juredical_address  = d['adress']
                re.mail_address = d['adress']
                re.fax = d['phone']
                re.phone1 = d['phone']
                re.E_mail = d['email']
                re.contact_person = d['fio']
                re.manager_roleImPad = d['post']
                re.manager_fioImPad = d['fio']
                re.manager_rolRdPad = d['fio']
                re.manager_fioRdPad = d['fio']
                re.own_company_my_button_fill = False



    active = fields.Boolean(default=True)
    company_type = fields.Selection([('svoe_ur_lico', 'svoe_ur_lico'),
    ('postavshic', 'postavshic')], default='svoe_ur_lico')

    price_list_ids = fields.Selection([('rd', 'Vibor PRICE LISTA')])
    type_os = fields.Boolean()
    type_lab = fields.Boolean()

    reglament = fields.Many2many("tech_directory.reglament")
    extra_service_ids = fields.Many2many('tech_directory.extra_service_group', 'tech_directory_extra_service_groups')

    inn = fields.Char()
    kpp = fields.Integer()
    ogrn_ogrnip = fields.Char()
    okpo = fields.Char()
    okved = fields.Char()
    checking_accound = fields.Char()
    bank= fields.Char()
    bik = fields.Char()
    cor_account = fields.Char()
    short_org_name = fields.Char()
    full_org_name = fields.Char()
    juredical_address = fields.Char()
    mail_address = fields.Char()
    fax = fields.Char()
    phone1 = fields.Char()
    phone2 = fields.Char()
    ogrn = fields.Integer()
    signature = fields.Char()
    client_code = fields.Char()
    E_mail = fields.Char()
    contact_person = fields.Char()
    independent_client = fields.Boolean()
    active_user = fields.Boolean()
    import_code = fields.Char()
    manager_roleImPad = fields.Char()
    manager_fioImPad = fields.Char()
    manager_rolRdPad = fields.Char()
    manager_fioRdPad = fields.Char()
    type_of_document = fields.Char()
    main_account_manager = fields.Char()
    main_account_manager_fio_RdPad = fields.Char()
    website = fields.Char()
