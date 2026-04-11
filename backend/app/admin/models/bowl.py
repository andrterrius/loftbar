from fastapi.requests import Request

from sqladmin import ModelView
from markupsafe import Markup

from app.db.models import DBBowl
from app.core.common import format_datetime_msk
from app.admin.utils import add_css_styles

class BowlAdmin(ModelView, model=DBBowl):
    name = "Чаша"
    name_plural = "Чаши"
    icon = "fa-solid fa-bowl-food"

    column_labels = {
        "name": "Название",
        "category": "Категория",
        "price": "Цена",
        "added_price": "Добавочная дневная цена",
        "added_price_evening": "Добавочная вечерняя цена",
        "is_available": "В наличии",
        "icon": "Иконка",
        "image_url": "Изображение",
        "created_at": "Дата создания",
        "updated_at": "Дата обновления",
        "presets": "Пресеты"
    }

    column_list = [
        DBBowl.name,
        DBBowl.category,
        DBBowl.price,
        DBBowl.added_price,
        DBBowl.added_price_evening,
        DBBowl.is_available,
        DBBowl.image_url,
        DBBowl.created_at,
    ]

    column_searchable_list = [DBBowl.name, DBBowl.category]
    column_sortable_list = [DBBowl.name, DBBowl.price, DBBowl.added_price, DBBowl.added_price_evening, DBBowl.created_at]
    column_default_sort = [(DBBowl.is_available, True), (DBBowl.updated_at, True)]

    form_create_rules = [
        "name", "category", "price", "added_price", "added_price_evening", "is_available", "icon", "image_url"
    ]
    form_edit_rules = [
        "name", "category", "price", "added_price", "added_price_evening", "is_available", "icon", "image_url"
    ]

    form_args = {
        "name": {
            "label": "Название",
            "description": "Название чаши",
            "render_kw": {"placeholder": "Например: Стандартная чаша", "class": "form-control"}
        },
        "category": {
            "label": "Категория",
            "description": "Например: стандартная, премиум",
            "render_kw": {"placeholder": "стандартная/премиум", "class": "form-control"}
        },
        "price": {
            "label": "Цена",
            "description": "Цена в рублях",
            "render_kw": {"type": "number", "step": "0.01", "class": "form-control"}
        },
        "added_price": {
            "label": "Добавочная дневная цена",
            "description": "Дополнительная цена для дневного времени",
            "render_kw": {"type": "number", "step": "0.01", "class": "form-control"}
        },
        "added_price_evening": {
            "label": "Добавочная вечерняя цена",
            "description": "Дополнительная цена для вечернего времени",
            "render_kw": {"type": "number", "step": "0.01", "class": "form-control"}
        },
        "is_available": {
            "label": "В наличии",
            "description": "Доступна ли для заказа",
            "render_kw": {"class": "form-check-input"}
        },
        "icon": {
            "label": "Иконка",
            "description": "Эмодзи иконки или любой текст",
            "render_kw": {"placeholder": "🥥", "class": "form-control"}
        },
        "image_url": {
            "label": "URL изображения",
            "description": "Ссылка на изображение чаши",
            "render_kw": {"placeholder": "https://example.com/bowl-image.jpg", "class": "form-control", "type": "url"}
        }
    }

    form_widget_args = {
        "is_available": {"class": "form-check-input"}
    }

    def _price_formatter(m, a):
        return f"{m.price:.2f} ₽"

    def _added_price_formatter(m, a):
        return f"{m.added_price:.2f} ₽" if m.added_price else "0.00 ₽"

    def _added_price_evening_formatter(m, a):
        return f"{m.added_price_evening:.2f} ₽" if m.added_price_evening else "0.00 ₽"

    def _available_formatter(m, a):
        return Markup("✅ Да") if m.is_available else Markup("❌ Нет")

    def _image_formatter(m, a):
        if m.image_url:
            return Markup(f'<img src="{m.image_url}" alt="{m.name}" style="max-width: 50px; max-height: 50px; border-radius: 4px;">')
        return Markup("Нет изображения")

    column_formatters = {
        DBBowl.price: _price_formatter,
        DBBowl.added_price: _added_price_formatter,
        DBBowl.added_price_evening: _added_price_evening_formatter,
        DBBowl.is_available: _available_formatter,
        DBBowl.image_url: _image_formatter,
        "created_at": lambda m, a: format_datetime_msk(m.created_at),
        "updated_at": lambda m, a: format_datetime_msk(m.updated_at)
    }

    column_formatters_detail = column_formatters

    async def on_before_form(self, request: Request, obj=None):
        request.state.custom_css = add_css_styles()
        return await super().on_before_form(request, obj)

    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True