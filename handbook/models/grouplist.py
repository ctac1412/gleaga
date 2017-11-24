# -*- coding: utf-8 -*-

from odoo import models, fields, api

class grouplist(models.Model):
    _name = 'tech_directory.grouplist'
    reglament_ids = fields.One2many('tech_directory.reglament','group_id', readonly = True)
    name = fields.Text('Group name')

    def _check_id(self):
        if self.id:
            self.check_id = True
        else:
            self.check_id = False
# False = создание
# True =  редактирование


    check_id = fields.Boolean( compute='_check_id')
    reglament_main_id  = fields.Many2one(
        string="reglament_main_id",
        comodel_name="tech_directory.reglament"
    )
