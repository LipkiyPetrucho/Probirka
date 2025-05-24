from django.contrib import admin

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at", "short_msg", "is_processed")
    list_filter = ("is_processed", "created_at")
    readonly_fields = ("name", "email", "message", "created_at")
    search_fields = ("name", "email")
    actions = ["mark_as_processed"]

    def short_msg(self, obj):
        return (obj.message[:60] + "…") if len(obj.message) > 60 else obj.message

    short_msg.short_description = "Message"

    @admin.action(description="Mark selected messages as processed")
    def mark_as_processed(self, request, queryset):
        updated = queryset.update(is_processed=True)
        self.message_user(request, f"{updated} message(s) marked as processed")

        # Отключаем добавление новых сообщений вручную — только просмотр

    def has_add_permission(self, request):
        return False
