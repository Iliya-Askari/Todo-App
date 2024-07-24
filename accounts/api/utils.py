import threading
from django.core.mail import send_mail
from django.conf import settings

class EmailThread(threading.Thread):
    def __init__(self, subject, message, recipient_list):
        threading.Thread.__init__(self)
        self.subject = subject
        self.message = message
        self.recipient_list = recipient_list

    def run(self):
        send_mail(
            self.subject,
            self.message,
            settings.DEFAULT_FROM_EMAIL,  # فرض بر این است که این مقدار در تنظیمات تعریف شده است
            self.recipient_list,
            fail_silently=False,
        )
