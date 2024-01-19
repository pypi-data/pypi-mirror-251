import json

import requests
from django.conf import settings
from django.core.management import BaseCommand

from oscarbot.bot import Bot
from oscarbot.services import get_bot_model
from oscarbot.views import handle_content


class Command(BaseCommand):

    def handle(self, *args, **options):
        bot_model = get_bot_model()
        bot_object = bot_model.objects.all().first()
        bot = Bot(bot_object.token)
