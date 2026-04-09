from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from sqladmin import ModelView, action
from sqladmin.fields import QuerySelectMultipleField
from markupsafe import Markup
from wtforms import SelectMultipleField, widgets
from sqlalchemy import nulls_last, desc, update

from app.db.models import DBFlavor, DBFlavorCategory
from app.core.common import format_datetime_msk
from app.admin.utils import add_css_styles, add_image_preview_js


class FlavorAdmin(ModelView, model=DBFlavor):
    name = "Вкус"
    name_plural = "Вкусы"
    icon = "fa-solid fa-ice-cream"

    column_labels = {
        "id": "ID",
        "name": "Название вкуса",
        "brand": "Бренд",
        "is_available": "В наличии",
        "description": "Описание",
        "hex_color": "Цвет",
        "image_url": "Изображение",
        "categories": "Категории",
        "priority": "Приоритет",
        "created_at": "Дата создания",
        "updated_at": "Дата обновления"
    }

    column_list = [
        DBFlavor.name,
        DBFlavor.brand,
        DBFlavor.categories,
        DBFlavor.is_available,
        "priority",
        DBFlavor.created_at
    ]

    column_searchable_list = [DBFlavor.name, DBFlavor.brand]

    column_sortable_list = [
        DBFlavor.name,
        DBFlavor.brand,
        DBFlavor.is_available,
        DBFlavor.priority,
        DBFlavor.created_at,
        DBFlavor.updated_at
    ]

    column_default_sort = [(DBFlavor.priority, False), (DBFlavor.is_available, True), (DBFlavor.name, True)]

    # Переопределяем поле categories для использования QuerySelectMultipleField
    form_overrides = {
        "categories": QuerySelectMultipleField
    }

    form_create_rules = [
        "name", "brand", "categories", "is_available",
        "description", "hex_color", "image_url"
    ]

    form_edit_rules = [
        "name", "brand", "categories", "is_available",
        "description", "hex_color", "image_url"
    ]

    form_args = {
        "name": {
            "label": "Название вкуса",
            "render_kw": {"placeholder": "Например: Клубника", "class": "form-control"}
        },
        "brand": {
            "label": "Бренд",
            "render_kw": {"placeholder": "Например: TPA", "class": "form-control"}
        },
        "categories": {
            "label": "Категории",
            "description": "Выберите одну или несколько категорий для этого вкуса",
            "render_kw": {
                "class": "form-control category-select",
                "multiple": "multiple",
                "data-live-search": "true",
                "data-actions-box": "true",
                "size": "10"
            }
        },
        "is_available": {
            "label": "В наличии",
            "render_kw": {"class": "form-check-input"}
        },
        "description": {
            "label": "Описание",
            "render_kw": {"rows": 3, "class": "form-control"}
        },
        "hex_color": {
            "label": "Цвет",
            "description": "Выберите цвет для вкуса",
            "render_kw": {
                "type": "color",
                "class": "form-control form-control-color",
                "style": "width: 60px; height: 40px; padding: 0;"
            }
        },
        "image_url": {
            "label": "URL изображения",
            "description": "Ссылка на изображение вкуса",
            "render_kw": {"placeholder": "https://...", "class": "form-control"}
        }
    }

    @action(
        name="set_available",
        label="✅ Установить 'В наличии' для выбранных",
        confirmation_message="Вы уверены, что хотите установить статус 'В наличии' для выбранных вкусов?",
        add_in_detail=False,
        add_in_list=True
    )
    async def set_available_action(self, request: Request):
        form = request.query_params
        pks = form.get("pks", "").split(",")

        if not pks:
            referer = request.headers.get("referer", f"/admin/{self.identity}/list")
            return RedirectResponse(url=referer, status_code=302)

        # Обновляем записи
        async with self.session_maker() as session:
            stmt = (
                update(self.model)
                .where(self.model.id.in_(pks))
                .values(is_available=True)
            )
            await session.execute(stmt)
            await session.commit()

        # Перенаправляем обратно
        referer = request.headers.get("referer", f"/admin/{self.identity}/list")
        return RedirectResponse(url=referer, status_code=302)

    @action(
        name="set_unavailable",
        label="❌ Установить 'Не в наличии' для выбранных",
        confirmation_message="Вы уверены, что хотите установить статус 'Не в наличии' для выбранных вкусов?",
        add_in_detail=False,
        add_in_list=True
    )
    async def set_unavailable_action(self, request: Request):
        form = request.query_params
        pks = form.get("pks", "").split(",")

        if not pks:
            referer = request.headers.get("referer", f"/admin/{self.identity}/list")
            return RedirectResponse(url=referer, status_code=302)

        async with self.session_maker() as session:
            stmt = (
                update(self.model)
                .where(self.model.id.in_(pks))
                .values(is_available=False)
            )
            await session.execute(stmt)
            await session.commit()

        referer = request.headers.get("referer", f"/admin/{self.identity}/list")
        return RedirectResponse(url=referer, status_code=302)

    def _available_formatter(m, a):
        return Markup("✅ Да") if m.is_available else Markup("❌ Нет")

    def _color_formatter(m, a):
        if m.hex_color:
            return Markup(
                f'<div style="background-color: {m.hex_color}; width: 30px; height: 20px; '
                f'border-radius: 4px; border: 1px solid #ddd;"></div>'
            )
        return Markup('<span style="color: #999;">—</span>')

    column_formatters = {
        DBFlavor.is_available: _available_formatter,
        DBFlavor.hex_color: _color_formatter,
        "created_at": lambda m, a: format_datetime_msk(m.created_at),
        "updated_at": lambda m, a: format_datetime_msk(m.updated_at)
    }

    column_formatters_detail = column_formatters

    async def on_before_form(self, request: Request, obj=None):
        request.state.custom_css = add_css_styles()
        request.state.custom_js = add_image_preview_js()
        return await super().on_before_form(request, obj)