# -*- coding: utf-8 -*-

from odoo import models, fields, api
from petrovich.main import Petrovich
from petrovich.enums import Case, Gender

class partner(models.Model):
    _name = 'my_docs.partner'
    _rec_name='rek_name'
    type_of_partner=fields.Selection(selection=[
                ('urlico', 'urlico'),
                ('ip', 'ip'),
                ('fizlico', 'fizlico'),
                ('foreign', 'foreign'),
        ],default="urlico")

    name_im_pad = fields.Char(required=True)
    name_rd_pad = fields.Char()

    dolznhost_im_pad_id  = fields.Many2one(
            comodel_name="my_docs.post",
            )

    dolznhost_rd_pad = fields.Char(related="dolznhost_im_pad_id.post_rd_pad")

    rek_name = fields.Char(index=True)
    rek_result = fields.Text()

    address = fields.Char('Mesto Nahogdeniya Address')
    country_id = fields.Many2one('my_docs.country', 'Strana')
    region_id = fields.Many2one('my_docs.country_region', 'Russian Region')

    address_is_same = fields.Boolean('Address sovpadaet', default=True)

    address_real = fields.Char('Mesto Nahogdeniya Address')
    country_real_id = fields.Many2one('my_docs.country', 'Strana')
    region_real_id = fields.Many2one('my_docs.country_region', 'Russian Region')

    @api.onchange('address_is_same', 'country_id', 'region_id', 'address')
    def _change_address_is_same(self):
        for r in self:
            if r.address_is_same:
                r.address_real = r.address
                r.country_real_id = r.country_id
                r.region_real_id = r.region_id

    rek_real_adress = fields.Text()
    rek_phone = fields.Char()
    rek_fax = fields.Char()
    rek_email= fields.Char()
    rek_inn = fields.Char()
    rek_ogrn = fields.Char()

    @api.onchange('name_im_pad')
    def _skloninefio(self):
        if self.name_im_pad:
            fio = self.name_im_pad
            fio = fio.split(' ')
            if len(fio) == 3:
                p = Petrovich()
                surname = fio[0]
                name = fio[1]
                lastname = fio[2]
                self.name_rd_pad = p.lastname(surname, Case.GENITIVE) + ' ' + p.firstname(
                    name, Case.GENITIVE) + ' ' + p.middlename(lastname, Case.GENITIVE)

class post(models.Model):
    _name = 'my_docs.post'
    _rec_name= 'post_im_pad'
    post_im_pad=fields.Char()
    post_rd_pad=fields.Char()

class country(models.Model):
    _name = 'my_docs.country'
    name =  fields.Char('Country Name', required=True, index=True)
    code =  fields.Char('Country Code', size=4, required=True, index=True)

class country_region(models.Model):
    _name = 'my_docs.country_region'
    name =  fields.Char('Region Name', required=True, index=True)
