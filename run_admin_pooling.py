import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tennis_bot.settings")
django.setup()

from admin_bot.main import main

if __name__ == "__main__":
    main()
