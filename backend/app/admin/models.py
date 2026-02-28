import uuid as uuid_pkg
import csv
import io

from fastapi.requests import Request
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse

from fastapi.responses import RedirectResponse, Response
from markupsafe import Markup
from sqlalchemy import select, delete, or_
from sqlalchemy.orm import selectinload
from sqladmin import BaseView, ModelView, expose, action
from sqladmin.authentication import login_required

from typing import Any, Optional, List
from wtforms import FieldList, FormField, SelectField, FloatField, HiddenField
from wtforms.validators import DataRequired, NumberRange, ValidationError
from wtforms import Form

from app.db.models import (
    DBPreset,
    DBFlavor,
    DBPresetFlavor,
    DBLiquid,
    DBBowl,
    DBUser,
)
from .utils import *

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
        "image_url": "Изображение",
        "liquid": "Жидкость",
        "bowl": "Чаша",
        "created_by": "Создатель",
        "created_at": "Дата создания",
        "updated_at": "Дата обновления",
        "preset_flavors": "Список вкусов"
    }

    column_list = [
        DBPreset.name,
        DBPreset.category,
        DBPreset.price,
        DBPreset.is_available,
        DBPreset.liquid,
        DBPreset.bowl,
        DBPreset.image_url,
        DBPreset.created_at,
    ]

    column_searchable_list = [DBPreset.name, DBPreset.category, DBPreset.description]
    column_sortable_list = [DBPreset.name, DBPreset.price, DBPreset.created_at]
    column_default_sort = [(DBPreset.created_at, True)]

    # Убираем стандартные правила форм
    form_create_rules = []
    form_edit_rules = []

    # Форматтеры для колонок
    @staticmethod
    def _price_formatter(m, a):
        return f"{m.price:.2f} ₽"

    @staticmethod
    def _image_formatter(m, a):
        if m.image_url:
            return Markup(
                f'<img src="{m.image_url}" style="max-width: 50px; max-height: 50px; border-radius: 4px; object-fit: cover;" onerror="this.style.display=\'none\'">'
            )
        return Markup('<span style="color: #999;">—</span>')

    def _available_formatter(self, a):

        for pf in self.preset_flavors:
            if not pf.flavor or not pf.flavor.is_available:
                return Markup(f'<span style="color: red;">❌ Нет (недоступен вкус {pf.flavor.name})</span>')

        if not self.bowl or not self.bowl.is_available:
            return Markup(f'<span style="color: red;">❌ Нет (недоступна чаша)</span>')

        if not self.liquid or not self.liquid.is_available:
            return Markup(f'<span style="color: red;">❌ Нет (недоступна жидкость)</span>')


        return Markup('<span style="color: green;">✅ Да</span>')

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
    def _creator_formatter(m, a):
        if hasattr(m, 'created_by') and m.created_by:
            return m.created_by.username or m.created_by.first_name or str(m.created_by.telegram_id)
        return "-"

    column_formatters = {
        DBPreset.price: _price_formatter,
        DBPreset.image_url: _image_formatter,
        DBPreset.is_available: _available_formatter,
        DBPreset.liquid: _liquid_formatter,
        DBPreset.bowl: _bowl_formatter,
        DBPreset.created_by: _creator_formatter
    }

    column_formatters_detail = {
        DBPreset.price: _price_formatter,
        DBPreset.image_url: _image_formatter,
        DBPreset.is_available: _available_formatter,
        DBPreset.liquid: _liquid_formatter,
        DBPreset.bowl: _bowl_formatter,
        DBPreset.created_by: _creator_formatter
    }

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
        "updated_at": "Дата обновления"
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
    column_default_sort = [(DBBowl.created_at, True)]

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
        print(m)
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


