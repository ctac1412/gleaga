# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, RedirectWarning, ValidationError

class set_expert_wizard(models.TransientModel):
    _name = 'my_docs.set_expert_wizard'

    def _get_default_task(self):
        return self.env['my_docs.task'].browse(self.env.context.get('active_ids'))

    task_ids= fields.Many2many('my_docs.task', string="Tasks", default=_get_default_task)
    expert_id = fields.Many2one('res.users', string="exper_id")
    @api.multi
    def _set_experts(self):
        for r in self:
            if r.task_ids:
                for c in r.task_ids:
                    c.expert_id = self.expert_id


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
