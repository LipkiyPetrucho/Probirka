from django.contrib import admin

from .models import Section, Subsection, Test, AdditionalService


class SubsectionInline(admin.TabularInline):
    model = Subsection
    extra = 1
    fields = ("name", "description")
    show_change_link = True


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [SubsectionInline]


@admin.register(Subsection)
class SubsectionAdmin(admin.ModelAdmin):
    list_display = ("name", "section")
    list_filter = ("section",)
    search_fields = ("name",)


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ("name", "section", "subsection", "price", "additional_service")
    list_filter = (
        "section",
        ("subsection", admin.RelatedOnlyFieldListFilter),
        "additional_service",
    )
    search_fields = ("name",)
    autocomplete_fields = ("section", "subsection", "additional_service")


@admin.register(AdditionalService)
class AdditionalServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price")
    search_fields = ("name",)
