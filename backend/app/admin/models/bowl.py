from fastapi.requests import Request

from sqladmin import ModelView
from markupsafe import Markup

from app.db.models import DBBowl

from app.admin.utils import add_css_styles

class BowlAdmin(ModelView, model=DBBowl):
    name = "Чаша"
    name_plural = "Чаши"
    icon = "fa-solid fa-bowl-food"

    column_labels = {
        "name": "Название",
        "category": "Категория",
        "price": "Цена",
        "is_available": "Доступна",
        "icon": "Иконка",
        "created_at": "Дата создания",
        "updated_at": "Дата обновления",
        "presets": "Пресеты"
    }

    column_list = [
        DBBowl.name,
        DBBowl.category,
        DBBowl.price,
        DBBowl.is_available,
        DBBowl.created_at,
    ]

    column_searchable_list = [DBBowl.name, DBBowl.category]
    column_sortable_list = [DBBowl.name, DBBowl.price, DBBowl.created_at]
    column_default_sort = [(DBBowl.is_available, True), (DBBowl.updated_at, True)]

    form_create_rules = [
        "name", "category", "price", "is_available", "icon"
    ]
    form_edit_rules = [
        "name", "category", "price", "is_available", "icon"
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
        "is_available": {
            "label": "В наличии",
            "description": "Доступна ли для заказа",
            "render_kw": {"class": "form-check-input"}
        },
        "icon": {
            "label": "Иконка",
            "description": "Название иконки из библиотеки Font Awesome",
            "render_kw": {"placeholder": "fa-solid fa-bowl-food", "class": "form-control"}
        }
    }

    form_widget_args = {
        "is_available": {"class": "form-check-input"}
    }

    def _price_formatter(m, a):
        return f"{m.price:.2f} ₽"

    def _available_formatter(m, a):
        return Markup("✅ Да") if m.is_available  else Markup("❌ Нет")

    column_formatters = {
        DBBowl.price: _price_formatter,
        DBBowl.is_available: _available_formatter
    }

    async def on_before_form(self, request: Request, obj=None):
        request.state.custom_css = add_css_styles()
        return await super().on_before_form(request, obj)

    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True