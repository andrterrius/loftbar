from fastapi.requests import Request
from sqladmin import ModelView
from markupsafe import Markup
from sqlalchemy import Integer

from app.db.models import DBFlavorCategory
from app.core.common import format_datetime_msk
from app.admin.utils import add_css_styles, add_image_preview_js


class FlavorCategoryAdmin(ModelView, model=DBFlavorCategory):
    name = "Категория вкуса"
    name_plural = "Категории вкусов"
    icon = "fa-solid fa-tags"

    column_labels = {
        "id": "ID",
        "name": "Название категории",
        "flavors": "Вкусы в категории",
        "order": "Порядок",
        "created_at": "Дата создания",
        "updated_at": "Дата обновления"
    }

    # Список отображаемых колонок в таблице
    column_list = [
        DBFlavorCategory.name,
        DBFlavorCategory.order,
        DBFlavorCategory.flavors,
        DBFlavorCategory.created_at,
        DBFlavorCategory.updated_at
    ]

    # Поиск по названию категории
    column_searchable_list = [DBFlavorCategory.name]

    # Сортировка
    column_sortable_list = [
        DBFlavorCategory.name,
        DBFlavorCategory.order,
        DBFlavorCategory.created_at,
        DBFlavorCategory.updated_at
    ]

    # Сортировка по умолчанию (по полю order)
    column_default_sort = [(DBFlavorCategory.order, False)]

    # Поля для создания и редактирования
    form_create_rules = ["name", "order"]
    form_edit_rules = ["name", "order"]

    # Настройка формы
    form_args = {
        "name": {
            "label": "Название категории",
            "description": "Например: Фруктовые, Ягодные, Десертные, Мятные",
            "render_kw": {
                "placeholder": "Введите название категории вкуса",
                "class": "form-control"
            }
        },
        "order": {
            "label": "Порядковый номер",
            "description": "Чем меньше число, тем выше позиция в списке",
            "render_kw": {
                "placeholder": "Например: 1, 2, 3...",
                "class": "form-control",
                "type": "number"
            }
        }
    }

    # Форматтер для дат
    def _created_at_formatter(m, a):
        return format_datetime_msk(m.created_at)

    def _updated_at_formatter(m, a):
        return format_datetime_msk(m.updated_at)

    # Применение форматтеров
    column_formatters = {
        DBFlavorCategory.created_at: _created_at_formatter,
        DBFlavorCategory.updated_at: _updated_at_formatter
    }

    # Детальное отображение использует те же форматтеры
    column_formatters_detail = column_formatters

    # Дополнительные настройки
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    # Экспорт данных
    can_export = True
    export_types = ["csv", "json"]

    async def on_before_form(self, request: Request, obj=None):
        """Добавляем CSS и JS для улучшения интерфейса"""
        request.state.custom_css = add_css_styles()
        request.state.custom_js = add_image_preview_js()
        return await super().on_before_form(request, obj)