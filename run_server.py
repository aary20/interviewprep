import os
import sys

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'interviewprep.settings')

# Try to avoid importing problematic packages
sys.path = [p for p in sys.path if 'pyresparser' not in p]

try:
    import django
    django.setup()
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'runserver'])
except Exception as e:
    print(f"Error: {e}")
