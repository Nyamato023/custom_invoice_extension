{
    "name": "Custom Invoice Extension",
    "version": "1.0",
    "summary": "Adds additional columns to Odoo invoices.",
    "description": "Extends the Accounting module to include Previous, New, and Actual meter readings.",
    "category": "Accounting",
    "author": "SImba",
    "depends": ["account"],
    "data": ["views/invoice_view.xml", "reports/invoice_report.xml"],
    "installable": True,
    "application": False,
}
