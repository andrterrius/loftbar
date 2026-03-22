from typing import Optional

from fastapi.requests import Request

from sqladmin.pagination import Pagination
from sqladmin import ModelView
from sqlalchemy.orm import selectinload
from sqlalchemy import func, select

from markupsafe import Markup

from app.core.common import format_datetime_msk
from app.db.models import (
    DBPreset,
    DBLiquid,
    DBBowl,
    DBSettings
)

class PresetAdmin(ModelView, model=DBPreset):
    name = "Пресет"
    name_plural = "Пресеты"
    icon = "fa-solid fa-layer-group"

    column_labels = {
        "name": "Название",
        "category": "Категория",
        "price": "Цена",
        "is_available": "Доступен",
        "description": "Описание",
        "liquid": "Жидкость",
        "bowl": "Чаша",
        "settings": "Настройки",
        "created_by": "Создатель",
        "created_at": "Дата создания",
        "updated_at": "Дата обновления",
        "hex_color": "Цвет",
        "presets": "Пресеты",
        "preset_flavors": "Проценты вкусов"
    }

    column_list = [
        "name",
        "category",
        "price",
        "is_available",
        "liquid",
        "bowl",
        "hex_color",
        "created_by",
        "created_at",
    ]

    column_details_list = [
        "name",
        "category",
        "price",
        "description",
        "is_available",
        "bowl",
        "liquid",
        "settings",
        "preset_flavors",
        "created_by",
        "created_at",
        "updated_at",
    ]

    column_sortable_list = [
        DBPreset.category,
        "price",
        DBPreset.is_available,
        DBPreset.created_at,
        DBPreset.created_by_id,
    ]

    column_default_sort = [("created_by_id", True), ("is_available", True), ("updated_at", True)]

    column_searchable_list = ["name", "category", "description"]

    form_create_rules = []
    form_edit_rules = []

    @staticmethod
    def _price_formatter(m, a):
        """Форматтер для цены без пояснений"""
        total_price = m.settings.preset_base_price
        if m.liquid:
            total_price += m.liquid.price
        if m.bowl:
            total_price += m.bowl.price

        return f"{total_price}₽"

    @staticmethod
    def _price_formatter_detail(m, a):
        """Форматтер для цены с пояснениями"""
        total_price = m.settings.preset_base_price
        if m.liquid:
            total_price += m.liquid.price
        if m.bowl:
            total_price += m.bowl.price
        return Markup(f"{m.settings.preset_base_price}₽ (базовая цена)"
                f"<br>{m.liquid.price if m.liquid else "<span style='color: red;'>❌ удалено</span>, 0"}₽ (жидкость)"
                f"<br>{m.bowl.price if m.bowl else "<span style='color: red;'>❌ удалено</span>, 0"}₽ (чаша)"
                f"<br> = {total_price}₽")

    @staticmethod
    def _available_formatter(m, a):
        """Форматтер доступности"""
        is_available, reason = m.availability_info

        if not is_available:
            return Markup(f'<span style="color: red;">❌ Нет {reason}</span>')

        return Markup('<span style="color: green;">✅ Да</span>')

    def _color_formatter(m, a):
        if m.hex_color:
            return Markup(
                f'<div style="background-color: {m.hex_color}; width: 30px; height: 20px; border-radius: 4px; border: 1px solid #ddd;"></div>'
            )
        return Markup('<span style="color: #999;">—</span>')

    @staticmethod
    def _liquid_formatter(m, a):
        if hasattr(m, 'liquid') and m.liquid:
            return m.liquid.name
        return "-"

    @staticmethod
    def _bowl_formatter(m, a):
        if hasattr(m, 'bowl') and m.bowl:
            return m.bowl.name
        return "-"

    @staticmethod
    def _settings_formatter(m, a):
        if hasattr(m, 'settings') and m.settings:
            return f"Базовая цена: {m.settings.preset_base_price} ₽"
        return "-"

    @staticmethod
    def _creator_formatter(m, a):
        if hasattr(m, 'created_by') and m.created_by:
            return m.created_by.username or m.created_by.first_name or str(m.created_by.telegram_id)
        return "Админ"

    column_formatters = {
        "price": _price_formatter,
        "is_available": _available_formatter,
        "liquid": _liquid_formatter,
        "bowl": _bowl_formatter,
        "settings": _settings_formatter,
        "created_by": _creator_formatter,
        "hex_color": _color_formatter,
        "created_at": lambda m, a: format_datetime_msk(m.created_at),
        "updated_at": lambda m, a: format_datetime_msk(m.updated_at)
    }

    column_formatters_detail = {
        "price": _price_formatter_detail,
        "is_available": _available_formatter,
        "liquid": _liquid_formatter,
        "bowl": _bowl_formatter,
        "settings": _settings_formatter,
        "created_by": _creator_formatter,
        "hex_color": _color_formatter,
        "created_at": lambda m, a: format_datetime_msk(m.created_at),
        "updated_at": lambda m, a: format_datetime_msk(m.updated_at)
    }

    _list_relations = [
        DBPreset.bowl,
        DBPreset.liquid,
        DBPreset.created_by,
        DBPreset.settings,
        DBPreset.preset_flavors
    ]

    def list_query(self, request: Request) -> select:
        """Базовый запрос для списка"""
        return select(DBPreset)

    def sort_query(self, stmt: select, request: Request) -> select:
        """Кастомная сортировка для цены"""
        sort_by = request.query_params.get("sortBy")
        sort_desc = request.query_params.get("sortDesc") == "true"

        if sort_by == "price":
            price_expression = (
                    func.coalesce(DBSettings.preset_base_price, 0) +
                    func.coalesce(DBBowl.price, 0) +
                    func.coalesce(DBLiquid.price, 0)
            )

            stmt = stmt.outerjoin(DBBowl, DBPreset.bowl_id == DBBowl.id)
            stmt = stmt.outerjoin(DBLiquid, DBPreset.liquid_id == DBLiquid.id)
            stmt = stmt.outerjoin(DBSettings, DBPreset.settings_id == DBSettings.id)

            if sort_desc:
                stmt = stmt.order_by(price_expression.desc())
            else:
                stmt = stmt.order_by(price_expression.asc())

            return stmt
        else:
            return super().sort_query(stmt, request)

    def validate_page_number(self, value: Optional[str], default: int) -> int:
        """Валидация номера страницы"""
        try:
            return int(value) if value else default
        except ValueError:
            return default

    async def list(self, request: Request) -> Pagination:
        """Переопределенный метод list с поддержкой сортировки по цене"""
        page = self.validate_page_number(request.query_params.get("page"), 1)
        page_size = self.validate_page_number(request.query_params.get("pageSize"), 0)
        page_size = min(page_size or self.page_size, max(self.page_size_options))
        search = request.query_params.get("search", None)

        stmt = self.list_query(request)

        for relation in self._list_relations:
            stmt = stmt.options(selectinload(relation))

        stmt = self.sort_query(stmt, request)

        if search:
            stmt = self.search_query(stmt=stmt, term=search)

        count = await self.count(
            request, select(func.count()).select_from(stmt.subquery())
        )

        stmt = stmt.limit(page_size).offset((page - 1) * page_size)
        rows = await self._run_query(stmt)

        pagination = Pagination(
            rows=rows,
            page=page,
            page_size=page_size,
            count=count,
        )

        return pagination