from .bowl import BowlAdmin
from .flavor import FlavorAdmin
from .flavor_categories import FlavorCategoryAdmin
from .user import UserAdmin
from .liquid import LiquidAdmin
from .preset import PresetAdmin
from .preset_flavor import PresetFlavorAdmin
from .settings import SettingsAdmin
from .table import TableAdmin
from .order import OrderAdmin

__all__ = [
    "BowlAdmin",
    "FlavorAdmin",
    "UserAdmin",
    "LiquidAdmin",
    "PresetAdmin",
    "PresetFlavorAdmin",
    "FlavorCategoryAdmin",
    "TableAdmin",
    "OrderAdmin",
    "SettingsAdmin",
]