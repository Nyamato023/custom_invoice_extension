from odoo import models, fields


class AccountMove(models.Model):
    _inherit = "account.move"

    previous_reading = fields.Float(string="Previous Reading")
    new_reading = fields.Float(string="New Reading")
    actual_usage = fields.Float(
        string="Actual Usage", compute="_compute_actual_usage", store=True
    )

    @api.depends("previous_reading", "new_reading")
    def _compute_actual_usage(self):
        for record in self:
            record.actual_usage = record.new_reading - record.previous_reading
