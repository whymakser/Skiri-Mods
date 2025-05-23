#--------------------------------------------------
#|      _    _      _                       _     |
#|  ___| | _(_)_ __(_)  _ __ ___   ___   __| |___ |
#| / __| |/ / | '__| | | '_ ` _ \ / _ \ / _` / __||
#| \__ \   <| | |  | | | | | | | | (_) | (_| \__ \|
#| |___/_|\_\_|_|  |_| |_| |_| |_|\___/ \__,_|___/|
#--------------------------------------------------

# meta developer: @skirimods
# license: GNU General Public License v3.0


import subprocess
import re
from .. import loader, utils
from telethon.tl.types import Message

@loader.tds
class FastFetchMod(loader.Module):
    """Красивое отображение fastfetch с дизайном"""

    strings = {
        "name": "FastFetch",
        "fetching": "🔄 Получаю информацию о системе..."
    }

    async def client_ready(self, client, db):
        self._db = db
        self._client = client

    @loader.command()
    async def ffetch(self, message: Message):
        """- Показать системную информацию в стильном оформлении"""
        await utils.answer(message, self.strings["fetching"])

        try:
            # Запускаем fastfetch с компактным режимом и цветами
            result = subprocess.run(
                ["fastfetch", "--logo-color-1", "blue", "--logo-color-2", "cyan", "-L", "none"],
                capture_output=True,
                text=True,
                check=True
            ).stdout

            # Убираем управляющие последовательности ANSI
            clean_result = re.sub(r'\x1B\[[0-9;]*[mGABCDHJKf]?', '', result)

            # Создаем красивое оформление
            response = (
                "→ <b>fastfetch</b>\n\n"
                "<blockquote>\n"
                f"{clean_result.strip()}"
                "</blockquote>\n\n"
            )

            await utils.answer(message, response)
        except subprocess.CalledProcessError as e:
            await utils.answer(message, f"❌ Ошибка: {e.stderr.strip()}")
        except FileNotFoundError:
            await utils.answer(message, "❌ fastfetch не установлен!\nУстановите: <code>sudo apt install fastfetch</code>")

    @loader.command()
    async def fflarge(self, message: Message):
        """- Подробная системная информация"""
        await utils.answer(message, self.strings["fetching"])

        try:
            # Полная версия с анимированным лого
            result = subprocess.run(
                ["fastfetch", "--logo-color-1", "magenta", "--logo-color-2", "cyan"],
                capture_output=True,
                text=True,
                check=True
            ).stdout

            # Убираем управляющие последовательности ANSI
            clean_result = re.sub(r'\x1B\[[0-9;]*[mGABCDHJKf]?', '', result)

            response = (
                "→ <b>fastfetch</b>\n\n"
                "<blockquote>\n"
                f"{clean_result.strip()}"
                "</blockquote>\n\n"
            )

            await utils.answer(message, response)
        except subprocess.CalledProcessError as e:
            await utils.answer(message, f"❌ Ошибка: {e.stderr.strip()}")
        except FileNotFoundError:
            await utils.answer(message, "❌ fastfetch не установлен!\nУстановите: <code>sudo apt install fastfetch</code>")
        except Exception as e:
            await utils.answer(message, f"❌ Неизвестная ошибка: {str(e)}")
          
