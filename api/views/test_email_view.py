from django.http import JsonResponse
from django.core.mail import send_mail, get_connection
from django.views import View
from api.models.smtp_model import EmailSettings

class TestEmailView(View):
    def get(self, request, *args, **kwargs):
        email_settings = EmailSettings.objects.first()
        if not email_settings:
            return JsonResponse({'status': 'error', 'message': 'No email settings found.'}, status=400)

        try:
            connection = get_connection(
                backend=email_settings.email_backend,
                host=email_settings.email_host,
                port=email_settings.email_port,
                username=email_settings.email_host_user,
                password=email_settings.email_host_password,
                use_tls=email_settings.email_use_tls
            )
            send_mail(
                'Test Email',
                'This is a test email.',
                email_settings.default_from_email,
                [email_settings.email_host_user],
                connection=connection
            )
            return JsonResponse({'status': 'success', 'message': 'Test email sent successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error sending test email: {e}'}, status=500)
