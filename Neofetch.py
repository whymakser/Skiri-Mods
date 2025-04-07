#     _    _      _                       _     
# ___| | _(_)_ __(_)  _ __ ___   ___   __| |___ 
#/ __| |/ / | '__| | | '_ ` _ \ / _ \ / _` / __|
#\__ \   <| | |  | | | | | | | | (_) | (_| \__ \
#|___/_|\_\_|_|  |_| |_| |_| |_|\___/ \__,_|___/

# meta developer: @skirimods
# license: GNU General Public License v3.0


# Уйди нахуй отсюда!






from hikkatl.types import Message
from hikkatl.errors import RPCError
from .. import loader, utils
import subprocess

@loader.tds
class NeofetchMod(loader.Module):
    """Выводит результат neofetch --stdout"""
    strings = {"name": "Neofetch"}

    async def neofetchcmd(self, message: Message):
        """Запустить neofetch и отправить результат"""
        try:
            result = subprocess.run(
                ["neofetch", "--stdout"],
                capture_output=True,
                text=True,
                check=True
            )
            output = result.stdout
        except FileNotFoundError:
            output = "❌ Neofetch не установлен!\nУстановите: apt install neofetch (Linux/Android)"
        except Exception as e:
            output = f"❌ Ошибка: {e}"

        # Отправляем как код (используем Markdown или Telethon-форматирование)
        await utils.answer(
            message,
            f"```\n{output}\n```",  # Блок кода в Markdown
            parse_mode="Markdown"
        )
