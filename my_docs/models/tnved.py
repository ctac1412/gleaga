# -*- coding: utf-8 -*-

from odoo import models, fields, api


class tnved(models.Model):
    _name = 'my_docs.tnved'

    name = fields.Text('name')
    text = fields.Char("text")
    parent_id =  fields.Char("parent_id")

class schema(models.Model):
    _name = 'my_docs.schema'
    name = fields.Char()
    doc_type = fields.Selection(selection=[('ds', 'ds'),
                                           ('ss', 'ss')])

class reglament(models.Model):
    _name = 'my_docs.reglament'
    name = fields.Text('Rglament name')
    number = fields.Char("Reglament number")

class post(models.Model):
    _name = 'my_docs.post'
    _rec_name = 'post_im_pad'
    post_im_pad = fields.Char()
    post_rd_pad = fields.Char()


class country(models.Model):
    _name = 'my_docs.country'
    name = fields.Char('Country Name', required=True, index=True)
    code = fields.Char('Country Code', size=4, required=True, index=True)


class country_region(models.Model):
    _name = 'my_docs.country_region'
    name = fields.Char('Region Name', required=True, index=True)


class type_ip(models.Model):
    _name = 'my_docs.type_ip'
    name = fields.Char('Type_form', required=True)
