from django.db import models

class Conversation(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    history = models.JSONField(default=list)

    def __str__(self):
        return self.title if self.title else f"Conversation {self.id}"
