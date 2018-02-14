# -*- coding: utf-8 -*-

from odoo import models, fields, api
from petrovich.main import Petrovich
from petrovich.enums import Case, Gender




class partner(models.Model):
    _name = 'my_docs.partner'
    _rec_name = 'Title'

    type_of_partner = fields.Selection(selection=[
        ('urlico', 'urlico'),
        ('ip', 'ip'),
        ('fizlico', 'fizlico'),
        ('foreign', 'foreign'),
    ], default="urlico")

    type_ip_id = fields.Many2one(
        comodel_name="my_docs.type_ip"
    )

    @api.onchange("type_of_partner" )
    def _onchange_type_of_partner(self):
        if self.type_of_partner !='ip':
            self.type_ip_id = [5]

    Title = fields.Char('Polnoe nazvanie', required=True)
    address = fields.Char('Mesto Nahogdeniya Address')
    country_id = fields.Many2one('my_docs.country', 'Strana')
    region_id = fields.Many2one('my_docs.country_region', 'Russian Region')
    index =  fields.Char('index')

    phone = fields.Char('Phone')
    email = fields.Char('Email')
    faxnum = fields.Char('Fax')

    address_is_same = fields.Boolean('Address sovpadaet', default=True)

    address_real = fields.Char('Mesto Nahogdeniya Address')
    country_real_id = fields.Many2one('my_docs.country', 'Strana')
    region_real_id = fields.Many2one(
        'my_docs.country_region', 'Russian Region')
    index_real = fields.Char('index')

    org_prav_forma = fields.Char('Org Prav Forma')
    svedeniya_o_gos_reg = fields.Char('Svedeniya O Gos Reg')
    ogrn = fields.Char('OGRN')
    vidano = fields.Char('Svidetelctvo o Registracii Vidano')
    data_vidachi = fields.Date('Data Vidachi Svidetelctva')

    inn = fields.Char('INN')
    okpo = fields.Char('OKPO')

    # -------------------------------------
    # IP
    # partner_ip_form_id = fields.Many2one('labs.partner_ip_form', 'Vid individualnogo predprinimatelya')
    # -------------------------------------
    # IP

    fio_head = fields.Char('FIO Rukovoditelya')
    fio_head_rod_pad = fields.Char('FIO Rukovoditelya v Roditelnom Padege')
    fio_head_dat_pad = fields.Char('FIO Rukovoditelya v Datelnom padege')
    head_role = fields.Many2one(
        comodel_name="my_docs.post",
    )
    head_role_rod_pad = fields.Char(related="head_role.post_rd_pad", readonly=True)
    head_doc = fields.Char('Deistvuyushego Na Osnovanii')

    @api.onchange('fio_head')
    def _skloninefio(self):
        if self.fio_head:
            fio = self.fio_head.split(' ')
            if len(fio) == 3:
                p = Petrovich()
                surname = fio[0]
                name = fio[1]
                lastname = fio[2]
                self.fio_head_rod_pad = p.lastname(surname, Case.GENITIVE) + ' ' + p.firstname(
                    name, Case.GENITIVE) + ' ' + p.middlename(lastname, Case.GENITIVE)
                self.fio_head_dat_pad = p.lastname(surname, Case.DATIVE) + ' ' + p.firstname(
                    name, Case.DATIVE) + ' ' + p.middlename(lastname, Case.DATIVE)

    @api.multi
    @api.onchange('address_is_same', 'country_id', 'region_id', 'address','index')
    def _change_address_is_same(self):
        for r in self:
            if r.address_is_same:
                r.address_real = r.address
                r.country_real_id = r.country_id
                r.region_real_id = r.region_id
                r.index_real = r.index

class partner_kz(models.Model):
    _name = 'my_docs.partnerr_kz'
    _inherit = 'my_docs.partner'

    title_kz = fields.Char('Polnoe nazvanie', required=True)
    address_kz = fields.Char('Mesto Nahogdeniya Address')
    country_id_kz = fields.Many2one('my_docs.country', 'Strana')
    region_id_kz = fields.Many2one('my_docs.country_region', 'Russian Region')
    index_kz =  fields.Char('index')

    address_real_kz = fields.Char('Mesto Nahogdeniya Address')
    country_real_id_kz = fields.Many2one('my_docs.country', 'Strana')
    region_real_id_kz = fields.Many2one(
        'my_docs.country_region', 'Russian Region')
    index_real_kz = fields.Char('index')

    org_prav_forma_kz = fields.Char('Org Prav Forma')
    svedeniya_o_gos_reg_kz = fields.Char('Svedeniya O Gos Reg')
    ogrn_kz = fields.Char('OGRN')
    vidano_kz = fields.Char('Svidetelctvo o Registracii Vidano')
    data_vidachi_kz = fields.Date('Data Vidachi Svidetelctva')

    inn_kz = fields.Char('INN')
    okpo_kz = fields.Char('OKPO')

    fio_head_kz = fields.Char('FIO Rukovoditelya')
    fio_head_rod_pad_kz = fields.Char('FIO Rukovoditelya v Roditelnom Padege')
    fio_head_dat_pad_kz = fields.Char('FIO Rukovoditelya v Datelnom padege')
    head_role_kz = fields.Many2one(
        comodel_name="my_docs.post",
    )
    head_role_rod_pad_kz = fields.Char(related="head_role.post_rd_pad", readonly=True)
    head_doc_kz = fields.Char('Deistvuyushego Na Osnovanii')

class partner_local(models.Model):
    _name = 'my_docs.partner_local'
    _inherit = 'my_docs.partner'

    partner_id = fields.Many2one(
        comodel_name="my_docs.partner"
    )

    @api.multi
    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        fil = ['type_of_partner', 'type_ip_id',
               'Title',
               'address',
               'country_id',
               'region_id',
               'index',
               'phone',
               'email',
               'faxnum',
               'address_is_same',
               'address_real',
               'country_real_id',
               'region_real_id',
               'index_real',
               'org_prav_forma',
               'svedeniya_o_gos_reg',
               'ogrn',
               'vidano',
               'data_vidachi',
               'inn',
               'okpo',
               'fio_head',
               'fio_head_rod_pad',
               'fio_head_dat_pad',
               'head_role',
               'head_role_rod_pad',
               'head_doc']
        for i in fil:
            setattr(self, i,  getattr(self.partner_id, i))
