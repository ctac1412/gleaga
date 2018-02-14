# -*- coding: utf-8 -*-

from odoo import models, fields, api
from rddata import *
from odoo.exceptions import UserError, RedirectWarning, ValidationError
from datetime import datetime, date, time
import json


class task(models.Model):
    _name = 'my_docs.task'
    _rec_name = 'name'
    _inherit = ['mail.thread']

    task_parent_id = fields.Many2one(
        comodel_name="my_docs.task"
    )
    task_child_id = fields.Many2one(
        comodel_name="my_docs.task"
    )

    @api.multi
    def copy_to_child(self):
        new_vals = {}
        for r in self:
            child = r.task_child_id
            if child:
                child.ShippingDocumentation = r.ShippingDocumentation
                child.ManufacturerInfo = r.ManufacturerInfo
                child.DeliveryContract = r.DeliveryContract
                child.ProductType = r.ProductType
                child.AcceptanceReason = r.AcceptanceReason
                child.ProductIdentification = r.ProductIdentification
                child.reglament_ids = r.reglament_ids
                child.ApplicantInfo = r.ApplicantInfo
                child.supplement_free_form_ids = r.supplement_free_form_ids
                child.ProductInfo = r.ProductInfo
                child.Part = r.Part
                child.DocumentValidity = r.DocumentValidity
                child.ApplicantType = r.ApplicantType
                child.tnved_ids = r.tnved_ids
                child.ProductIdentificationOther = r.ProductIdentificationOther
                child.shema_id = r.shema_id
                child.ProductLocation = r.ProductLocation
                child.Applicant_partner_id = r.Applicant_partner_id
                child.Manufacturer_partner_id = r.Manufacturer_partner_id
                child.Invoice = r.Invoice

    @api.multi
    def copy_to_parent(self):
        new_vals = {}
        for r in self:
            parent = r.task_parent_id
            if parent:
                parent.ShippingDocumentation = r.ShippingDocumentation
                parent.ManufacturerInfo = r.ManufacturerInfo
                parent.DeliveryContract = r.DeliveryContract
                parent.ProductType = r.ProductType
                parent.AcceptanceReason = r.AcceptanceReason
                parent.ProductIdentification = r.ProductIdentification
                parent.reglament_ids = r.reglament_ids
                parent.ApplicantInfo = r.ApplicantInfo
                parent.supplement_free_form_ids = r.supplement_free_form_ids
                parent.ProductInfo = r.ProductInfo
                parent.Part = r.Part
                parent.DocumentValidity = r.DocumentValidity
                parent.ApplicantType = r.ApplicantType
                parent.tnved_ids = r.tnved_ids
                parent.ProductIdentificationOther = r.ProductIdentificationOther
                parent.shema_id = r.shema_id
                parent.ProductLocation = r.ProductLocation
                parent.Applicant_partner_id = r.Applicant_partner_id
                parent.Manufacturer_partner_id = r.Manufacturer_partner_id
                parent.Invoice = r.Invoice

    @api.multi
    def resent(self):
        for r in self:
            default = {
                'name': 'Replicate of ' + r.name,
                'sender_expert_id': self.env.user.id,
                'sender_company_id': self.env.user.company_id.id,
                'getter_expert_id': [],
                'getter_company_id': [],
                'task_parent_id': r.id,
            }

            res = r.copy(default=default)
            r.write({'task_child_id': res.id})
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'current',
                'res_model': 'my_docs.task',
                'res_id': res.id,
            }
        # return res

    @api.multi
    def _is_user_company_getter_company(self):
        for r in self:
            r.is_user_company_getter_company = self.env.user.company_id.id == r.getter_company_id.id

    is_user_company_getter_company = fields.Boolean(
        compute="_is_user_company_getter_company")

    @api.multi
    def write(self, vals={}):

        if self._name == 'my_docs.task':
            new_recodrs = []
            block_list = ['task_log_ids', 'state', 'message_follower_ids',
                          'supplement_free_form_ids', 'getter_company_id', 'getter_expert_id']
            for i in vals:
                if i not in block_list and getattr(self, i) != vals[i]:
                    # if 'local_task' in self._name:
                    #     new_recodrs.append((0,0,{'local_task_id':self.id, 'name':i, 'value_before':getattr(self,i), 'value_after':vals[i], 'change_user':self.env.user.name}))
                    # else:
                    new_recodrs.append((0, 0, {'task_id': self.id, 'name': i, 'value_before': getattr(
                        self, i), 'value_after': vals[i], 'change_user': self.env.user.name}))
            if new_recodrs:
                vals['task_log_ids'] = new_recodrs

        super(task, self).write(vals)
        return True

    def set_new_expert(self):
        view_id = self.env.ref('my_docs.set_expert_wizard_form').id
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'my_docs.set_expert_wizard',
            'view_id': view_id,
            'context': {'default_task_id': self.id}
        }

    def generate_adress(self, record, vid_partner):
        for r in record:
            res = []

            def _manufacturer_adress_generator():
                if not r.address_is_same and r.address != r.address_real:
                    if r.type_of_partner in ['urlico', 'fizlico', 'foreign']:
                        res.append(u'Место нахождения: ')
                    elif r.type_of_partner in ['ip']:
                        res.append(u'Место жительства: ')

                    if r.country_id.code == 'RU':
                        res.append(r.country_id.name)
                    if r.region_id:
                        res.append(r.region_id.name)
                    if r.index:
                        res.append(r.index)
                    if r.address:
                        res.append(r.address)
                    if r.country_id.code != 'RU':
                        res.append(r.country_id.name)

                    res.append(
                        u'адрес места осуществления деятельности по изготовлению продукции: ')
                    if r.country_real_id.code == 'RU':
                        res.append(r.country_real_id.name)
                    if r.region_real_id:
                        res.append(r.region_real_id.name)
                    if r.index_real:
                        res.append(r.index_real)
                    if r.address_real:
                        res.append(r.address_real)
                    if r.country_real_id.code != 'RU':
                        res.append(r.country_real_id.name)

                else:
                    if r.type_of_partner in ['urlico', 'fizlico', 'foreign']:
                        res.append(
                            u'Место нахождения и адрес места осуществления деятельности по изготовлению продукции: ')
                    elif r.type_of_partner in ['ip']:
                        res.append(
                            u'Место жительства и адрес места осуществления деятельности по изготовлению продукции: ')

                    if r.country_id.code == 'RU':
                        res.append(r.country_id.name)
                    if r.region_id:
                        res.append(r.region_id.name)
                    if r.index:
                        res.append(r.index)
                    if r.address:
                        res.append(r.address)
                    if r.country_id.code != 'RU':
                        res.append(r.country_id.name)

            def _ogrn_generator():
                if r.type_of_partner in ['urlico', 'fizlico', 'foreign']:
                    if r.country_id.code == 'KZ':
                        return u'бизнес-идентификационный номер: ' + r.ogrn
                    elif r.country_id.code in ['BY', 'AR']:
                        return u'учетный номер плательщика: ' + r.ogr
                    elif r.country_id.code == 'KY':
                        return u'идентификационный налоговый номер налогоплательщика: ' + r.ogrn
                    elif r.country_id.code == 'RU':
                        return u'основной государственный регистрационный номер: ' + r.ogrn
                    else:
                        return u'основной государственный регистрационный номер: ' + r.ogrn
                elif r.type_of_partner in ['ip']:
                    if r.country_id.code == 'KZ':
                        # индивидуальный Идентификационный Номер
                        return u'бизнес-идентификационный номер: ' + r.ogrn
                    elif r.country_id.code in ['BY']:
                        return u'свидетельство о государственной регистрации индивидуального предпринимателя: ' + r.ogrn
                    elif r.country_id.code in ['AR']:
                        return u'свидетельство о государственной регистрации: ' + r.ogrn
                    elif r.country_id.code == 'KY':
                        return u'свидетельство о государственной регистрации физического лица, занимающегося предпринимательской деятельностью: ' + r.ogrn
                    elif r.country_id.code == 'RU':
                        return u'основной государственный регистрационный номер: ' + r.ogrn
                    else:
                        return u'основной государственный регистрационный номер: ' + r.ogrn

            def _applicant_adress_generator():
                if not r.address_is_same and r.address != r.address_real:
                    if r.type_of_partner in ['urlico', 'fizlico', 'foreign']:
                        res.append(u'Место нахождения: ' + r.country_id.name)
                    elif r.type_of_partner in ['ip']:
                        res.append(u'Место жительства: ' + r.country_id.name)
                    if r.region_id:
                        res.append(r.region_id.name)
                    if r.index:
                        res.append(r.index)
                    if r.address:
                        res.append(r.address)
                    res.append(
                        u'адрес места осуществления деятельности:' + r.country_real_id.name)
                    if r.region_real_id:
                        res.append(r.region_real_id.name)
                    if r.index_real:
                        res.append(r.index_real)
                    if r.address_real:
                        res.append(r.address_real)
                else:
                    if r.type_of_partner in ['urlico', 'fizlico', 'foreign']:
                        res.append(
                            u'Место нахождения и адрес места осуществления деятельности: ' + r.country_id.name)
                    elif r.type_of_partner in ['ip']:
                        res.append(
                            u'Место жительства и адрес места осуществления деятельности: ' + r.country_id.name)
                    if r.region_id:
                        res.append(r.region_id.name)
                    if r.index:
                        res.append(r.index)
                    if r.address:
                        res.append(r.address)

            def _applicant_other_generator():
                if r.ogrn:
                    res.append(_ogrn_generator())
                if r.phone:
                    res.append(u'телефон: ' + r.phone)
                if r.email:
                    res.append(u'адрес электронной почты: ' + r.phone)
                if r.faxnum:
                    res.append(u'факс: ' + r.faxnum)

            if vid_partner in ['applicant']:
                _applicant_adress_generator()
                _applicant_other_generator()
            elif vid_partner in ['manufacturer']:
                _manufacturer_adress_generator()

            result = ", ".join(res)
            result = result.replace(': ,', ': ')
            result = result.replace('  ', ' ')
            return result

    @api.multi
    @api.onchange("ApplicantType")
    def _onchange_ApplicantType(self):
        if self.ApplicantType == "Manufacturer":
            self.Manufacturer_partner_id = self.Applicant_partner_id

    @api.multi
    @api.onchange("Applicant_partner_id", "Manufacturer_partner_id")
    def _onchange_applicant(self):
        if self.Applicant_partner_id:
            self.ApplicantInfo = self.generate_adress(
                self.Applicant_partner_id, vid_partner='applicant')
            self.ApplicantInFace = self.Applicant_partner_id.head_role_rod_pad + \
                " " + self.Applicant_partner_id.fio_head_rod_pad

        if self.Manufacturer_partner_id:
            self.ManufacturerInfo = self.generate_adress(
                self.Manufacturer_partner_id, vid_partner='manufacturer')
            if self.Manufacturer_partner_id.country_id.code in ['RU', 'KZ', 'AR', 'BY', 'KY'] and self.Applicant_partner_id.country_id.code in ['RU', 'KZ', 'AR', 'BY', 'KY'] and self.Manufacturer_partner_id.country_id.code == self.Applicant_partner_id.country_id.code:
                self.ProductLocation = "Local"
            else:
                self.ProductLocation = "Foreign"

    @api.multi
    @api.onchange("task_my_button_fill")
    def _onchange_field(self):
        d = rdfast()
        for re in self:
            if re.task_my_button_fill:
                re.ProductInfo = d['production']

    type_task = fields.Selection(selection=[(
        'ss', 'ss'), ('ds', 'ds'), ('request', 'request')], default='ds')

    getter_expert_id = fields.Many2one(
        comodel_name="res.users",
    )

    sender_expert_id = fields.Many2one(
        comodel_name="res.users",
        default=lambda self: self.env.user
    )

    getter_company_id = fields.Many2one(
        comodel_name="res.company"
    )
    sender_company_id = fields.Many2one(
        comodel_name="res.company",
        default=lambda self: self.env.user.company_id
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('new', 'New'),
        ('await_expert', 'await_expert'),
        ('await_client', 'await_client'),
        ('end', 'End')
    ], default='draft')

    def open(self):
        print 'm0011111------------------------------------------'
        print self.id

    # @api.model
    # def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
    #     """ Override read_group to always display all states. """
    #     if groupby and groupby[0] == "state":
    #         # Default result structure
    #         states = [
    #             ('draft', 'Draft'),
    #             ('new', 'New'),
    #             ('await_expert', 'await_expert'),
    #             ('await_client', 'await_client'),
    #             ('end', 'End')
    #         ]
    #
    #         read_group_all_states = [{
    #             '__context': {'group_by': groupby[1:]},
    #             '__domain': domain + [('state', '=', state_value)],
    #             'state': state_value,
    #             'state_count': 0,
    #         } for state_value, state_name in states]
    #         # Get standard results
    #         read_group_res = super(task, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby)
    #         # Update standard results with default results
    #         result = []
    #         for state_value, state_name in states:
    #             res = filter(lambda x: x['state'] == state_value, read_group_res)
    #             if not res:
    #                 res = filter(lambda x: x['state'] == state_value, read_group_all_states)
    #             if state_value == 'cancel':
    #                 res[0]['__fold'] = True
    #             res[0]['state'] = [state_value, state_name]
    #             result.append(res[0])
    #         return result
    #     else:
    #         return super(task, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby)

    active = fields.Boolean(default=True)
    expert_enter = fields.Boolean(string="expert_enter", default=False)
    client_enter = fields.Boolean(string="client_enter", default=False)

    ApplicantType = fields.Selection(selection=[
        ('Manufacturer', u'Изготовитель'),
        ('Seller', u'Продавец'),
        ('Supplier', u'Поставщик'),
        ('AuthorizedPerson', u'Уполномоченное изготовителем лицо'),
    ], default="AuthorizedPerson")

    Applicant_partner_id = fields.Many2one(
        comodel_name="my_docs.partner_local"
    )

    Manufacturer_partner_id = fields.Many2one(
        comodel_name="my_docs.partner_local"
    )

    task_my_button_fill = fields.Boolean()

    ApplicantInfo = fields.Text()
    ApplicantInFace = fields.Char()
    ManufacturerInfo = fields.Text()

    @api.onchange("ProductType")
    @api.multi
    def _onchange_ProductType(self):
        for r in self:
            if r.ProductType == 'Serial':
                r.Part = ''
                r.Invoice = ''

    app_date = fields.Date(readonly=True, index=True,
                           default=fields.Date.context_today)
    start_date = fields.Date(default=fields.Date.context_today)
    end_date = fields.Date(default=fields.Date.context_today)

    ProductType = fields.Selection(
        selection=[('Serial', 'Serial'), ('Part', 'Part'), ('Single', 'Single')], default="Serial")
    ProductInfo = fields.Text()
    ProductIdentification = fields.Text()
    ShippingDocumentation = fields.Char(
        string="Rekvizity tovarosoprovoditel'noj dokumentacii")
    Part = fields.Char(string="Kolichestvo partii")
    Invoice = fields.Char(string="Invoice")
    DeliveryContract = fields.Char(
        string="Nomer i data dogovora ili kontrakta o postavke produkcii")
    ProductIdentificationOther = fields.Char(
        string="Inaya informaciya, identificiruyushchaya produkciyu")

    tnved_ids = fields.Many2many(
        comodel_name="my_docs.tnved", string='Kod TNVED')
    reglament_ids = fields.Many2many("my_docs.reglament")

    DocumentValidity = fields.Char(
        string="Srok dejstviya deklaracii o sootvetstvii:")
    # AdditionalInfo
    AcceptanceReason = fields.Char(string="Protokol ispitanii")
    ProductLocation = fields.Selection(
        selection=[('Local', 'otechestvennaya'), ('Foreign', 'importnaya')], default="Local", readonly=True)

    shema_id = fields.Many2one(
        comodel_name="my_docs.schema",
    )
    name = fields.Char(default=u"Новая задача")

    task_log_ids = fields.One2many(
        comodel_name="my_docs.task_log",
        inverse_name="task_id",
    )
    supplement_free_form_ids = fields.One2many(
        comodel_name="my_docs.supplement_free_form",
        inverse_name="task_id",
    )

    @api.multi
    def _watcher_id(self):
        for r in self:
            r.watcher_id = self.env.user

    @api.multi
    def _watcher_company_id(self):
        for r in self:
            r.watcher_company_id = self.env.user.company_id

    @api.multi
    def _my_role(self):
        for r in self:
            if r.getter_expert_id == self.env.user:
                r.my_role = 'getter'
            elif r.sender_expert_id == self.env.user or r.create_uid == self.env.user:
                r.my_role = 'sender'
            elif r.getter_company_id in self.env.user.company_ids:
                r.my_role = 'getter_watcher'
            elif r.sender_company_id in self.env.user.company_ids:
                r.my_role = 'sender_watcher'
            else:
                r.my_role = 'who_i_am'

    watcher_id = fields.Many2one(comodel_name='res.users', compute=_watcher_id)
    watcher_company_id = fields.Many2one(
        comodel_name='res.company', compute=_watcher_company_id)

    @api.multi
    def open_record(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'my_docs.task',
            'name': 'Record name',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'current',
        }

    my_role = fields.Selection(selection=[
        ('getter', 'getter'),
        ('sender', 'sender'),
        ('sender_watcher', 'sender_watcher'),
        ('getter_watcher', 'getter_watcher'),
        ('who_i_am', 'who_i_am????')
    ], compute=_my_role, default="sender")

    @api.one
    def first_send(self):
        self.state = 'new'
        self.log_prod(self.state)

    @api.one
    def toggle_client_enter(self):
        self.client_enter = not self.client_enter

    @api.one
    def toggle_expert_enter(self):
        self.expert_enter = not self.expert_enter

    @api.multi
    def state_draft(self):
        self.state = 'draft'
        self.log_prod(self.state)

    @api.multi
    def state_new(self):
        self.state = 'new'
        self.log_prod(self.state)

    @api.multi
    def create_new_task(self):
        print 'm0001------------------------------------------'
        for r in self:
            r.state = 'new'
            r.log_prod(r.state)
            for c in r.message_follower_ids:
                c.subtype_ids = [(6, 0, [1, 2])]

            company_rec = self.env.user.company_id
            company_rec.sudo().write(
                {'task_count': company_rec.task_count + 1})
            r.name = str(company_rec.task_count + 1)
            print 'm0002------------------------------------------'

    @api.multi
    def state_await_expert(self):
        if self.getter_company_id:
            self.state = 'await_expert'
            self.log_prod(self.state)
        else:
            raise UserError("Pls choose the getter company")

    @api.multi
    def state_await_client(self):
        print 'm00888------------------------------------------'
        for r in self:
            r.state = 'await_client'
            r.log_prod(r.state)
        print 'm00890------------------------------------------'

    @api.multi
    def state_end(self):
        self.state = 'end'
        self.log_prod(self.state)

    @api.multi
    def log_prod(self, action):
        for r in self:
            msg = ''
            if action == 'await_client' and r.sender_expert_id:
                print 'm00892------------------------------------------'
                msg = u"%s, нужно ваше внимание." % (
                    r.sudo().sender_expert_id.name)
            elif action == 'await_expert' and r.getter_expert_id:
                print 'm00893------------------------------------------'
                msg = u"%s, нужно ваше внимание." % (
                    r.sudo().getter_expert_id.name)
            elif action == 'end':
                print 'm00894------------------------------------------'
                msg = u"Работа закрыта"
            if msg != '':
                print 'm00895------------------------------------------'
                return r.message_post(body=msg)


