from django.db import models


class LowerEmailField(models.EmailField):
    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value is not None:
            value = value.lower()

        return value


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
