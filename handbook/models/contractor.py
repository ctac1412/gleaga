# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from petrovich.main import Petrovich
from petrovich.enums import Case, Gender
from rddata import *
from data_data import suggest_api,clean_api

import json

class contractor(models.Model):
    _name = 'tech_directory.contractor'
    _rec_name = 'factory_name_kratkoe'

    client_id =  fields.Many2one("tech_directory.client")

    rukovoditel_dolzhnost_v_imenitelnom = fields.Char(required = 'True')
    rukovoditel_fio_v_imenitelnom = fields.Char(required = 'True')
    rukovoditel_dolzhnost_v_roditelnom = fields.Char(required = 'True')
    rukovoditel_fio_v_roditelnom = fields.Char(required = 'True')
    rukovoditel_osnovanie_doc = fields.Text()
    rukovoditel_phone = fields.Char(required = 'True')
    rukovoditel_email = fields.Char(required = 'True')

    buhgalter_phone = fields.Char()
    buhgalter_email = fields.Char()

    otvetstvennyj_po_sdelke = fields.Text()
    otvetstvennyj_po_sdelke_phone = fields.Char()
    otvetstvennyj_po_sdelke_email = fields.Char()

    factory_name = fields.Char(required = 'True')
    factory_name_kratkoe = fields.Char(required = 'True')
    factory_yuridicheskij_adres= fields.Text(required = 'True')
    factory_pochtovyj_adres= fields.Text()

    factory_inn= fields.Char()
    factory_kpp= fields.Char()
    factory_ogrn_ogrnip= fields.Char(required = 'True')
    factory_okpo= fields.Char()
    factory_okvehd= fields.Char()
    factory_raschetnyj_schet= fields.Char()
    factory_bank= fields.Char()
    factory_korr_schet = fields.Char()
    factory_bik= fields.Char()

    factory_status= fields.Boolean()
    factory_other_comment= fields.Text()

    dogovor_lab_ids= fields.One2many('tech_directory.dogovor','contractor_id', compute='_compute_dogovor_lab_ids')
    dogovor_os_ids = fields.One2many('tech_directory.dogovor','contractor_id', compute='_compute_dogovor_os_ids')
    my_button_fill  = fields.Boolean(store='False')
    nalog_api  = fields.Boolean(store='False')
    @api.one
    @api.depends('dogovor_lab_ids','dogovor_os_ids')
    def _compute_dogovor_lab_ids(self):
        re = self.env["tech_directory.dogovor"].search([("type_selection","=","lab")])
        self.dogovor_lab_ids = re


    @api.one
    @api.depends('dogovor_lab_ids','dogovor_os_ids')
    def _compute_dogovor_os_ids(self):
        re = self.env["tech_directory.dogovor"].search([("type_selection","=","os")])
        self.dogovor_os_ids = re

    def check_api(self,value):
        res=value
        if value == "null":
            res=''
        return res

    @api.multi
    @api.onchange("nalog_api")
    def _onchange_nalog_api(self):
        for re in self:
            if re.nalog_api:
                re.nalog_api = False
                if re.factory_ogrn_ogrnip:
                    try:
                        res = suggest_api(re.factory_ogrn_ogrnip, 'party')
                        data = res["data"]
                        value = res["value"]
                        unrestricted_value = res["unrestricted_value"]

                        re.factory_name = data['name']['full_with_opf']
                        re.factory_name_kratkoe = data['name']['short_with_opf']
                        re.factory_yuridicheskij_adres = data['address']['unrestricted_value']
                        re.factory_pochtovyj_adres = data['address']['unrestricted_value']
                        re.rukovoditel_fio_v_imenitelnom= data['management']['name']
                        re.rukovoditel_dolzhnost_v_imenitelnom = data['management']['post']
                        re.factory_inn = data['inn']
                        re.factory_kpp =  data['kpp']
                        re.factory_okpo = data['okpo']
                        re.factory_okvehd = data['okved']
                    except (ValueError, KeyError, TypeError):
                        print "JSON format error" + str(ValueError)

    @api.multi
    @api.onchange("my_button_fill")
    def _onchange_field(self):
        d=rdfast()
        fk_name = rdcompany_type() + ' ' + rdcompany()
        for re in self:
            if re.my_button_fill:
                re.my_button_fill = False
                re.rukovoditel_fio_v_imenitelnom= d['fio']
                re.rukovoditel_dolzhnost_v_imenitelnom = d['post']
                re.rukovoditel_osnovanie_doc = rdnums(7)
                re.rukovoditel_phone = d['phone']
                re.rukovoditel_email = d['email']
                re.buhgalter_phone = rdphone()
                re.buhgalter_email = rdemail()
                re.otvetstvennyj_po_sdelke = rdfio()
                re.otvetstvennyj_po_sdelke_phone = rdphone()
                re.otvetstvennyj_po_sdelke_email = rdemail()
                re.factory_name = fk_name
                re.factory_name_kratkoe = fk_name + u' краткое'
                re.factory_yuridicheskij_adres = rdadress()
                re.factory_pochtovyj_adres = rdadress()
                re.factory_inn = rdnums(11)
                re.factory_kpp = rdnums(11)
                re.factory_ogrn_ogrnip = rdnums(11)
                re.factory_okpo = rdnums(11)
                re.factory_okvehd = rdnums(11)
                re.factory_raschetnyj_schet = rdnums(18)
                re.factory_bank = rdnums(9)
                re.factory_korr_schet = rdnums(15)
                re.factory_bik = rdnums(8)

    @api.onchange('rukovoditel_fio_v_imenitelnom')
    def _skloninefio(self):
        if self.rukovoditel_fio_v_imenitelnom:
            fio = self.rukovoditel_fio_v_imenitelnom
            fio = fio.split(' ')
            if len(fio)==3:
                p = Petrovich()
                surname=fio[0]
                name=fio[1]
                lastname=fio[2]
                self.rukovoditel_fio_v_roditelnom =p.lastname(surname, Case.GENITIVE) + ' ' + p.firstname(name, Case.GENITIVE) + ' '  + p.middlename(lastname, Case.GENITIVE)

    @api.onchange('rukovoditel_dolzhnost_v_imenitelnom')
    def _dolzhnost(self):
        if self.rukovoditel_dolzhnost_v_imenitelnom:
            p = Petrovich()
            res = ''
            for member in self.rukovoditel_dolzhnost_v_imenitelnom.split(' '):
                if member != '':
                    res = res+p.lastname(member, Case.GENITIVE) + ' '
            self.rukovoditel_dolzhnost_v_roditelnom = res.strip()