class company(models.Model):
    _name = 'res.company'
    _inherit = 'res.company'
    task_count = fields.Integer(default=0)
    unic_id = fields.Char()

    @api.multi
    def _test(self):
        for r in self:
            r.is_user_company = self.env.user.company_id.id == r.id

    is_user_company = fields.Boolean(compute="_test")

    friends_ids = fields.Many2many(
        comodel_name="my_docs.friends"
    )

    def add_friend_wizard(self):
        view_id = self.env.ref('my_docs.friends_wizard').id
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'my_docs.friend_wizard',
            'view_id': view_id,
            'context': {'default_company_in_id': self.id}
        }


class task_log(models.Model):
    _name = 'my_docs.task_log'
    task_id = fields.Many2one('my_docs.task')
    local_task_id = fields.Many2one('my_docs.local_task_kz')
    # @api.multi
    # def _now(self):
    #     self.change_time = datetime.datetime.now()

    name = fields.Char()
    value_before = fields.Char(string='value_before')
    value_after = fields.Char(string='value_after')
    # change_time = fields.Datetime(compute='_now')
    change_user = fields.Char(string='change_user')

    @api.multi
    def return_change(self):
        for r in self:
            vals = {}
            before = r.value_before
            vals[str(r.name)] = before
            r.task_id.write(vals)

        view_id = self.env.ref('my_docs.task_form').id

        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'my_docs.task',
            'view_id': view_id,
            'target': 'current',
            'res_id': self.task_id.id,
        }


