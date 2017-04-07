import os
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.rxncon_site.settings")

from django.core.management import call_command
from django.core.wsgi import get_wsgi_application 
application = get_wsgi_application()
call_command('runserver',  '127.0.0.1:8000')	
