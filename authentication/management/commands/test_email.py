from django.core.management.base import BaseCommand
from django.core.mail import send_mail

class Command(BaseCommand):
    help = 'Test email sending'

    def handle(self, *args, **kwargs):
        try:
            send_mail(
                "Test Email from Devsplug",
                "This is a test email from Devsplug.",
                "noreply@devsplug.com",
                ["info@paullilian.dev"],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS('Successfully sent test email'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to send email: {str(e)}')) 