class supplement_free_form(models.Model):
    _name = 'my_docs.supplement_free_form'
    task_id = fields.Many2one('my_docs.task')
    value = fields.Text()


class counter(models.Model):
    _name = 'my_docs.counter'
    # users_ids = fields.One2many(
    #     comodel_name="res.users",
    #     inverse_name="users_busy_id",
    # )
    user_id = fields.Many2one(
        comodel_name="res.users"
    )

    @api.multi
    def _count_of_task(self):
        for r in self:
            count_of_task = random.randint(1, 30)

    count_of_task = fields.Integer(default=0, compute=_count_of_task)


class users(models.Model):
    _name = 'res.users'
    _inherit = 'res.users'
    _rec_name = "full_name"
    company_friends_ids = fields.Many2many(
        related='company_id.friends_ids'
    )

    @api.multi
    def _count_of_task(self):
        for r in self:
            result = self.env['my_docs.task'].search(
                [('getter_expert_id', '=', r.id), ('state', 'in', ['await_expert'])], count=True)
            # r.count_of_task=random.randint(1,30)
            r.count_of_task = result

    @api.depends('count_of_task')
    @api.multi
    def _full_name(self):
        for r in self:
            if r._context.get('compute_name'):
                r.full_name = "%s (%d Task)" % (r.name, r.count_of_task)
            else:
                r.full_name = "%s" % (r.name)

    def choose_expert(self, context=None):
        vals = {}
        vals['getter_expert_id'] = self.id
        if not self.partner_id in self.env['my_docs.task'].search([('id', '=', context.get('parent_id'))]).message_follower_ids.mapped('partner_id'):
            vals['message_follower_ids'] = [(0, 0, {
                'res_model': 'my_docs.task',
                'subtype_ids': [(6, 0, [1, 2])],
                'partner_id':self.partner_id.id})]
        task = self.env['my_docs.task'].search(
            [('id', '=', context.get('parent_id'))])
        task.write(vals)
        task.message_post(
            body=u"Данной задаче присвоен эксперт %s." % (self.name))
        return {}

    count_of_task = fields.Integer(compute='_count_of_task')
    full_name = fields.Char(compute='_full_name')


