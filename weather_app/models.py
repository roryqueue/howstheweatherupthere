from django.db import models
from django.core.mail import send_mail

# Create your models here.

class Location(models.Model):
    city = models.TextField(null=False, blank=True)
    state = models.TextField(null=False, blank=True)
    wunderground_url_format = models.TextField(null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  


class User(models.Model):
    email = models.TextField(null=False, blank=False)
    password = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL)


class EmailMessage(models.Model):
    subject = models.TextField(null=False, blank=True)
    body = models.TextField(null=False, blank=True)
    from_address = models.TextField(null=False, blank=False)
    successful = models.BooleanField(default=False)
    error = models.TextField()
    traceback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)

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
