from fastapi.requests import Request

from sqladmin import ModelView
from markupsafe import Markup

from app.db.models import DBLiquid

from app.admin.utils import add_css_styles, add_image_preview_js

class LiquidAdmin(ModelView, model=DBLiquid):
    name = "Жидкость"
    name_plural = "Жидкости"
    icon = "fa-solid fa-flask"

    column_labels = {
        "name": "Название",
        "category": "Категория",
        "price": "Цена",
        "is_available": "В наличии",
        "hex_color": "Цвет",
        "created_at": "Дата создания",
        "updated_at": "Дата обновления",
        "presets": "Пресеты"
    }

    column_list = [
        DBLiquid.name,
        DBLiquid.category,
        DBLiquid.price,
        DBLiquid.is_available,
        DBLiquid.created_at
    ]

    column_searchable_list = [DBLiquid.name, DBLiquid.category]
    column_sortable_list = [DBLiquid.name, DBLiquid.price, DBLiquid.created_at]
    column_default_sort = [(DBLiquid.is_available, True), (DBLiquid.updated_at, True)]

    form_create_rules = [
        "name", "category", "price", "is_available", "description",
        "hex_color"
    ]
    form_edit_rules = [
        "name", "category", "price", "is_available", "description",
        "hex_color"
    ]

    form_args = {
        "name": {
            "label": "Название",
            "description": "Название жидкости",
            "render_kw": {"placeholder": "Например: Малиновый лимонад", "class": "form-control"}
        },
        "category": {
            "label": "Категория",
            "description": "Например: классика, премиум",
            "render_kw": {"placeholder": "классика/премиум", "class": "form-control"}
        },
        "price": {
            "label": "Цена",
            "description": "Цена в рублях",
            "render_kw": {"type": "number", "step": "0.01", "class": "form-control"}
        },
        "is_available": {
            "label": "В наличии",
            "description": "Доступна ли для заказа",
            "render_kw": {"class": "form-check-input"}
        },
        "hex_color": {
            "label": "Цвет",
            "description": "Выберите цвет для жидкости",
            "render_kw": {"type": "color", "class": "form-control form-control-color",
                          "style": "width: 60px; height: 40px; padding: 0;"}
        }
    }

    form_widget_args = {
        "is_available": {"class": "form-check-input"}
    }

    def _price_formatter(m, a):
        return f"{m.price:.2f} ₽"

    def _color_formatter(m, a):
        if m.hex_color:
            return Markup(
                f'<div style="background-color: {m.hex_color}; width: 30px; height: 20px; border-radius: 4px; border: 1px solid #ddd;"></div>'
            )
        return Markup('<span style="color: #999;">—</span>')

    def _available_formatter(m, a):
        return Markup("✅ Да") if m.is_available else Markup("❌ Нет")

    column_formatters = {
        DBLiquid.price: _price_formatter,
        DBLiquid.hex_color: _color_formatter,
        DBLiquid.is_available: _available_formatter
    }

    async def on_before_form(self, request: Request, obj=None):
        request.state.custom_css = add_css_styles()
        request.state.custom_js = add_image_preview_js()
        return await super().on_before_form(request, obj)
