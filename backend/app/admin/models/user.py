from fastapi.requests import Request
from sqladmin import ModelView
from markupsafe import Markup

from app.db.models import DBUser
from app.core.common import format_datetime_msk
from app.admin.utils import add_css_styles


class UserAdmin(ModelView, model=DBUser):
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-users"

    column_labels = {
        "id": "ID",
        "is_admin": "Статус",
        "telegram_id": "Telegram ID",
        "phone_number": "Номер телефона",
        "first_name": "Имя",
        "last_name": "Фамилия",
        "username": "Username",
        "photo_url": "Фото",
        "language_code": "Язык",
        "is_premium": "Premium",
        "is_active": "Активен",
        "is_banned": "Заблокирован",
        "preset_base_price": "Базовая цена пресета",
        "presets": "Пресеты",
        "orders": "Заказы",
        "created_at": "Дата регистрации",
        "updated_at": "Дата обновления",
    }

    column_list = [
        DBUser.username,
        DBUser.first_name,
        DBUser.last_name,
        DBUser.phone_number,
        DBUser.is_admin,
        DBUser.is_active,
        DBUser.is_banned,
        DBUser.preset_base_price,
        DBUser.created_at,
    ]

    column_searchable_list = [
        DBUser.username,
        DBUser.first_name,
        DBUser.last_name,
        DBUser.telegram_id,
        DBUser.phone_number,
    ]

    column_sortable_list = [
        DBUser.username,
        DBUser.first_name,
        DBUser.last_name,
        DBUser.phone_number,
        DBUser.is_admin,
        DBUser.is_active,
        DBUser.is_banned,
        DBUser.created_at,
        DBUser.preset_base_price,
    ]

    column_default_sort = [(DBUser.is_admin, True), (DBUser.created_at, True)]

    form_edit_rules = [
        "preset_base_price",
        "telegram_id",
        "phone_number",
        "first_name",
        "last_name",
        "username",
        "language_code",
        "is_admin",
        "is_active",
        "is_banned",
        "is_premium",
    ]

    form_args = {
        "preset_base_price": {
            "label": "Базовая цена пресета",
            "description": "Базовая цена для пресетов пользователя (необязательно)",
            "render_kw": {"type": "number", "step": "0.01", "class": "form-control", "placeholder": "0.00"}
        },
        "telegram_id": {
            "label": "Telegram ID",
            "description": "Уникальный идентификатор пользователя в Telegram",
            "render_kw": {"type": "number", "class": "form-control"}
        },
        "phone_number": {
            "label": "Номер телефона",
            "description": "Номер телефона пользователя",
            "render_kw": {"placeholder": "+7 (999) 123-45-67", "class": "form-control"}
        },
        "first_name": {
            "label": "Имя",
            "description": "Имя пользователя",
            "render_kw": {"placeholder": "Иван", "class": "form-control"}
        },
        "last_name": {
            "label": "Фамилия",
            "description": "Фамилия пользователя",
            "render_kw": {"placeholder": "Петров", "class": "form-control"}
        },
        "username": {
            "label": "Username",
            "description": "Имя пользователя в Telegram (без @)",
            "render_kw": {"placeholder": "ivan_petrov", "class": "form-control"}
        },
        "language_code": {
            "label": "Язык",
            "description": "Код языка пользователя",
            "render_kw": {"placeholder": "ru", "class": "form-control"}
        },
        "is_admin": {
            "label": "Администратор",
            "description": "Дать пользователю права администратора",
            "render_kw": {"class": "form-check-input"}
        },
        "is_active": {
            "label": "Активен",
            "description": "Активен ли пользователь",
            "render_kw": {"class": "form-check-input"}
        },
        "is_banned": {
            "label": "Заблокирован",
            "description": "Заблокировать пользователя",
            "render_kw": {"class": "form-check-input"}
        },
        "is_premium": {
            "label": "Premium",
            "description": "Есть ли у пользователя Telegram Premium",
            "render_kw": {"class": "form-check-input", "type": "checkbox", "value": "y"}
        }
    }

    def _bool_formatter(value, true_markup="✅ Да", false_markup="❌ Нет"):
        return Markup(true_markup) if value else Markup(false_markup)

    def _admin_formatter(m, a):
        return UserAdmin._bool_formatter(m.is_admin, "👑 Админ", "👤 Пользователь")

    def _active_formatter(m, a):
        return UserAdmin._bool_formatter(m.is_active)

    def _banned_formatter(m, a):
        return UserAdmin._bool_formatter(m.is_banned, "🚫 Заблокирован", "✅ Нет")

    def _premium_formatter(m, a):
        return UserAdmin._bool_formatter(m.is_premium, "⭐ Premium", "—")

    def _username_formatter(m, a):
        if m.username:
            return Markup(f"@{m.username}")
        return "—"

    def _phone_formatter(m, a):
        if m.phone_number:
            return Markup(f'<a href="tel:{m.phone_number}">{m.phone_number}</a>')
        return "—"

    def _price_formatter(m, a):
        if m.preset_base_price is not None:
            return Markup(f"{m.preset_base_price:.2f} ₽")
        return "—"

    def _photo_formatter(m, a):
        if m.photo_url:
            return Markup(
                f'<img src="{m.photo_url}" style="max-width: 50px; max-height: 50px; border-radius: 50%;" title="Фото профиля">')
        return "—"

    column_formatters = {
        DBUser.username: _username_formatter,
        DBUser.phone_number: _phone_formatter,
        DBUser.is_admin: _admin_formatter,
        DBUser.is_active: _active_formatter,
        DBUser.is_banned: _banned_formatter,
        DBUser.is_premium: _premium_formatter,
        DBUser.preset_base_price: _price_formatter,
        DBUser.photo_url: _photo_formatter,
        "created_at": lambda m, a: format_datetime_msk(m.created_at),
        "updated_at": lambda m, a: format_datetime_msk(m.updated_at),
    }

    column_formatters_detail = column_formatters

    async def on_before_form(self, request: Request, obj=None):
        request.state.custom_css = add_css_styles()
        return await super().on_before_form(request, obj)

    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True