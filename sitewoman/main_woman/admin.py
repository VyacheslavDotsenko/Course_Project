from django.contrib import admin, messages
from django.db.models.functions import Length
from django.utils.safestring import mark_safe

from .models import Women, Category

class MarriedFilter(admin.SimpleListFilter): # пользовательский фильтр для админ-панели
    title = "Статус женщин"
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('married', 'Замужем'),
            ('single', 'Не замужем')
        ]

    def queryset(self, request, queryset):
        if self.value() == 'married':
            return queryset.filter(husband__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(husband__isnull=True)

@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'content', 'photo', 'post_photo', 'cat', 'husband', 'tags']
    # exclude = ['tags', 'is_published']
    readonly_fields = ['post_photo']
    prepopulated_fields = {"slug": ("title",)}

    filter_horizontal = ['tags']

    list_display = (
    'title', 'post_photo', 'time_create', 'is_published', 'cat')  # поля для отоборажения на панели модели
    list_display_links = ('title',)  # кликабельные поля-ссылки

    ordering = ['-time_create', 'title']  # сортировка записей для админ-панели

    list_editable = ['is_published']

    list_per_page = 10

    actions = ['set_published', 'set_draft']

    search_fields = ["title__startswith", "cat__name"]

    list_filter = [MarriedFilter, "cat__name", "is_published"]

    save_on_top = True

    @admin.display(description="Фото", ordering=Length('content')) # сортировка здесь не нужна, просто пример
    def post_photo(self, women: Women):
        if women.photo:
            return mark_safe(f"<img src='{women.photo.url}' width=50>")
        return "Фото не добавлено"

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.filter(is_published=Women.Status.PUBLISHED).update(is_published=Women.Status.PUBLISHED)

        self.message_user(request, f"Изменено {count} записей")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Women.Status.DRAFT)

        self.message_user(request, f"Снято {count} записей с публикации", messages.WARNING)


# admin.site.register(Women, WomenAdmin)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
