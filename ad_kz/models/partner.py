# -*- coding: utf-8 -*-

from odoo import models, fields, api
from petrovich.main import Petrovich
from petrovich.enums import Case, Gender


class partner_kz(models.Model):
    _name = 'ad_kz.partner_kz'
    _rec_name = 'title'

    type_of_partner = fields.Selection(selection=[
        ('urlico', 'urlico'),
        ('ip', 'ip'),
        ('fizlico', 'fizlico'),
        ('foreign', 'foreign'),
    ], default="urlico")

    type_ip_id = fields.Many2one(
        comodel_name="ad_kz.type_ip"
    )

    @api.onchange("type_of_partner" )
    def _onchange_type_of_partner(self):
        if self.type_of_partner !='ip':
            self.type_ip_id = [5]

    title = fields.Char('Polnoe nazvanie', required=True)
    address = fields.Text('Mesto Nahogdeniya Address')
    country_id = fields.Many2one('ad_kz.country', 'Strana')
    region_id = fields.Many2one('ad_kz.country_region', 'Russian Region')
    index = fields.Char('index')

    phone = fields.Char('Phone')
    email = fields.Char('Email')
    faxnum = fields.Char('Fax')

    address_is_same = fields.Boolean('Address sovpadaet', default=True)

    address_real = fields.Text('Mesto Nahogdeniya Address')
    country_real_id = fields.Many2one('ad_kz.country', 'Strana')
    region_real_id = fields.Many2one(
        'ad_kz.country_region', 'Russian Region')
    index_real = fields.Char('index')

    org_prav_forma  = fields.Many2one(
        comodel_name="ad_kz.proove_form"
    )
    svedeniya_o_gos_reg = fields.Char('Svedeniya O Gos Reg')
    ogrn = fields.Char('OGRN')
    vidano = fields.Char('Svidetelctvo o Registracii Vidano')
    data_vidachi = fields.Date('Data Vidachi Svidetelctva')

    inn = fields.Char('INN')
    okpo = fields.Char('OKPO')
    head_doc = fields.Char('Deistvuyushego Na Osnovanii')
    # -------------------------------------
    # IP
    # partner_ip_form_id = fields.Many2one('labs.partner_ip_form', 'Vid individualnogo predprinimatelya')
    # -------------------------------------
    # IP

    fio_item_id = fields.Many2one(
        comodel_name="ad_kz.fio_item"
    )

    fio_head = fields.Char(related='fio_item_id.name',readonly=True)
    fio_head_rod_pad = fields.Char(related='fio_item_id.name_rod_pad',readonly=True)
    fio_head_dat_pad = fields.Char(related='fio_item_id.name_dat_pad',readonly=True)
    head_role = fields.Char(related='fio_item_id.post_id.post_im_pad',readonly=True)
    head_role_rod_pad = fields.Char(
        related="fio_item_id.post_id.post_rd_pad", readonly=True)


    # @api.onchange('fio_head')
    # def _skloninefio(self):
    #     if self.fio_head:
    #         fio = self.fio_head.split(' ')
    #         if len(fio) == 3:
    #             p = Petrovich()
    #             surname = fio[0]
    #             name = fio[1]
    #             lastname = fio[2]
    #             self.fio_head_rod_pad = p.lastname(surname, Case.GENITIVE) + ' ' + p.firstname(
    #                 name, Case.GENITIVE) + ' ' + p.middlename(lastname, Case.GENITIVE)
    #             self.fio_head_dat_pad = p.lastname(surname, Case.DATIVE) + ' ' + p.firstname(
    #                 name, Case.DATIVE) + ' ' + p.middlename(lastname, Case.DATIVE)

    @api.multi
    @api.onchange('address_is_same', 'country_id', 'region_id', 'address', 'index')
    def _change_address_is_same(self):
        for r in self:
            if r.address_is_same:
                r.address_real = r.address
                r.country_real_id = r.country_id
                r.region_real_id = r.region_id
                r.index_real = r.index

    title_kz = fields.Char('Polnoe nazvanie', required=True)
    address_kz = fields.Text('Mesto Nahogdeniya Address')
    address_real_kz = fields.Text('Mesto Nahogdeniya Address')

    svedeniya_o_gos_reg_kz = fields.Char('Svedeniya O Gos Reg')
    vidano_kz = fields.Char('Svidetelctvo o Registracii Vidano')
    head_doc_kz = fields.Char('Deistvuyushego Na Osnovanii')

    # READ ONLY PART
    org_prav_forma_kz = fields.Char( related='org_prav_forma.name_kz',readonly=True)
    country_id_kz = fields.Char(related='country_id.name_kz',readonly=True)
    region_id_kz = fields.Char(related='region_id.name_kz',readonly=True )
    index_kz = fields.Char(related='index',readonly=True)

    country_real_id_kz = fields.Char(related='country_real_id.name_kz',readonly=True)
    region_real_id_kz = fields.Char(related='region_real_id.name_kz',readonly=True )
    index_real_kz = fields.Char(related='index_real',readonly=True)

    ogrn_kz = fields.Char(related='ogrn',readonly=True)
    data_vidachi_kz = fields.Date(related='data_vidachi',readonly=True)
    inn_kz = fields.Char(related='inn',readonly=True)
    okpo_kz = fields.Char(related='okpo',readonly=True)
    fio_item_id_kz = fields.Char(
            related='fio_item_id.compute_name',
            string='Fio KZ'
        )

    fio_head_kz = fields.Char(related='fio_item_id.name_kz',readonly=True)
    fio_head_rod_pad_kz = fields.Char(related='fio_item_id.name_rod_pad_kz',readonly=True)
    fio_head_dat_pad_kz = fields.Char(related='fio_item_id.name_dat_pad_kz',readonly=True)
    head_role_kz = fields.Char(rselated='fio_item_id.post_id.post_im_pad_kz',readonly=True)
    head_role_rod_pad_kz = fields.Char(
        related="fio_item_id.post_id.post_rd_pad_kz", readonly=True)
    # READ ONLY PART
