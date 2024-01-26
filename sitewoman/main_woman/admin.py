from django.contrib import admin, messages
from django.db.models.functions import Length

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
    fields = ['title', 'slug', 'content', 'cat', 'husband', 'tags']
    # exclude = ['tags', 'is_published']
    # readonly_fields = ['slug']
    prepopulated_fields = {"slug": ("title",)}

    filter_horizontal = ['tags']

    list_display = (
    'title', 'time_create', 'is_published', 'cat', 'brief_info')  # поля для отоборажения на панели модели
    list_display_links = ('title',)  # кликабельные поля-ссылки

    ordering = ['-time_create', 'title']  # сортировка записей для админ-панели

    list_editable = ['is_published']

    list_per_page = 10

    actions = ['set_published', 'set_draft']

    search_fields = ["title__startswith", "cat__name"]

    list_filter = [MarriedFilter, "cat__name", "is_published"]

    @admin.display(description="Краткое описание", ordering=Length('content'))
    def brief_info(self, women: Women):
        return f"Описание {len(women.content.split())} слов"

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
