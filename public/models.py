from django.db import models
from django.core.exceptions import ValidationError

class Info(models.Model):
    welcome_title = models.TextField(blank=True, null=True)
    welcome_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.welcome_title

    def save(self, *args, **kwargs):
        if not self.pk and Info.objects.exists():
        # if you'll not check for self.pk 
        # then error will also raised in update of exists model
            raise ValidationError('Nur bestehender Eintrag kann geändert werden')
        return super(Info, self).save(*args, **kwargs)