from hikkatl.types import Message
from .. import loader, utils
import asyncio
import logging
import re

logger = logging.getLogger(__name__)

@loader.tds
class SpeedTestMod(loader.Module):
    """Проверка скорости интернета"""
    strings = {
        "name": "SpeedTest",
        "testing": "🔄 Запускаю тест скорости...",
        "result": "📊 <b>Результаты SpeedTest:</b>\n\n{result}",
        "error": "❌ Ошибка: {error}",
        "not_installed": "❌ speedtest-cli не установлен\n\nУстановите:\n<code>pip install speedtest-cli</code>"
    }

    async def client_ready(self, client, db):
        self._client = client
        self._db = db

    async def speedtestcmd(self, message: Message):
        """Запустить тест скорости"""
        try:
            await utils.answer(message, self.strings["testing"])

            # Проверяем доступность speedtest-cli
            proc = await asyncio.create_subprocess_shell(
                "speedtest --version",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await proc.communicate()

            if proc.returncode != 0:
                await utils.answer(message, self.strings["not_installed"])
                return

            # Запускаем тест скорости
            proc = await asyncio.create_subprocess_shell(
                "speedtest --simple",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()

            if proc.returncode != 0:
                error = stderr.decode().strip() or "Неизвестная ошибка"
                raise Exception(error)

            # Форматируем результат
            result = stdout.decode().strip()
            formatted = re.sub(
                r"(Ping|Download|Upload):\s+(.*)",
                lambda m: f"• <b>{m.group(1)}:</b> {m.group(2)}",
                result
            )

            await utils.answer(
                message,
                self.strings["result"].format(result=formatted)
            )

        except Exception as e:
            logger.exception("Speedtest failed")
            await utils.answer(
                message,
                self.strings["error"].format(error=str(e))
            )