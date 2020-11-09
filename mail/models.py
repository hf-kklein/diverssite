from django.db import models
from django.conf import settings
from django.core.mail import send_mail


# Create your models here.


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.PROTECT,
                                 related_name="message_sender_set")
    recipients = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name="message_recipients_set")
    subject = models.CharField(max_length=100)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    attachment = models.FileField()
    sent = models.BooleanField(default=False)

    def send(self):
        recipient_mails = [r.email for r in self.recipients.all()]

        send_mail(subject=self.subject, message=self.body,
                  from_email='ultimail@saxy-divers.de',
                  recipient_list=recipient_mails)

        self.sent = True

        self.save()

    def __str__(self):
        return self.subject
