from fastapi.requests import Request
from sqladmin import ModelView
from sqladmin.fields import QuerySelectMultipleField
from markupsafe import Markup
from wtforms import SelectMultipleField, widgets
from sqlalchemy import select

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
        "created_at": "Дата создания",
        "updated_at": "Дата обновления"
    }

    column_list = [
        DBFlavor.name,
        DBFlavor.brand,
        DBFlavor.categories,
        DBFlavor.is_available,
        DBFlavor.created_at
    ]

    column_searchable_list = [DBFlavor.name, DBFlavor.brand]

    column_sortable_list = [
        DBFlavor.name,
        DBFlavor.brand,
        DBFlavor.is_available,
        DBFlavor.created_at,
        DBFlavor.updated_at
    ]

    column_default_sort = [(DBFlavor.is_available, True), (DBFlavor.name, True)]

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
        """Добавляем CSS и JS для красивого выпадающего списка"""
        request.state.custom_css = add_css_styles() + """
        /* Стили для улучшенного select с множественным выбором */
        .category-select {
            width: 100%;
            padding: 0.375rem 2.25rem 0.375rem 0.75rem;
            font-size: 1rem;
            font-weight: 400;
            line-height: 1.5;
            color: #212529;
            background-color: #fff;
            background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3e%3cpath fill='none' stroke='%23343a40' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='m2 5 6 6 6-6'/%3e%3c/svg%3e");
            background-repeat: no-repeat;
            background-position: right 0.75rem center;
            background-size: 16px 12px;
            border: 1px solid #ced4da;
            border-radius: 0.375rem;
            appearance: none;
        }

        .category-select[multiple] {
            height: auto;
            min-height: 120px;
            background-image: none;
        }

        .category-select option {
            padding: 8px 12px;
            margin: 2px 0;
            border-radius: 4px;
        }

        .category-select option:checked {
            background-color: #0d6efd;
            color: white;
        }

        .category-select optgroup {
            font-weight: bold;
            background-color: #f8f9fa;
        }

        /* Стили для тегов выбранных категорий в форме */
        .select2-container--default .select2-selection--multiple {
            min-height: 120px;
            border: 1px solid #ced4da;
            border-radius: 0.375rem;
        }

        .select2-container--default .select2-selection--multiple .select2-selection__choice {
            background-color: #0d6efd;
            color: white;
            border: none;
            border-radius: 12px;
            padding: 4px 10px;
            margin: 4px;
        }

        .select2-container--default .select2-selection--multiple .select2-selection__choice__remove {
            color: white;
            margin-right: 6px;
        }

        .select2-container--default .select2-selection--multiple .select2-selection__choice__remove:hover {
            color: #dc3545;
            background: none;
        }

        .select2-search__field {
            margin-top: 5px !important;
        }
        """

        request.state.custom_js = add_image_preview_js() + """
        <!-- Подключаем Select2 для красивого выбора с поиском -->
        <link href="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css" rel="stylesheet" />
        <script src="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/i18n/ru.js"></script>

        <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Инициализируем Select2 для поля categories
            setTimeout(function() {
                const categorySelect = document.querySelector('select[name="categories"]');
                if (categorySelect && !categorySelect.classList.contains('select2-hidden-accessible')) {
                    // Сохраняем оригинальные выбранные значения
                    const selectedValues = Array.from(categorySelect.selectedOptions).map(opt => opt.value);

                    $(categorySelect).select2({
                        theme: 'default',
                        language: 'ru',
                        placeholder: 'Выберите категории вкусов',
                        allowClear: false,
                        width: '100%',
                        closeOnSelect: false,
                        dropdownAutoWidth: true
                    });

                    // Восстанавливаем выбранные значения
                    if (selectedValues.length > 0) {
                        $(categorySelect).val(selectedValues).trigger('change');
                    }
                }
            }, 100);
        });

        // Обновляем Select2 после добавления/удаления элементов (для динамических форм)
        document.addEventListener('DOMNodeInserted', function(e) {
            const categorySelect = document.querySelector('select[name="categories"]');
            if (categorySelect && !categorySelect.classList.contains('select2-hidden-accessible')) {
                setTimeout(function() {
                    if ($(categorySelect).data('select2')) {
                        $(categorySelect).select2('destroy');
                    }
                    $(categorySelect).select2({
                        theme: 'default',
                        language: 'ru',
                        placeholder: 'Выберите категории вкусов',
                        allowClear: false,
                        width: '100%',
                        closeOnSelect: false,
                        dropdownAutoWidth: true
                    });
                }, 100);
            }
        });
        </script>
        """

        return await super().on_before_form(request, obj)