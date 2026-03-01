from fastapi.requests import Request
from sqladmin import ModelView
from markupsafe import Markup

from app.db.models import DBSettings
from app.admin.utils import add_css_styles


class SettingsAdmin(ModelView, model=DBSettings):
    name = "Настройка"
    name_plural = "Настройки"
    icon = "fa-solid fa-gear"

    column_labels = {
        "id": "ID",
        "preset_base_price": "Базовая цена пресета",
        "created_at": "Дата создания",
        "updated_at": "Дата обновления",
    }

    column_list = [
        DBSettings.id,
        DBSettings.preset_base_price,
        DBSettings.created_at,
        DBSettings.updated_at,
    ]

    column_searchable_list = [DBSettings.preset_base_price]
    column_sortable_list = [DBSettings.id, DBSettings.preset_base_price, DBSettings.created_at]
    column_default_sort = [(DBSettings.id, False)]

    form_create_rules = [
        "preset_base_price"
    ]
    form_edit_rules = [
        "preset_base_price"
    ]

    form_args = {
        "preset_base_price": {
            "label": "Базовая цена пресета",
            "description": "Базовая цена для расчета стоимости пресетов",
            "render_kw": {"type": "number", "step": "1", "min": "0", "class": "form-control"}
        }
    }

    def _price_formatter(m, a):
        return f"{m.preset_base_price:.2f} ₽"

    column_formatters = {
        DBSettings.preset_base_price: _price_formatter
    }

    async def on_before_form(self, request: Request, obj=None):
        request.state.custom_css = add_css_styles()
        return await super().on_before_form(request, obj)

    can_create = False
    can_edit = True
    can_delete = False
    can_view_details = True