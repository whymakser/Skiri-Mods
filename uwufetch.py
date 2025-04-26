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
class UwUFetchMod(loader.Module):
    """Кавайное отображение uwufetch"""

    strings = {
        "name": "UwUFetch",
        "fetching": "(⁠｡⁠♡⁠‿⁠♡⁠｡⁠) Nya~~, получаю информацию о твоем сервере <3",
        "not_installed": (
            "❌ uwufetch не установлен!\n"
            "Установите:\n"
            "<code>sudo pacman -S uwufetch</code>\n"
            "Или соберите из исходников:\n"
            "<code>git clone https://github.com/TheDarkBug/uwufetch.git</code>\n"
            "<code>cd uwufetch && make build && sudo make install</code>"
        )
    }

    async def client_ready(self, client, db):
        self._db = db
        self._client = client

    def clean_ansi(self, text: str) -> str:
        """Удаляет ANSI escape последовательности"""
        return re.sub(r'\x1B\[[0-9;]*[mGABCDHJKf]?', '', text)

    @loader.command()
    async def uwufetch(self, message: Message):
        """- Показать системную информацию в кавайном стиле"""
        await utils.answer(message, self.strings["fetching"])

        try:
            # Простой вызов uwufetch без дополнительных параметров
            result = subprocess.run(
                ["uwufetch"],
                capture_output=True,
                text=True,
                check=True
            ).stdout

            clean_result = self.clean_ansi(result)

            response = (
                "→ <b>uwufetch</b>\n\n"
                "<blockquote>\n"
                f"{clean_result.strip()}"
                "</blockquote>\n\n"
            )

            await utils.answer(message, response)
        except subprocess.CalledProcessError as e:
            await utils.answer(message, f"❌ Ошибка: {e.stderr.strip()}")
        except FileNotFoundError:
            await utils.answer(message, self.strings["not_installed"])
        except Exception as e:
            await utils.answer(message, f"❌ Неизвестная ошибка: {str(e)}")