class change_class(models.AbstractModel):
    _name = 'ad_kz.change_class'

    replicate_list = ['title',
                      'address',
                      # 'country_id',
                      # 'region_id',
                      # 'index',
                      # 'phone',
                      # 'email',
                      # 'faxnum',
                      # 'address_is_same',
                      'address_real',
                      # 'country_real_id',
                      # 'region_real_id',
                      # 'index_real',
                      # 'org_prav_forma',
                      'svedeniya_o_gos_reg',
                      # 'ogrn',
                      'vidano',
                      # 'data_vidachi',
                      # 'inn',
                      # 'okpo',
                      # 'fio_head',
                      # 'fio_head_rod_pad',
                      # 'fio_head_dat_pad'
                      ]

    @api.multi
    def replicate_to_kz(self):
        for r in self:
            for item in self.replicate_list:
                self[item + '_kz'] = self[item]

    # @api.onchange("title")
    # @api.multi
    # def _onchange_field(self):
    #     if not self.title_kz:
    #         self.title_kz = self.title
    #
    # @api.onchange("address")
    # @api.multi
    # def _onchange_field(self):
    #     if not self.address_kz:
    #         self.address_kz = self.address
    #
    # @api.onchange("country_id")
    # @api.multi
    # def _onchange_field(self):
    #     if not self.country_id_kz:
    #         self.country_id_kz = self.country_id
    #
    # @api.onchange("region_id")
    # @api.multi
    # def _onchange_field(self):
    #     if not self.region_id_kz:
    #         self.region_id_kz = self.region_id
    #
    # @api.onchange("index")
    # @api.multi
    # def _onchange_field(self):
    #     if not self.index_kz:
    #         self.index_kz = self.index
    #
    # @api.onchange("address_real")
    # @api.multi
    # def _onchange_field(self):
    #     if not self.address_real_kz:
    #         self.address_real_kz = self.address_real
class partner_local_kz(models.Model):
    _name = 'ad_kz.partner_local_kz'
    _inherit = ['ad_kz.partner_kz', 'ad_kz.change_class']

    partner_id = fields.Many2one(
        comodel_name="ad_kz.partner_kz"
    )
    @api.multi
    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        fil = [
        # 'type_of_partner',
         # 'type_ip_id',
            'type_of_partner',
            'type_ip_id',
            'title',
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
            'head_doc',
            'fio_item_id',
            'fio_head',
            'fio_head_rod_pad',
            'fio_head_dat_pad',
            'head_role',
            'head_role_rod_pad',

            'title_kz',
            'address_kz',
            'country_id_kz',
            'region_id_kz',
            'index_kz',
            'address_real_kz',
            'country_real_id_kz',
            'region_real_id_kz',
            'index_real_kz',
            'org_prav_forma_kz',
            'svedeniya_o_gos_reg_kz',
            'ogrn_kz',
            'vidano_kz',
            'data_vidachi_kz',
            'inn_kz',
            'okpo_kz',
            'head_doc_kz',
            'fio_item_id_kz',
            'fio_head_kz',
            'fio_head_rod_pad_kz',
            'fio_head_dat_pad_kz',
            'head_role_kz',
            'head_role_rod_pad_kz',



               ]
        for i in fil:
            setattr(self, i,  getattr(self.partner_id, i))
