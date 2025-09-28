import csv
from django.core.management.base import BaseCommand
from my_profile.models import NotificationDeliveryLog

class Command(BaseCommand):
    help = 'Export notification delivery logs to CSV for compliance.'

    def add_arguments(self, parser):
        parser.add_argument('--output', type=str, default='notification_delivery_logs.csv', help='Output CSV file path')

    def handle(self, *args, **options):
        output_path = options['output']
        logs = NotificationDeliveryLog.objects.all().select_related('notification')
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'NotificationID', 'User', 'Message', 'AttemptTime', 'Status', 'Channel', 'ErrorMessage', 'UserAgent', 'IPAddress'
            ])
            for log in logs:
                writer.writerow([
                    log.notification.id,
                    log.notification.user.username,
                    log.notification.message,
                    log.attempt_time,
                    log.status,
                    log.channel,
                    log.error_message,
                    log.user_agent,
                    log.ip_address,
                ])
        self.stdout.write(self.style.SUCCESS(f'Exported {logs.count()} logs to {output_path}'))
