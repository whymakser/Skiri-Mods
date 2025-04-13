#     _    _      _                       _     
# ___| | _(_)_ __(_)  _ __ ___   ___   __| |___ 
#/ __| |/ / | '__| | | '_ ` _ \ / _ \ / _` / __|
#\__ \   <| | |  | | | | | | | | (_) | (_| \__ \
#|___/_|\_\_|_|  |_| |_| |_| |_|\___/ \__,_|___/

# meta developer: @skirimods
# license: GNU General Public License v3.0


from hikkatl.types import Message
from .. import loader, utils
import subprocess
import os
import platform
import logging
from typing import Optional

logger = logging.getLogger(__name__)

@loader.tds
class SkiriPCManagerMod(loader.Module):
    """Удаленное управление ПК через Telegram"""
    strings = {
        "name": "SkiriPCManager",
        "help": "🖥️ <b>Доступные команды:</b>\n\n"
                "• <code>.shutdown</code> - Выключить ПК\n"
                "• <code>.pcrestart</code> - Перезагрузить ПК\n"
                "• <code>.lock</code> - Заблокировать ПК\n"
                "• <code>.screenshot</code> - Сделать скриншот\n"
                "• <code>.cmd [command]</code> - Выполнить команду\n"
                "• <code>.files [path]</code> - Список файлов\n"
                "• <code>.send [path]</code> - Отправить файл\n"
                "• <code>.pchelp</code> - Показать это сообщение",
        "shutdown": "🖥️ Компьютер выключится через 30 секунд",
        "restart": "🔄 Компьютер перезагрузится через 30 секунд",
        "lock": "🔒 Компьютер заблокирован",
        "screenshot": "📸 Скриншот сохранен и отправлен",
        "cmd_result": "📝 <b>Результат команды:</b>\n<code>{}</code>",
        "files_list": "📂 <b>Содержимое {}:</b>\n\n<code>{}</code>",
        "file_sent": "📁 Файл успешно отправлен",
        "file_not_found": "❌ Файл не найден",
        "error": "❌ Ошибка: {}"
    }

    def __init__(self):
        self.os_type = platform.system()
        self.screenshot_path = "telegram_screenshot.png"

    async def client_ready(self, client, db):
        self._client = client
        self._db = db

    async def pchelpcmd(self, message: Message):
        """Показать список команд"""
        await utils.answer(message, self.strings["help"])

    async def shutdowncmd(self, message: Message):
        """Выключить компьютер"""
        try:
            if self.os_type == "Windows":
                os.system("shutdown /s /t 30")
            else:
                os.system("shutdown -h now")
            await utils.answer(message, self.strings["shutdown"])
        except Exception as e:
            await utils.answer(message, self.strings["error"].format(str(e)))

    async def pcrestartcmd(self, message: Message):
        """Перезагрузить компьютер"""
        try:
            if self.os_type == "Windows":
                os.system("shutdown /r /t 30")
            else:
                os.system("reboot")
            await utils.answer(message, self.strings["restart"])
        except Exception as e:
            await utils.answer(message, self.strings["error"].format(str(e)))

    async def lockcmd(self, message: Message):
        """Заблокировать компьютер"""
        try:
            if self.os_type == "Windows":
                os.system("rundll32.exe user32.dll,LockWorkStation")
            elif self.os_type == "Linux":
                os.system("gnome-screensaver-command -l")
            elif self.os_type == "Darwin":
                os.system("/System/Library/CoreServices/Menu\\ Extras/User.menu/Contents/Resources/CGSession -suspend")
            await utils.answer(message, self.strings["lock"])
        except Exception as e:
            await utils.answer(message, self.strings["error"].format(str(e)))

    async def screenshotcmd(self, message: Message):
        """Сделать скриншот экрана"""
        try:
            if self.os_type == "Windows":
                import pyautogui
                pyautogui.screenshot(self.screenshot_path)
            else:
                from mss import mss
                with mss() as sct:
                    sct.shot(output=self.screenshot_path)
            
            await self._client.send_file(
                message.peer_id,
                self.screenshot_path,
                caption="🖥️ Скриншот экрана"
            )
            os.remove(self.screenshot_path)
            await utils.answer(message, self.strings["screenshot"])
        except Exception as e:
            await utils.answer(message, self.strings["error"].format(str(e)))
            logger.exception("Screenshot failed")

    async def cmdcmd(self, message: Message):
        """Выполнить команду в терминале"""
        command = utils.get_args_raw(message)
        if not command:
            await utils.answer(message, "❌ Укажите команду для выполнения")
            return

        try:
            result = subprocess.check_output(
                command,
                shell=True,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                timeout=60
            )
            await utils.answer(
                message,
                self.strings["cmd_result"].format(result[:4000])
            )
        except subprocess.CalledProcessError as e:
            await utils.answer(
                message,
                self.strings["error"].format(e.output[:4000])
            )
        except Exception as e:
            await utils.answer(message, self.strings["error"].format(str(e)))

    async def filescmd(self, message: Message):
        """Показать список файлов"""
        path = utils.get_args_raw(message) or "."
        try:
            files = "\n".join(os.listdir(path))
            await utils.answer(
                message,
                self.strings["files_list"].format(path, files[:4000])
            )
        except Exception as e:
            await utils.answer(message, self.strings["error"].format(str(e)))

    async def sendcmd(self, message: Message):
        """Отправить файл"""
        file_path = utils.get_args_raw(message)
        if not file_path:
            await utils.answer(message, "❌ Укажите путь к файлу")
            return

        try:
            if os.path.exists(file_path):
                await self._client.send_file(
                    message.peer_id,
                    file_path,
                    caption=f"📁 Файл: {os.path.basename(file_path)}"
                )
                await utils.answer(message, self.strings["file_sent"])
            else:
                await utils.answer(message, self.strings["file_not_found"])
        except Exception as e:
            await utils.answer(message, self.strings["error"].format(str(e)))
