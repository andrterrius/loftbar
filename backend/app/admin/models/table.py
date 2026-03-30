from fastapi.requests import Request
from sqladmin import ModelView
from markupsafe import Markup

from app.db.models import DBTable
from app.core.common import format_datetime_msk
from app.admin.utils import add_css_styles


class TableAdmin(ModelView, model=DBTable):
    name = "Столик"
    name_plural = "Столики"
    icon = "fa-solid fa-chair"

    column_labels = {
        "id": "ID",
        "number": "Номер",
        "name": "Название",
        "seats": "Количество мест",
        "is_available": "Доступен",
        "location": "Расположение",
        "description": "Описание",
        "created_at": "Дата создания",
        "updated_at": "Дата обновления",
        "table_link": "Ссылка на столик"
    }

    column_list = [
        DBTable.number,
        DBTable.name,
        "table_link",
        DBTable.seats,
        DBTable.is_available,
        DBTable.location,
        DBTable.created_at,
    ]

    column_details_list = column_list + [
        DBTable.updated_at,
        DBTable.description,
    ]

    column_searchable_list = [DBTable.number, DBTable.name, DBTable.location]
    column_sortable_list = [
        DBTable.number,
        DBTable.seats,
        DBTable.location,
        DBTable.created_at,
        DBTable.is_available
    ]
    column_default_sort = [(DBTable.number, False)]

    form_create_rules = [
        "number", "name", "seats", "is_available", "location", "description"
    ]
    form_edit_rules = [
        "number", "name", "seats", "is_available", "location", "description"
    ]

    form_args = {
        "number": {
            "label": "Номер столика",
            "description": "Уникальный номер столика",
            "render_kw": {"type": "number", "min": "1", "step": "1", "class": "form-control", "required": "required"}
        },
        "name": {
            "label": "Название",
            "description": "Необязательное название столика (например, 'У окна', 'VIP')",
            "render_kw": {"placeholder": "Например: У окна", "class": "form-control"}
        },
        "seats": {
            "label": "Количество мест",
            "description": "Вместимость столика",
            "render_kw": {"type": "number", "min": "1", "max": "20", "step": "1", "class": "form-control",
                          "required": "required"}
        },
        "is_available": {
            "label": "Доступен",
            "description": "Доступен ли столик",
            "render_kw": {"class": "form-check-input"}
        },
        "location": {
            "label": "Расположение",
            "description": "Где находится столик (зал, веранда, VIP и т.д.)",
            "render_kw": {"placeholder": "Например: Основной зал", "class": "form-control"}
        },
        "description": {
            "label": "Описание",
            "description": "Дополнительная информация о столике",
            "render_kw": {"placeholder": "Особенности столика, примечания...", "class": "form-control", "rows": 3}
        }
    }

    form_widget_args = {
        "is_available": {"class": "form-check-input"},
        "description": {"rows": 3}
    }

    def _available_formatter(m, a):
        return Markup("✅ Да") if m.is_available else Markup("❌ Нет")

    def _table_link_formatter(m, a):
        if m.id:
            # Используем JavaScript для получения текущего домена
            # Ссылка будет создана на клиентской стороне
            return Markup(f'''
                <script>
                    (function() {{
                        var link = document.createElement('a');
                        link.href = window.location.origin + '/?table_id={m.id}';
                        link.textContent = window.location.origin + '/?table_id={m.id}';
                        link.target = '_blank';
                        link.rel = 'noopener noreferrer';
                        document.write(link.outerHTML);
                    }})();
                </script>
            ''')
        return Markup("-")

    column_formatters = {
        DBTable.is_available: _available_formatter,
        "created_at": lambda m, a: format_datetime_msk(m.created_at),
        "updated_at": lambda m, a: format_datetime_msk(m.updated_at),
        "table_link": _table_link_formatter
    }

    column_formatters_detail = column_formatters

    async def on_before_form(self, request: Request, obj=None):
        request.state.custom_css = add_css_styles()
        return await super().on_before_form(request, obj)

    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True