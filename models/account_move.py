from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    # Meter reading fields
    previous_reading = fields.Float(string="Previous Reading")
    new_reading = fields.Float(string="New Reading")
    actual_usage = fields.Float(
        string="Actual Usage", compute="_compute_actual_usage", store=True
    )
    unit_price = fields.Float(string="Unit Price", default=10.0)
    total_price = fields.Float(
        string="Total Price", compute="_compute_total_price", store=True
    )

    # Compute actual usage
    @api.depends("previous_reading", "new_reading")
    def _compute_actual_usage(self):
        for record in self:
            record.actual_usage = record.new_reading - record.previous_reading

    # Compute total price based on usage and unit price
    @api.depends("actual_usage", "unit_price")
    def _compute_total_price(self):
        for record in self:
            record.total_price = (
                record.actual_usage * record.unit_price if record.actual_usage else 0.0
            )

    # Action to view past readings
    def action_view_past_readings(self):
        return {
            "name": "Meter Reading History",
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "view_mode": "tree,form",
            "domain": [("partner_id", "=", self.partner_id.id)],
        }

    # Constraint to ensure valid usage values
    @api.constrains("actual_usage")
    def _check_usage_limit(self):
        for record in self:
            if record.actual_usage < 0:
                raise ValidationError(
                    "The new reading cannot be lower than the previous reading!"
                )
            elif record.actual_usage > 1000:
                raise ValidationError("Warning: Unusually high meter reading detected!")
