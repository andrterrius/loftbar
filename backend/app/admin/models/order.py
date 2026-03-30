from fastapi.requests import Request
from sqladmin import ModelView

from markupsafe import Markup
from sqladmin.fields import SelectField
from wtforms import SelectField as WTSelectField

from app.db.models import DBOrder
from app.db.models.order import OrderStatus
from app.core.common import format_datetime_msk
from app.admin.utils import add_css_styles

class OrderAdmin(ModelView, model=DBOrder):
    name = "Заказ"
    name_plural = "Заказы"
    icon = "fa-solid fa-receipt"

    column_labels = {
        "id": "ID заказа",
        "daily_number": "Номер заказа",
        "user": "Пользователь",
        "table": "Столик",
        "preset": "Пресет",
        "status": "Статус",
        "total_price": "Сумма",
        "special_requests": "Особые пожелания",
        "is_custom": "Тип заказа",
        "custom_name": "Название кастомного заказа",
        "composition_snapshot": "Состав заказа",
        "confirmed_at": "Подтвержден",
        "ready_at": "Готов",
        "completed_at": "Завершен",
        "admin_notification_sent": "Уведомление админу",
        "created_at": "Создан",
        "updated_at": "Обновлен",
    }

    column_list = [
        DBOrder.daily_number,
        DBOrder.user,
        DBOrder.total_price,
        DBOrder.status,
        DBOrder.preset,
        DBOrder.is_custom,
        DBOrder.table,
        DBOrder.admin_notification_sent,
        DBOrder.created_at,
    ]

    column_searchable_list = [
        DBOrder.id,
        DBOrder.daily_number,
        DBOrder.custom_name,
        DBOrder.special_requests,
    ]

    column_sortable_list = [
        DBOrder.status,
        DBOrder.is_custom,
        DBOrder.total_price,
        DBOrder.created_at,
        DBOrder.confirmed_at,
        DBOrder.ready_at,
        DBOrder.completed_at,
    ]

    column_default_sort = [(DBOrder.created_at, True)]

    form_create_rules = [
        "user", "table", "preset", "status", "total_price",
        "special_requests", "is_custom", "custom_name",
        "composition_snapshot", "confirmed_at", "ready_at",
        "completed_at", "admin_notification_sent"
    ]

    form_edit_rules = [
        "user", "table", "preset", "status", "total_price",
        "special_requests", "is_custom", "custom_name",
        "confirmed_at", "ready_at",
        "completed_at", "admin_notification_sent"
    ]

    STATUS_CHOICES = [
        (OrderStatus.PENDING.value, "🕒 Ожидает (Pending)"),
        (OrderStatus.IN_PROGRESS.value, "👨‍🍳 Готовится (In Progress)"),
        (OrderStatus.READY.value, "✅ Готов (Ready)"),
        (OrderStatus.COMPLETED.value, "✔️ Завершен (Completed)"),
        (OrderStatus.CANCELLED.value, "❌ Отменен (Cancelled)"),
    ]

    form_overrides = {
        "status": SelectField
    }

    form_args = {
        "user": {
            "label": "Пользователь",
            "description": "Пользователь, оформивший заказ",
        },
        "table": {
            "label": "Столик",
            "description": "Столик для заказа",
        },
        "preset": {
            "label": "Пресет",
            "description": "Выбранный пресет (для готовых заказов)",
        },
        "status": {
            "label": "Статус / Status",
            "description": "Текущий статус заказа / Current order status",
            "choices": STATUS_CHOICES,
            "coerce": str,
        },
        "total_price": {
            "label": "Сумма",
            "description": "Итоговая сумма заказа",
            "render_kw": {"type": "number", "step": "0.01", "min": "0", "class": "form-control", "required": "required"}
        },
        "special_requests": {
            "label": "Особые пожелания",
            "description": "Дополнительные пожелания к заказу",
            "render_kw": {"placeholder": "Без чего-то, с чем-то и т.д.", "class": "form-control", "rows": 3}
        },
        "is_custom": {
            "label": "Кастомный заказ",
            "description": "Отметить, если это кастомный заказ",
            "render_kw": {"class": "form-check-input"}
        },
        "custom_name": {
            "label": "Название кастомного заказа",
            "description": "Название для кастомного заказа",
            "render_kw": {"placeholder": "Мой особый заказ", "class": "form-control"}
        },
        "composition_snapshot": {
            "label": "Состав заказа",
            "description": "JSON с составом заказа на момент создания",
            "render_kw": {"class": "form-control", "rows": 5}
        },
        "admin_notification_sent": {
            "label": "Уведомление отправлено",
            "description": "Было ли отправлено уведомление администратору",
            "render_kw": {"class": "form-check-input"}
        },
        "confirmed_at": {
            "label": "Подтвержден",
            "description": "Дата и время подтверждения заказа",
            "render_kw": {"type": "datetime-local", "class": "form-control"}
        },
        "ready_at": {
            "label": "Готов",
            "description": "Дата и время готовности заказа",
            "render_kw": {"type": "datetime-local", "class": "form-control"}
        },
        "completed_at": {
            "label": "Завершен",
            "description": "Дата и время завершения заказа",
            "render_kw": {"type": "datetime-local", "class": "form-control"}
        }
    }

    form_widget_args = {
        "is_custom": {"class": "form-check-input"},
        "admin_notification_sent": {"class": "form-check-input"},
        "special_requests": {"rows": 3},
        "composition_snapshot": {"rows": 5},
    }

    def _status_formatter(m, a):
        status_colors = {
            OrderStatus.PENDING: ("warning", "🕒 Ожидает (Pending)"),
            OrderStatus.IN_PROGRESS: ("info", "👨‍🍳 Готовится (In Progress)"),
            OrderStatus.READY: ("success", "✅ Готов (Ready)"),
            OrderStatus.COMPLETED: ("secondary", "✔️ Завершен (Completed)"),
            OrderStatus.CANCELLED: ("danger", "❌ Отменен (Cancelled)"),
        }

        color, text = status_colors.get(m.status, ("secondary", str(m.status)))
        return Markup(f'<span class="badge bg-{color}">{text}</span>')

    def _price_formatter(m, a):
        return Markup(f'{m.total_price:.2f} ₽')

    def _order_type_formatter(m, a):
        if m.is_custom:
            if m.custom_name:
                return Markup(f'✨ {m.custom_name}')
            return Markup('✨ Кастомный')
        return Markup('📦 Готовый')

    def _notification_formatter(m, a):
        if m.admin_notification_sent:
            return Markup('✅ Да')
        return Markup('❌ Нет')

    column_formatters = {
        DBOrder.status: _status_formatter,
        DBOrder.total_price: _price_formatter,
        DBOrder.is_custom: _order_type_formatter,
        DBOrder.admin_notification_sent: _notification_formatter,
        "confirmed_at": lambda m, a: format_datetime_msk(m.confirmed_at),
        "ready_at": lambda m, a: format_datetime_msk(m.ready_at),
        "completed_at": lambda m, a: format_datetime_msk(m.completed_at),
        "created_at": lambda m, a: format_datetime_msk(m.created_at),
        "updated_at": lambda m, a: format_datetime_msk(m.updated_at)
    }

    column_formatters_detail = column_formatters

    async def on_before_form(self, request: Request, obj=None):
        request.state.custom_css = add_css_styles()
        return await super().on_before_form(request, obj)

    can_edit = True
    can_delete = True
    can_view_details = True