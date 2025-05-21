from django.db import models
from django.utils.translation import gettext_lazy as _


class ContactMessage(models.Model):
    """Сообщение, отправленное через форму обратной связи."""
    name = models.CharField(_('sender name'), max_length=100)
    email = models.EmailField(_('email'))
    message = models.TextField(_('message'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    is_processed = models.BooleanField(_('processed'), default=False)

    class Meta:
        verbose_name = _('Contact message')
        verbose_name_plural = _('Contact messages')
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'{self.name} <{self.email}> ({self.created_at:%d.%m.%Y})'
