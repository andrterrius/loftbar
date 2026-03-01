from fastapi.requests import Request

from sqladmin import ModelView
from markupsafe import Markup

from app.db.models import DBUser

from app.admin.utils import add_css_styles, add_image_preview_js


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
        "created_at": "Дата регистрации",
        "updated_at": "Дата обновления",
        "presets": "Пресеты"
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
    column_default_sort = [(DBUser.is_admin, True), (DBUser.created_at, True)]

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

    can_create = False
    can_edit = True
    can_delete = True
    can_view_details = True