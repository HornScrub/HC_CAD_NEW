from django.core.management.base import BaseCommand
from calls.models import Call, CallInteraction
from django.conf import settings

class Command(BaseCommand):
    help = "Cleans up test data from the test database"

    def handle(self, *args, **kwargs):
        if settings.DATABASES['default']['NAME'] == 'test_dispatch_db':
            self.stdout.write("⚠️ Using test database. Proceeding with cleanup.")
            CallInteraction.objects.all().delete()
            Call.objects.all().delete()
            self.stdout.write("✅ Test database cleaned successfully.")
        else:
            self.stdout.write("❌ Not using the test database! Cleanup aborted.")
