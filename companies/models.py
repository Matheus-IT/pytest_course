from django.db import models
from django.utils.timezone import now


class Company(models.Model):
    class Meta:
        verbose_name_plural = "Companies"

    class CompanyStatus(models.TextChoices):
        LAYOFFS = "Layoffs"
        HIRING_FREEZE = "Hiring Freeze"
        HIRING = "Hiring"

    name = models.CharField(max_length=30, unique=True)
    status = models.CharField(
        max_length=30,
        choices=CompanyStatus.choices,
        default=CompanyStatus.HIRING,
    )
    last_update = models.DateTimeField(default=now, editable=True)
    notes = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name
