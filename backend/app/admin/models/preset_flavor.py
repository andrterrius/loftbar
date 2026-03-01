from fastapi.requests import Request
from sqladmin import ModelView
from markupsafe import Markup
from sqlalchemy import Numeric
import uuid as uuid_pkg

from app.db.models import DBPresetFlavor
from app.admin.utils import add_css_styles


class PresetFlavorAdmin(ModelView, model=DBPresetFlavor):
    name = "Проценты вкусов пресета"
    name_plural = "Проценты вкусов пресетов"
    icon = "fa-solid fa-percent"

    column_labels = {
        "preset_id": "ID пресета",
        "flavor_id": "ID вкуса",
        "preset": "Пресет",
        "flavor": "Вкус",
        "percent": "Процент",
    }

    column_list = [
        DBPresetFlavor.preset,
        DBPresetFlavor.flavor,
        DBPresetFlavor.percent,
    ]

    column_searchable_list = []
    column_sortable_list = [DBPresetFlavor.percent]
    column_default_sort = [(DBPresetFlavor.percent, True)]

    form_create_rules = [
        "preset", "flavor", "percent"
    ]
    form_edit_rules = [
        "preset", "flavor", "percent"
    ]

    def _percent_formatter(m, a):
        return Markup(f"{m.percent}%")

    def _preset_formatter(m, a):
        if m.preset:
            return Markup(f"<span title='{m.preset.id}'>{m.preset.name}</span>")
        return "—"

    column_formatters = {
        DBPresetFlavor.percent: _percent_formatter,
        DBPresetFlavor.preset: _preset_formatter,
    }

    column_formatters_detail = column_formatters

    async def on_before_form(self, request: Request, obj=None):
        request.state.custom_css = add_css_styles()
        return await super().on_before_form(request, obj)

    can_create = False
    can_edit = False
    can_delete = False
    can_view_details = True