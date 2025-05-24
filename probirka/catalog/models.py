from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Section(models.Model):
    """Верхнеуровневая категория анализов"""

    name = models.CharField(_("name"), max_length=255, unique=True)
    slug = models.SlugField(_("slug"), max_length=255, unique=True)
    description = models.TextField(_("description"), blank=True)

    class Meta:
        verbose_name = _("Section")
        verbose_name_plural = _("Sections")
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self) -> str:
        return self.name


class Subsection(models.Model):
    """Подкатегория, принадлежащая конкретному разделу"""

    name = models.CharField(_("name"), max_length=255)
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name="subsections",
        verbose_name=_("section"),
    )
    description = models.TextField(_("description"), blank=True)

    class Meta:
        verbose_name = _("Subsection")
        verbose_name_plural = _("Subsections")
        unique_together = ("section", "name")
        ordering = ["section__name", "name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["section"]),
        ]

    def __str__(self) -> str:
        return f"{self.section} / {self.name}"


class AdditionalService(models.Model):
    """Справочник дополнительных услуг"""

    name = models.CharField(_("name"), max_length=255, unique=True)
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2)
    description = models.TextField(_("description"), blank=True)

    class Meta:
        verbose_name = _("Additional service")
        verbose_name_plural = _("Additional services")
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self) -> str:
        return f"{self.name} — {self.price} ₽"


class Test(models.Model):
    """Медицинский анализ"""

    name = models.CharField(_("name"), max_length=512)
    biomaterial = models.CharField(_("biomaterial"), max_length=255)
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2)
    section = models.ForeignKey(
        "Section",
        on_delete=models.PROTECT,
        related_name="tests",
        verbose_name=_("section"),
    )
    subsection = models.ForeignKey(
        "Subsection",
        on_delete=models.PROTECT,
        related_name="tests",
        verbose_name=_("subsection"),
        blank=True,
        null=True,
    )
    additional_service = models.ForeignKey(
        "AdditionalService",
        on_delete=models.SET_NULL,
        related_name="tests",
        verbose_name=_("additional service"),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Test")
        verbose_name_plural = _("Tests")
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["section"]),
            models.Index(fields=["subsection"]),
        ]

    def clean(self):
        """
        Правила согласованности:
        1. subsection, если указан, должен относиться к тому же section.
        2. Нужно заполнить хотя бы subsection или section (section всегда обязателен).
        """
        # (1) Если подраздел указан, проверяем, что он под тем же разделом
        if self.subsection and self.subsection.section_id != self.section_id:
            raise ValidationError(
                {"subsection": _("Subsection does not belong to the selected section.")}
            )

    def __str__(self) -> str:
        return self.name
