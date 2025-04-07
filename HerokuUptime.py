#     _    _      _                       _     
# ___| | _(_)_ __(_)  _ __ ___   ___   __| |___ 
#/ __| |/ / | '__| | | '_ ` _ \ / _ \ / _` / __|
#\__ \   <| | |  | | | | | | | | (_) | (_| \__ \
#|___/_|\_\_|_|  |_| |_| |_| |_|\___/ \__,_|___/

# meta developer: @skirimods
# license: GNU General Public License v3.0


# Уйди нахуй отсюда!

import time
import random
from datetime import timedelta
from hikka import loader, utils

@loader.tds
class HerokuUptimeMod(loader.Module):
    """Показывает аптайм Heroku (самый ненужный модуль по мнению автора)"""

    strings = {
        "name": "HerokuUptime",
        "uptime": "🖥️ Heroku работает уже: {}",
        "phrases": (
            "🖥️ Heroku работает уже: {}",

        )
    }

    async def client_ready(self, client, db):
        self.start_time = time.time()

    @loader.unrestricted
    async def uptimecmd(self, message):
        """Показать аптайм Heroku"""
        uptime = timedelta(seconds=int(time.time() - self.start_time))
        uptime_str = str(uptime)
        
        response = random.choice([
            self.strings["uptime"].format(uptime_str),
            *[p.format(uptime_str) for p in self.strings["phrases"]]
        ])
        
        await utils.answer(message, response)
