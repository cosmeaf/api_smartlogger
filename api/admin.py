from django.contrib import admin, messages
from django.core.mail import send_mail, get_connection
from django.shortcuts import redirect
from django.urls import path
from api.models.smtp_model import EmailSettings

@admin.register(EmailSettings)
class EmailSettingsAdmin(admin.ModelAdmin):
    list_display = ['email_backend', 'email_service', 'email_host', 'email_host_user', 'default_from_email']
    change_list_template = 'admin/email_settings_changelist.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('test-email/', self.admin_site.admin_view(self.test_email), name='test-email'),
        ]
        return custom_urls + urls

    def test_email(self, request):
        email_settings = EmailSettings.objects.first()
        if not email_settings:
            self.message_user(request, "No email settings found.", level=messages.ERROR)
            return redirect('..')

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
            self.message_user(request, "Test email sent successfully.", level=messages.SUCCESS)
        except Exception as e:
            self.message_user(request, f"Error sending test email: {e}", level=messages.ERROR)

        return redirect('..')
