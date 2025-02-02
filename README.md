This module extends the Odoo Accounting module by adding:
- Previous meter reading
- New meter reading
- Actual usage computed field
- Automatic price calculation
- Meter reading history
- Warning system for abnormal usage

1. After extracting the .zip file Copy `custom_invoice_extension` folder to your Odoo addons directory:
   ```bash
   cp -r custom_invoice_extension /path/to/odoo/addons/
   ```
2. Restart Odoo:
   ```bash
   sudo systemctl restart odoo
   ```
   Or if running Odoo manually:
   ```bash
   ./odoo-bin --addons-path=/path/to/odoo/addons/ -u custom_invoice_extension
   ```
3. Install the module via the Apps menu:
   - Go to **Apps**
   - Search for "Custom Invoice Extension"
   - Click **Install**

## Dependencies
- Odoo Accounting Module

## Github Repo:
[Nyamato023](https://github.com/Nyamato023/custom_invoice_extension.git)
