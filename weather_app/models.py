import traceback
from django.db import models
from django.core.mail import send_mail


class Location(models.Model):
    city = models.TextField(null=False, blank=False, unique=True)
    state = models.TextField(null=False, blank=False)
    state_abbreviation = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  
    
    def __str__(self):
        return '{}, {}'.format(self.city, self.state_abbreviation)

    class Meta:
        ordering = ('city',)


class User(models.Model):
    email = models.CharField(max_length=100, null=False, blank=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL)


class EmailMessage(models.Model):
    subject = models.TextField(null=False, blank=True)
    body = models.TextField(null=False, blank=True)
    from_address = models.TextField(null=False, blank=False)
    successful = models.BooleanField(default=False)
    error = models.TextField(null=True)
    traceback = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)

    def send(self):
        try:
            successful_sends = send_mail(
                self.subject,
                self.body,
                self.from_address,
                [self.recipient.email]
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
