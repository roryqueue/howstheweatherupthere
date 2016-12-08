from django.db import models
from django.core.mail import send_mail

# Create your models here.

class EmailMessage(models.Model):
    subject = models.TextField(null=False, blank=True)
    body = models.TextField(null=False, blank=True)
    recipient = models.TextField(null=False, blank=False)
    from_address = models.TextField(null=False, blank=False)
    successful = models.BooleanField(default=False)
    error = models.TextField()
    traceback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def send(self):
      try:
        successful_sends = send_mail(
          self.subject,
          self.body,
          self.from_address,
          [self.recipient]
        )
        if successful_sends == 0:
          self.success = False
          self.error = """
            send_mail returned 0, indication no successful recipients
          """

      except Exception as e:
        self.success = False
        self.error = str(e)
        self.traceback = traceback.print_exc()

      self.save()