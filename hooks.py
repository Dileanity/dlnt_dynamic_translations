"""Hooks for Dynamic Field Translations module."""

from odoo import SUPERUSER_ID, api


def _apply_configs(env):
    """Apply translation flags according to saved configurations."""
    configs = env["dlnt.translation.config"].sudo().search([])
    for config in configs:
        if config.active:
            config._apply_active_state()
        else:
            config._restore_original_state()


def post_init_apply_translations(cr, registry):
    """Executed right after module installation."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    _apply_configs(env)


def post_load_apply_translations(cr, registry):
    """Executed on every server restart once the registry is ready."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    _apply_configs(env)


def uninstall_reset_translations(cr, registry):
    """Best-effort reset of toggled fields during uninstall."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    configs = env["dlnt.translation.config"].sudo().search([])
    for config in configs:
        config._restore_original_state()
