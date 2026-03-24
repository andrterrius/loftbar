from typing import Optional
from app.schemas.order import OrderOutAdmin, OrderStatus
from app.core.common import format_datetime_msk


class NotificationTextService:
    """Сервис для генерации текстов уведомлений о заказах"""

    @staticmethod
    def get_status_emoji(status: OrderStatus) -> str:
        """Возвращает эмодзи для статуса"""
        emoji_map = {
            "pending": "⏳ В ожидании",
            "in_progress": "👨‍🍳 В процессе",
            "ready": "✅ Готов",
            "completed": "✨ Завершен",
            "cancelled": "❌ Отменен"
        }
        status_str = status.value
        return emoji_map.get(status_str, "🔄")

    def generate_order_notification(
            self,
            order: OrderOutAdmin,
            is_update: bool = False
    ) -> str:
        """Генерирует текст уведомления о заказе"""

        text = (
            f"🆕 <b>{'НОВЫЙ' if not is_update else 'ОБНОВЛЕННЫЙ'} ЗАКАЗ <code>{order.id}</code></b>\n\n"
        )
        if order.table:
            text += self._format_table_info(order.table)

        if order.preset:
            text += self._format_preset_info(order.preset)
        elif order.composition_snapshot:
            text += self._format_snapshot_info(order.composition_snapshot)

        if order.user:
            text += self._format_user_info(order.user)

        if order.special_requests:
            text += f"\n📝 <b>Пожелания:</b> {order.special_requests}\n"

        text += f"\n⏰ <b>Создан:</b> {format_datetime_msk(order.created_at)}"
        text += f"\n📊 <b>Статус:</b> {self.get_status_emoji(order.status)}\n"
        text += f"\n\n💰 <b>Сумма:</b> {order.total_price} ₽\n"
        return text

    @staticmethod
    def _format_user_info(user) -> str:
        """Форматирует информацию о пользователе"""
        username = f"@{user.username}" if user.username else "не указан"
        return (
            f"\n👤 <b>Пользователь:</b>\n"
            f"  • Имя: {user.first_name or ''} {user.last_name or ''}\n"
            f"  • Telegram: {username}\n"
            f"  • ID: <code>{user.telegram_id or 'не указан'}</code>\n"
        )

    @staticmethod
    def _format_table_info(table) -> str:
        """Форматирует информацию о столике"""
        text = f"\n🪑 <b>Столик: {table.name}</b>"
        return text

    @staticmethod
    def _format_preset_info(preset) -> str:
        """Форматирует информацию о пресете"""
        text = f"\n"

        if preset.liquid:
            text += f"🧪 <b>Колба:</b> {preset.liquid.name} ({preset.liquid.price} ₽)\n"

        if preset.bowl:
            icon = preset.bowl.icon or ''
            text += f"🥣 <b>Чаша:</b> {preset.bowl.name} {icon} ({preset.bowl.price} ₽)\n"


        if preset.flavors:
            text += f"\n<b>🍓 Вкусы:</b>\n"
            for flavor_item in preset.flavors:
                flavor = flavor_item.flavor
                percent = flavor_item.percent
                brand = f" ({flavor.brand})" if flavor and flavor.brand else ""
                name = flavor.name if flavor else "Неизвестный вкус"
                text += f"  • {name}{brand} — {percent}%\n"

        if preset.strength:
            text += f"\n💨<b>Крепкость:</b> {preset.strength}\n"

        return text

    @staticmethod
    def _format_snapshot_info(snapshot) -> str:
        """Форматирует информацию из снимка заказа"""
        text = f"\n"

        if snapshot.get("preset_flavors"):
            text += f"\n<b>🍓 Вкусы:</b>\n"
            for flavor_item in snapshot["preset_flavors"]:
                flavor = flavor_item.get("flavor", {})
                percent = flavor_item.get("percent", 0)
                flavor_name = flavor.get("name", "Неизвестный вкус")
                brand = flavor.get("brand", "")
                brand_text = f" ({brand})" if brand else ""
                text += f"  • {flavor_name}{brand_text} — {percent}%\n"

        return text
