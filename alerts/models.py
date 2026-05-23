from django.db import models
from django.conf import settings

class EmergencyAlert(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    sms_sent_count = models.IntegerField(default=0)

    def __str__(self):
        return f"ALERT: {self.title}"
