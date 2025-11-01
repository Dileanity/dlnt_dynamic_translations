# DLNT Dynamic Field Translations

Enable translation toggles (e.g., EN / EL) on any existing Char, Text, HTML, or Selection field without modifying the original module. Administrators can declaratively pick which fields should expose multilingual values and the module updates both the ORM registry and field metadata for you.

## Key Features
- Activate translations on existing fields across any installed model.
- Persist the original state so uninstalls or deactivations are safe.
- Works instantly after saving; no need to patch source modules.
- Supports Char, Text, HTML, and Selection field types.
- Dedicated configuration menu for system administrators.

## Installation
1. Copy the module folder `dlnt_dynamic_translations` into your Odoo Addons path.
2. Update the Apps list and search for **Dynamic Field Translations**.
3. Install the module.

## Configuration & Usage
1. Open *Settings → Dynamic Translations → Field Rules*.
2. Create a new record and pick the target model and field. Only supported field types will be available.
3. Save and keep the rule active. The inline language switcher appears immediately on that field across the system.
4. Archive a rule to revert to the original behaviour while preserving your configuration for later reuse.

## Compatibility
- Tested with Odoo 18.0 and 19.0 (Community & Enterprise).
- Earlier versions may work but are not officially verified.

## License
This module is released under the **Odoo Proprietary License v1.0 (OPL-1)**. See `LICENSE` for full terms. The app is distributed at no cost by **DILEANITY G.P.**

## Support
For assistance or customisations, reach out at **support@dileanity.com**.
