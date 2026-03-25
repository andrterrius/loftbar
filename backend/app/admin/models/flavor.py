from fastapi.requests import Request

from sqladmin import ModelView
from markupsafe import Markup

from app.db.models import DBFlavor
from app.core.common import format_datetime_msk
from app.admin.utils import add_css_styles, add_image_preview_js

class FlavorAdmin(ModelView, model=DBFlavor):
    name = "Вкус"
    name_plural = "Вкусы"
    icon = "fa-solid fa-ice-cream"

    column_labels = {
        "name": "Название",
        "brand": "Бренд",
        "category": "Категория",
        "description": "Описание",
        "is_available": "В наличии",
        "hex_color": "Цвет",
        "image_url": "Изображение",
        "created_at": "Дата создания",
        "updated_at": "Дата обновления",
        "presets": "Пресеты",
        "preset_flavors": "Проценты вкусов"
    }

    column_list = [
        DBFlavor.name,
        DBFlavor.brand,
        DBFlavor.category,
        DBFlavor.description,
        DBFlavor.is_available,
        DBFlavor.image_url,
        DBFlavor.hex_color,
        DBFlavor.created_at
    ]

    column_searchable_list = [
        DBFlavor.name,
        DBFlavor.brand,
        DBFlavor.category,
        DBFlavor.description
    ]
    column_sortable_list = [
        DBFlavor.is_available,
        DBFlavor.created_at]
    column_default_sort = [(DBFlavor.is_available, True), (DBFlavor.updated_at, True)]

    form_create_rules = [
        "name", "brand", "category", "description", "is_available", "hex_color", "image_url"
    ]
    form_edit_rules = [
        "name", "brand", "category", "description", "is_available", "hex_color", "image_url"
    ]

    form_args = {
        "name": {
            "label": "Название",
            "description": "Название вкуса",
            "render_kw": {"placeholder": "Например: Клубника", "class": "form-control"}
        },
        "brand": {
            "label": "Бренд",
            "description": "Производитель",
            "render_kw": {"placeholder": "Например: Dinner Lady", "class": "form-control"}
        },
        "category": {
            "label": "Категория",
            "description": "Фруктовый, десертный, мятный и т.д.",
            "render_kw": {"placeholder": "фруктовый/десертный/мятный", "class": "form-control"}
        },
        "description": {
            "label": "Описание",
            "description": "Red orange и т.д.",
            "render_kw": {"placeholder": "Red orange...", "class": "form-control"}
        },
        "is_available": {
            "label": "В наличии",
            "description": "Доступен ли для заказа",
            "render_kw": {"class": "form-check-input"}
        },
        "hex_color": {
            "label": "Цвет",
            "description": "Выберите цвет для вкуса",
            "render_kw": {"type": "color", "class": "form-control form-control-color",
                          "style": "width: 60px; height: 40px; padding: 0;"}
        },
        "image_url": {
            "label": "URL изображения",
            "description": "Ссылка на картинку",
            "render_kw": {"type": "url", "class": "form-control", "placeholder": "https://example.com/image.jpg"}
        }
    }

    form_widget_args = {
        "is_available": {"class": "form-check-input"}
    }

    def _color_formatter(m, a):
        if m.hex_color:
            return Markup(
                f'<div style="background-color: {m.hex_color}; width: 30px; height: 20px; border-radius: 4px; border: 1px solid #ddd;"></div>'
            )
        return Markup('<span style="color: #999;">—</span>')

    def _image_formatter(m, a):
        if m.image_url:
            return Markup(
                f'<img src="{m.image_url}" style="max-width: 50px; max-height: 50px; border-radius: 4px; object-fit: cover;" onerror="this.style.display=\'none\'">'
            )
        return Markup('<span style="color: #999;">—</span>')

    def _available_formatter(m, a):
        return Markup("✅ Да") if m.is_available else Markup("❌ Нет")

    column_formatters = {
        DBFlavor.hex_color: _color_formatter,
        DBFlavor.is_available: _available_formatter,
        DBFlavor.image_url: _image_formatter,
        "created_at": lambda m, a: format_datetime_msk(m.created_at),
        "updated_at": lambda m, a: format_datetime_msk(m.updated_at)
    }
    column_formatters_detail = column_formatters

    async def on_before_form(self, request: Request, obj=None):
        request.state.custom_css = add_css_styles()
        request.state.custom_js = add_image_preview_js()
        return await super().on_before_form(request, obj)
