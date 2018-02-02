# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, RedirectWarning, ValidationError

class set_expert_wizard(models.TransientModel):
    _name = 'my_docs.set_expert_wizard'

    task_id= fields.Many2one('my_docs.task', string="Tasks")
    getter_expert_id = fields.Many2one('res.users')
    @api.multi
    def _counter_ids(self):
        print 'm00010------------------------------------------'
        for r in self:
            result = self.env['res.users'].search([])
            print result
            r.user_ids =result

    counter_ids = fields.Many2many(
        comodel_name="my_docs.counter",compute=_counter_ids
    )
    user_ids = fields.Many2many(
        comodel_name="res.users",default=lambda self: self.env['res.users'].search([])
    )
    @api.multi
    def button_save(self):
        self.task_id.getter_expert_id=self.getter_expert_id
        vals={}
        vals['message_follower_ids'] = [(0,0,{
                  'res_model':'my_docs.task',
                  'subtype_ids': [(6, 0, [1,2])],
                  'partner_id':self.getter_expert_id.partner_id.id})]
        self.task_id.write(vals)
        self.task_id.message_post(body=u"Данной задаче присвоен эксперт %s." % (self.getter_expert_id.name))
        return {}


class new_task(models.TransientModel):
    _name = 'my_docs.new_task'
    name= fields.Char()
    type_task= fields.Selection(selection=[(
        'ss', 'ss'), ('ds', 'ds'), ('request', 'request')] )

    @api.multi
    def next(self):
        newr=self.env['my_docs.task'].create({'type_task':self.type_task})
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
            'res_id': newr.id,
            'res_model':'my_docs.task',
            'flags': {'initial_mode': 'edit'}
            }