class FlavorAdmin(ModelView, model=DBFlavor):
    name = "Вкус"
    name_plural = "Вкусы"
    icon = "fa-solid fa-ice-cream"

    column_labels = {
        "name": "Название",
        "brand": "Бренд",
        "category": "Категория",
        "is_available": "В наличии",
        "hex_color": "Цвет",
        "image_url": "Изображение",
        "created_at": "Дата создания"
    }

    column_list = [
        DBFlavor.name,
        DBFlavor.brand,
        DBFlavor.category,
        DBFlavor.is_available,
        DBFlavor.hex_color,
        DBFlavor.image_url,
        DBFlavor.created_at
    ]

    column_searchable_list = [DBFlavor.name, DBFlavor.brand, DBFlavor.category]
    column_sortable_list = [DBFlavor.name, DBFlavor.brand, DBFlavor.created_at]
    column_default_sort = [(DBFlavor.name, False)]

    form_create_rules = [
        "name", "brand", "category", "is_available", "hex_color", "image_url"
    ]
    form_edit_rules = [
        "name", "brand", "category", "is_available", "hex_color", "image_url"
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
            "description": "Ссылка на картинку или загрузите файл",
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
        DBFlavor.image_url: _image_formatter,
        DBFlavor.is_available: _available_formatter
    }

    async def on_before_form(self, request: Request, obj=None):
        request.state.custom_css = add_css_styles()
        request.state.custom_js = add_image_preview_js()
        return await super().on_before_form(request, obj)

    column_formatters_detail = column_formatters