class friends(models.Model):
    _name = 'my_docs.friends'

    company_in_id = fields.Many2one(
        comodel_name="res.company"
    )
    company_out_unic_id = fields.Char()
    company_out_id = fields.Many2one(
        comodel_name="res.company"
    )


class friend_wizard(models.TransientModel):
    _name = 'my_docs.friend_wizard'
    company_out_unic_id = fields.Char()

    company_in_id = fields.Many2one(
        comodel_name="res.company"
    )
    company_out_id = fields.Many2one(
        comodel_name="res.company"
    )

    def add_friend(self):
        if self.company_out_unic_id:
            result = self.sudo().env['res.company'].search(
                [('unic_id', '=', self.company_out_unic_id)], limit=1)
            if not result:
                raise UserError("No company founded")
            if result.friends_ids.search([('company_out_unic_id', '=', self.company_out_unic_id)], limit=1):
                raise UserError("U have this company in friend yet!")

            vals = {}
            vals['company_in_id'] = self.company_in_id.id
            vals['company_out_id'] = result.id
            vals['company_out_unic_id'] = self.company_out_unic_id
            rr = self.env['my_docs.friends'].create(vals)

        resvals = {}
        resvals['friends_ids'] = [[4, rr.id]]
        self.env['res.company'].search(
            [('id', '=', self.company_in_id.id)]).write(resvals)


