from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.fields import Char, Html, Selection, Text


SUPPORTED_FIELD_TYPES = (Char, Text, Html, Selection)
SUPPORTED_FIELD_TTYPES = {'char', 'text', 'html', 'selection'}


class DlntTranslationConfig(models.Model):
    _name = "dlnt.translation.config"
    _description = "Dynamic Field Translation Rule"
    _rec_name = "display_name"
    _order = "model_id, field_id"

    active = fields.Boolean(default=True)
    model_id = fields.Many2one(
        "ir.model",
        string="Model",
        required=True,
        help="Model that holds the target field.",
        ondelete="cascade",
    )
    field_id = fields.Many2one(
        "ir.model.fields",
        string="Field",
        required=True,
        help="Field that should expose multilingual values.",
        domain="[('model_id', '=', model_id), ('ttype', 'in', ['char', 'text', 'html', 'selection'])]",
        ondelete="cascade",
    )
    original_translate = fields.Boolean(
        string="Originally Translatable",
        readonly=True,
        help="Internal flag to restore the original field state on uninstall or when disabling the rule.",
    )
    display_name = fields.Char(
        compute="_compute_display_name",
        store=False,
    )

    _sql_constraints = [
        (
            "dlnt_translation_field_unique",
            "unique(field_id)",
            "A translation rule already exists for this field.",
        )
    ]

    @api.depends("model_id", "field_id")
    def _compute_display_name(self):
        for record in self:
            model = record.model_id.model or "?"
            field = record.field_id.name or "?"
            record.display_name = f"{model}.{field}" if record.model_id and record.field_id else _("Incomplete Rule")

    @api.constrains("field_id", "model_id")
    def _check_field_matches_model(self):
        for record in self:
            if record.field_id and record.model_id and record.field_id.model_id != record.model_id:
                raise ValidationError(
                    _("The selected field does not belong to the chosen model."),
                )
            if record.field_id and record.field_id.ttype not in SUPPORTED_FIELD_TTYPES:
                raise ValidationError(
                    _("Only Char, Text, HTML, or Selection fields can be enabled for translations."),
                )

    def _get_field_definition(self):
        self.ensure_one()
        if not self.model_id or not self.field_id:
            return None, None
        model_name = self.model_id.model
        if not model_name:
            return None, None
        try:
            model = self.env[model_name]
        except KeyError:
            return None, None
        field = model._fields.get(self.field_id.name)
        return model, field

    def _apply_active_state(self):
        for record in self:
            _, field = record._get_field_definition()
            if not field or not isinstance(field, SUPPORTED_FIELD_TYPES):
                continue
            if not getattr(field, "translate", False):
                field.translate = True
            if not record.field_id.translate:
                record.field_id.sudo().write({"translate": True})

    def _restore_original_state(self):
        for record in self:
            if record.original_translate:
                # Field was already translatable before we touched it.
                continue
            _, field = record._get_field_definition()
            if not field:
                continue
            if getattr(field, "translate", False):
                field.translate = False
            if record.field_id.translate:
                record.field_id.sudo().write({"translate": False})

    def _sync_translation_state(self):
        for record in self:
            if record.active:
                record._apply_active_state()
            else:
                record._restore_original_state()

    @api.model_create_multi
    def create(self, vals_list):
        prepared_vals = []
        fields_model = self.env["ir.model.fields"].sudo()
        for vals in vals_list:
            vals = dict(vals)
            field_id = vals.get("field_id")
            if field_id:
                field = fields_model.browse(field_id)
                if not field:
                    raise ValidationError(_("The selected field does not exist."))
                vals.setdefault("model_id", field.model_id.id)
                vals.setdefault("original_translate", bool(field.translate))
            prepared_vals.append(vals)
        records = super().create(prepared_vals)
        records._sync_translation_state()
        return records

    def write(self, vals):
        if any(key in vals for key in {"field_id", "model_id"}):
            # Revert current field to its original state before switching
            self._restore_original_state()
        res = super().write(vals)
        if "field_id" in vals:
            for record in self:
                if record.field_id:
                    super(DlntTranslationConfig, record.sudo()).write(
                        {"original_translate": bool(record.field_id.translate)}
                    )
        self._sync_translation_state()
        return res

    def unlink(self):
        self._restore_original_state()
        return super().unlink()

    def toggle_active(self):
        active_records = self.filtered("active")
        inactive_records = self - active_records
        if active_records:
            active_records.write({"active": False})
        if inactive_records:
            inactive_records.write({"active": True})
