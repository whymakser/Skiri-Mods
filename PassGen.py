#     _    _      _                       _     
# ___| | _(_)_ __(_)  _ __ ___   ___   __| |___ 
#/ __| |/ / | '__| | | '_ ` _ \ / _ \ / _` / __|
#\__ \   <| | |  | | | | | | | | (_) | (_| \__ \
#|___/_|\_\_|_|  |_| |_| |_| |_|\___/ \__,_|___/

# meta developer: @skirimods
# license: GNU General Public License v3.0



import random
import string
from .. import loader, utils

@loader.tds
class PassGenMod(loader.Module):
    """Генератор паролей"""
    strings = {"name": "PassGen"}

    async def passgencmd(self, message):
        """<длина> - сгенерировать пароль"""
        length = int(utils.get_args_raw(message)) if utils.get_args_raw(message) else 12
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = "".join(random.choice(chars) for _ in range(length))
        await utils.answer(message, f"🔑 Пароль:\n`{password}`")