class report_page(models.Model):
    _name = 'my_docs.report_page'
    name = fields.Char()
    select_report =  fields.Selection(
        selection=[
                ('actual_task_for_person', 'actual_task_for_person'),
                ('task_of_date', 'task_of_date'),
                ('count_of_sender', 'count_of_sender')
        ]
    )

    @api.model
    def sql_select(self,select_text=''):
        cr = self.env.cr
        cr.execute(select_text)
        return cr.dictfetchall()
# cr.execute("SELECT to_char(create_date,'YYYY-MM-DD') as cr_d, count(*) as numofwork FROM public.my_docs_task  group by cr_d")
    @api.model
    def count_of_sender(self):
        result = self.sql_select(select_text="SELECT sender_company_id as cr_d, count(*) as numofwork FROM public.my_docs_task  group by cr_d")

        def chItem(item):
            sender_company = item['cr_d']
            if sender_company == None:
                sender_company = u'Не определенные'
            else:
                sender_company = self.env['res.company'].search(
                    [('id', '=', sender_company)], limit=1)[0].name
            return {
                "category": sender_company,
                "column-1": item['numofwork']
            }

        new_result = map(lambda a: chItem(a), result)

        test = 	{
        'otherDate' : {'divname':'my_chart'},
        'data': {
								"type": "pie",
					"angle": 12,
					"balloonText": "[[title]]<br><span style='font-size:14px'><b>[[value]]</b> ([[percents]]%)</span>",
					"depth3D": 15,
					"titleField": "category",
					"valueField": "column-1",
					"allLabels": [],
					"balloon": {},
					"legend": {
						"enabled": True,
						"align": "center",
						"markerType": "circle"
					},
					"titles": [],
					"dataProvider": new_result
                    # [
					# 	{
					# 		"category": "category 1",
					# 		"column-1": 8
					# 	},
					# 	{
					# 		"category": "category 2",
					# 		"column-1": 6
					# 	},
					# 	{
					# 		"category": "category 3",
					# 		"column-1": 2
					# 	}
					# ]
				}
                }

        return json.dumps(test)

    @api.model
    def task_of_date(self):
        result = self.sql_select(select_text="SELECT to_char(create_date,'YYYY-MM-DD') as cr_d, count(*) as numofwork FROM public.my_docs_task  group by cr_d")

        def chItem(item):
            return {
                "category": item['cr_d'],
                "column-1": item['numofwork'],
                "color": "#d0c398",
            }
        new_result = map(lambda a: chItem(a), result)
        print 'm00key------------------------------------------'
        print new_result
        test = 	{
        'otherDate' : {'divname':'my_chart'},
        'data': {
					"type": "serial",
					"categoryField": "category",
					"dataDateFormat": "YYYY-MM-DD",
					"startDuration": 1,
					"categoryAxis": {
						"gridPosition": "start",
						"parseDates": True
					},
					"chartCursor": {
						"enabled": True
					},
					"chartScrollbar": {
						"enabled": True
					},
					"trendLines": [],
					"graphs": [
						{
							"fillAlphas": 1,
							"id": "AmGraph-1",
							"title": "graph 1",
							"type": "column",
							"valueField": "column-1"
						}
					],
					"guides": [],
					"valueAxes": [
						{
							"id": "ValueAxis-1",
							"title": "Axis title"
						}
					],
					"allLabels": [],
					"balloon": {},
					"titles": [
						{
							"id": "Title-1",
							"size": 15,
							"text": "Chart Title"
						}
					],
					"dataProvider": [
						{
							"category": "2014-03-01",
							"column-1": 8
						},
						{
							"category": "2014-03-02",
							"column-1": 16
						},
						{
							"category": "2014-03-03",
							"column-1": 2
						},
						{
							"category": "2014-03-04",
							"column-1": 7
						},
						{
							"category": "2014-03-05",
							"column-1": 5
						},
						{
							"category": "2014-03-06",
							"column-1": 9
						},
						{
							"category": "2014-03-07",
							"column-1": 4
						},
						{
							"category": "2014-03-08",
							"column-1": 15
						},
						{
							"category": "2014-03-09",
							"column-1": 12
						},
						{
							"category": "2014-03-10",
							"column-1": 17
						},
						{
							"category": "2014-03-11",
							"column-1": 18
						},
						{
							"category": "2014-03-12",
							"column-1": 21
						},
						{
							"category": "2014-03-13",
							"column-1": 24
						},
						{
							"category": "2014-03-14",
							"column-1": 23
						},
						{
							"category": "2014-03-15",
							"column-1": 24
						}
					]
				}
                }

        return json.dumps(test)

    @api.model
    def actual_task_for_person(self):
        result = self.sql_select(select_text='SELECT getter_expert_id as expert_id, count(*) as numofwork FROM public.my_docs_task group by expert_id')

        def chItem(item):
            expert = item['expert_id']
            if expert == None:
                expert = u'Не определенные'
            else:
                expert = self.env['res.users'].search(
                    [('id', '=', expert)], limit=1)[0].name
            return {
                "category": expert,
                "column-1": item['numofwork']
            }
        new_result = map(lambda a: chItem(a), result)
        test = {
            'otherDate' : {'divname':'my_chart'},
            'data': {"type": "serial",
            "categoryField": "category",
            "startDuration": 1,
            "categoryAxis": {
                "gridPosition": "start"
            },
            "trendLines": [],
            "graphs": [
                {
                    "colorField": "color",
                    "fillAlphas": 1,
                    "id": "AmGraph-1",
                    "title": "graph 1",
                    "type": "column",
                    "valueField": "column-1",
                    "labelText": "[[value]]",
                    "labelPosition": "top",
                }
            ],
            "guides": [],
            "valueAxes": [
                {
                    "id": "ValueAxis-1",
                    "title": "Количество задач"
                }
            ],
            "allLabels": [],
            "balloon": {},
            "titles": [
                {
                    "id": "Title-1",
                    "size": 15,
                    "text": "Распределение задач"
                }
            ],
            "dataProvider": new_result}

        }
        return json.dumps(test)

    @api.model
    def getCalc(self, *args, **kwargs):
        return json.dumps(self.actual_task_for_person())
