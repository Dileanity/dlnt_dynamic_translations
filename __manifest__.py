{
    'name': 'Dynamic Field Translations',
    'version': '19.0.1.0.0',
    'summary': 'Enable translations dynamically on existing fields without modifying source modules.',
    'description': """
        Dynamic Field Translations
        =========================

        Turn translation support on for existing text fields across any model without
        touching the original module source code. Administrators can opt-in specific
        fields and instantly expose the inline translation UI (e.g., EN/EL toggle).
    """,
    'author': 'DILEANITY G.P.',
    'website': 'https://www.dileanity.com',
    'maintainer': 'DILEANITY G.P.',
    'support': 'support@dileanity.com',
    'license': 'OPL-1',
    'price': 0.0,
    'currency': 'EUR',
    'category': 'Tools',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/translation_config_views.xml',
    ],
    'post_init_hook': 'post_init_apply_translations',
    'post_load': 'post_load_apply_translations',
    'uninstall_hook': 'uninstall_reset_translations',
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': ['static/description/icon.png'],
}
