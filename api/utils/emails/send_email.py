from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from api.models.smtp_model import EmailSettings

class EmailSender:
    def __init__(self, subject, to, template_name, context):
        self.subject = subject
        self.to = to
        self.template_name = template_name
        self.context = context
        self.email_settings = EmailSettings.objects.first()

    def send_email(self):
        if not self.email_settings:
            raise Exception("Email settings are not configured.")

        html_content = render_to_string(f'emails/{self.template_name}', self.context)
        text_content = strip_tags(html_content)

        connection = get_connection(
            backend=self.email_settings.email_backend,
            host=self.email_settings.email_host,
            port=self.email_settings.email_port,
            username=self.email_settings.email_host_user,
            password=self.email_settings.email_host_password,
            use_tls=self.email_settings.email_use_tls
        )

        email = EmailMultiAlternatives(
            subject=self.subject,
            body=text_content,
            from_email=self.email_settings.default_from_email,
            to=[self.to],
            connection=connection
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
