from fastapi.requests import Request
from sqladmin import ModelView
from markupsafe import Markup

from app.db.models import DBSettings
from app.core.common import format_datetime_msk
from app.admin.utils import add_css_styles


class SettingsAdmin(ModelView, model=DBSettings):
    name = "Настройка"
    name_plural = "Настройки"
    icon = "fa-solid fa-gear"

    column_labels = {
        "id": "ID",
        "preset_base_price": "Базовая цена пресета до 17:00",
        "preset_base_price_evening": "Базовая цена пресета после 17:00",
        "strength_added_price": "Добавочная цена крепости 9+",
        "liquids_image_url": "URL изображения жидкостей",
        "bowls_image_url": "URL изображения чаш",
        "created_at": "Дата создания",
        "updated_at": "Дата обновления",
    }

    column_list = [
        DBSettings.id,
        DBSettings.preset_base_price,
        DBSettings.preset_base_price_evening,
        DBSettings.strength_added_price,
        DBSettings.liquids_image_url,
        DBSettings.bowls_image_url,
        DBSettings.created_at,
        DBSettings.updated_at,
    ]

    column_searchable_list = [DBSettings.preset_base_price]
    column_sortable_list = [
        DBSettings.id,
        DBSettings.preset_base_price,
        DBSettings.preset_base_price_evening,
        DBSettings.created_at
    ]
    column_default_sort = [(DBSettings.id, False)]

    form_create_rules = [
        "preset_base_price",
        "preset_base_price_evening",
        "strength_added_price",
        "liquids_image_url",
        "bowls_image_url"
    ]
    form_edit_rules = [
        "preset_base_price",
        "preset_base_price_evening",
        "strength_added_price",
        "liquids_image_url",
        "bowls_image_url"
    ]

    form_args = {
        "preset_base_price": {
            "label": "Базовая цена пресета до 17:00",
            "description": "Базовая цена для расчета стоимости пресетов с 12:00 до 17:00",
            "render_kw": {"type": "number", "step": "1", "min": "0", "class": "form-control"}
        },
        "preset_base_price_evening": {
            "label": "Базовая цена пресета после 17:00",
            "description": "Базовая цена для расчета стоимости пресетов с 17:00 до 12:00",
            "render_kw": {"type": "number", "step": "1", "min": "0", "class": "form-control"}
        },
        "strength_added_price": {
            "label": "Добавочная цена крепости 8+",
            "description": "Добавляет к сумме заказа сумму за крепость 9+",
            "render_kw": {"type": "number", "step": "1", "min": "0", "class": "form-control"}
        },
        "liquids_image_url": {
            "label": "URL изображения жидкостей",
            "description": "Ссылка на изображение для раздела жидкостей",
            "render_kw": {"class": "form-control", "placeholder": "https://example.com/image.jpg"}
        },
        "bowls_image_url": {
            "label": "URL изображения чаш",
            "description": "Ссылка на изображение для раздела чаш",
            "render_kw": {"class": "form-control", "placeholder": "https://example.com/image.jpg"}
        }
    }

    def _base_price_formatter(m, a):
        return f"{m.preset_base_price:.2f} ₽"

    def _base_price_evening_formatter(m, a):
        return f"{m.preset_base_price_evening:.2f} ₽"

    def _added_price_formatter(m, a):
        return f"{m.strength_added_price:.2f} ₽"

    def _liquids_image_formatter(m, a):
        if m.liquids_image_url:
            return Markup(f'<a href="{m.liquids_image_url}" target="_blank">Просмотр</a>')
        return "-"

    def _bowls_image_formatter(m, a):
        if m.bowls_image_url:
            return Markup(f'<a href="{m.bowls_image_url}" target="_blank">Просмотр</a>')
        return "-"

    column_formatters = {
        DBSettings.preset_base_price: _base_price_formatter,
        DBSettings.preset_base_price_evening: _base_price_evening_formatter,
        DBSettings.strength_added_price: _added_price_formatter,
        DBSettings.liquids_image_url: _liquids_image_formatter,
        DBSettings.bowls_image_url: _bowls_image_formatter,
        "created_at": lambda m, a: format_datetime_msk(m.created_at),
        "updated_at": lambda m, a: format_datetime_msk(m.updated_at)
    }

    column_formatters_detail = column_formatters

    async def on_before_form(self, request: Request, obj=None):
        request.state.custom_css = add_css_styles()
        return await super().on_before_form(request, obj)

    can_create = False
    can_edit = True
    can_delete = False
    can_view_details = True