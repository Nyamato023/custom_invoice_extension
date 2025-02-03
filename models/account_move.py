from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = "account.move.line"

    # Meter reading fields
    previous_reading = fields.Float(
        string="Previous Reading",
        help="Last recorded meter reading from the previous invoice.",
    )
    new_reading = fields.Float(
        string="New Reading", help="Current month's meter reading."
    )
    actual_usage = fields.Float(
        string="Actual Usage",
        compute="_compute_actual_usage",
        store=True,
        help="Difference between New and Previous readings.",
    )
    quantity = fields.Float(
        string="Quantity",
        compute="_compute_quantity",
        store=True,
        help="Quantity to be billed, same as Actual Usage.",
    )
    unit_price = fields.Float(
        string="Unit Price", default=10.0, help="Price per unit of usage."
    )
    total_price = fields.Float(
        string="Total Price",
        compute="_compute_total_price",
        store=True,
        help="Total price based on quantity and unit price.",
    )

    # Compute actual usage
    @api.depends("previous_reading", "new_reading")
    def _compute_actual_usage(self):
        for record in self:
            if record.previous_reading and record.new_reading:
                record.actual_usage = max(
                    record.new_reading - record.previous_reading, 0
                )
            else:
                record.actual_usage = 0

    # Compute quantity (same as actual usage)
    @api.depends("actual_usage")
    def _compute_quantity(self):
        for record in self:
            record.quantity = record.actual_usage

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