class LiquidAdmin(ModelView, model=DBLiquid):
    name = "Жидкость"
    name_plural = "Жидкости"
    icon = "fa-solid fa-flask"

    column_labels = {
        "name": "Название",
        "category": "Категория",
        "price": "Цена",
        "is_available": "В наличии",
        "description": "Описание",
        "hex_color": "Цвет",
        "image_url": "Изображение",
        "created_at": "Дата создания"
    }

    column_list = [
        DBLiquid.name,
        DBLiquid.category,
        DBLiquid.price,
        DBLiquid.is_available,
        DBLiquid.description,
        DBLiquid.image_url,
        DBLiquid.created_at
    ]

    column_searchable_list = [DBLiquid.name, DBLiquid.category, DBLiquid.description]
    column_sortable_list = [DBLiquid.name, DBLiquid.price, DBLiquid.created_at]
    column_default_sort = [(DBLiquid.created_at, True)]

    form_create_rules = [
        "name", "category", "price", "is_available", "description",
        "hex_color", "image_url"
    ]
    form_edit_rules = [
        "name", "category", "price", "is_available", "description",
        "hex_color", "image_url"
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
        "description": {
            "label": "Описание",
            "description": "Краткое описание",
            "render_kw": {"placeholder": "Вкусная жидкость с ароматом...", "class": "form-control"}
        },
        "hex_color": {
            "label": "Цвет",
            "description": "Выберите цвет для жидкости",
            "render_kw": {"type": "color", "class": "form-control form-control-color",
                          "style": "width: 60px; height: 40px; padding: 0;"}
        },
        "image_url": {
            "label": "URL изображения",
            "description": "Ссылка на картинку или загрузите файл",
            "render_kw": {"type": "url", "class": "form-control", "placeholder": "https://example.com/image.jpg"}
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

    def _image_formatter(m, a):
        if m.image_url:
            return Markup(
                f'<img src="{m.image_url}" style="max-width: 50px; max-height: 50px; border-radius: 4px; object-fit: cover;" onerror="this.style.display=\'none\'">'
            )
        return Markup('<span style="color: #999;">—</span>')

    def _available_formatter(m, a):
        return Markup("✅ Да") if m.is_available else Markup("❌ Нет")

    column_formatters = {
        DBLiquid.price: _price_formatter,
        DBLiquid.hex_color: _color_formatter,
        DBLiquid.image_url: _image_formatter,
        DBLiquid.is_available: _available_formatter
    }

    async def on_before_form(self, request: Request, obj=None):
        request.state.custom_css = add_css_styles()
        request.state.custom_js = add_image_preview_js()
        return await super().on_before_form(request, obj)

# ==================== АДМИНКА ДЛЯ ПОЛЬЗОВАТЕЛЕЙ ====================
class UserAdmin(ModelView, model=DBUser):
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"

    column_labels = {
        "telegram_id": "Telegram ID",
        "first_name": "Имя",
        "last_name": "Фамилия",
        "username": "Username",
        "is_admin": "Админ",
        "is_premium": "Premium",
        "language_code": "Язык",
        "photo_url": "Фото",
        "created_at": "Дата регистрации"
    }

    column_list = [
        DBUser.telegram_id,
        DBUser.first_name,
        DBUser.last_name,
        DBUser.username,
        DBUser.is_admin,
        DBUser.is_premium,
        DBUser.language_code,
        DBUser.photo_url,
        DBUser.created_at
    ]

    column_searchable_list = [
        DBUser.first_name,
        DBUser.last_name,
        DBUser.username,
        DBUser.telegram_id
    ]
    column_sortable_list = [
        DBUser.created_at,
        DBUser.is_admin,
        DBUser.first_name,
        DBUser.telegram_id
    ]
    column_default_sort = [(DBUser.created_at, True)]

    form_create_rules = [
        "telegram_id", "first_name", "last_name", "username",
        "photo_url", "language_code", "is_admin", "is_premium"
    ]
    form_edit_rules = [
        "telegram_id", "first_name", "last_name", "username",
        "photo_url", "language_code", "is_admin", "is_premium"
    ]

    form_args = {
        "telegram_id": {
            "label": "Telegram ID",
            "description": "ID пользователя в Telegram",
            "render_kw": {"type": "number", "class": "form-control"}
        },
        "first_name": {
            "label": "Имя",
            "render_kw": {"placeholder": "Иван", "class": "form-control"}
        },
        "last_name": {
            "label": "Фамилия",
            "render_kw": {"placeholder": "Иванов", "class": "form-control"}
        },
        "username": {
            "label": "Username",
            "description": "Никнейм в Telegram",
            "render_kw": {"placeholder": "@username", "class": "form-control"}
        },
        "photo_url": {
            "label": "Фото URL",
            "description": "Ссылка на фото профиля",
            "render_kw": {"type": "url", "class": "form-control", "placeholder": "https://example.com/photo.jpg"}
        },
        "language_code": {
            "label": "Код языка",
            "description": "Например: ru, en",
            "render_kw": {"placeholder": "ru", "class": "form-control", "maxlength": "10"}
        },
        "is_admin": {
            "label": "Администратор",
            "description": "Есть ли права админа",
            "render_kw": {"class": "form-check-input"}
        },
        "is_premium": {
            "label": "Premium",
            "description": "Есть ли Telegram Premium",
            "render_kw": {"class": "form-check-input"}
        }
    }

    form_widget_args = {
        "is_admin": {"class": "form-check-input"},
        "is_premium": {"class": "form-check-input"}
    }

    def _photo_formatter(m, a):
        if m.photo_url:
            return Markup(
                f'<img src="{m.photo_url}" width="30" height="30" style="border-radius: 50%; object-fit: cover;" onerror="this.style.display=\'none\'">'
            )
        return Markup('<span style="color: #999;">—</span>')

    def _admin_formatter(m, a):
        return Markup("✅ Да") if m.is_admin else Markup("❌ Нет")

    def _premium_formatter(m, a):
        return Markup("✅ Да") if m.is_premium else Markup("❌ Нет")

    column_formatters = {
        DBUser.photo_url: _photo_formatter,
        DBUser.is_admin: _admin_formatter,
        DBUser.is_premium: _premium_formatter
    }

    async def on_before_form(self, request: Request, obj=None):
        request.state.custom_css = add_css_styles()
        request.state.custom_js = add_image_preview_js()
        return await super().on_before_form(request, obj)

    column_formatters_detail = column_formatters

    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True