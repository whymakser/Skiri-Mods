#     _    _      _                       _     
# ___| | _(_)_ __(_)  _ __ ___   ___   __| |___ 
#/ __| |/ / | '__| | | '_ ` _ \ / _ \ / _` / __|
#\__ \   <| | |  | | | | | | | | (_) | (_| \__ \
#|___/_|\_\_|_|  |_| |_| |_| |_|\___/ \__,_|___/

# meta developer: @skirimods
# license: GNU General Public License v3.0


from hikkatl.types import Message
from hikkatl.tl.functions.account import UpdateProfileRequest
from .. import loader, utils
import time

@loader.tds
class SkiriAFK(loader.Module):
    """Улучшенный AFK модуль с фиксом восстановления имени"""
    strings = {"name": "SkiriAFK"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "afk_message",
                "🌀 <b>Я в AFK!</b>\n<b>Причина:</b> <i>{reason}</i>",
                "Сообщение при активации",
                validator=loader.validators.String()
            ),
            loader.ConfigValue(
                "name_prefix",
                "[AFK] ",
                "Префикс для имени",
                validator=loader.validators.String()
            )
        )
        self.notified_chats = set()
        self.original_first_name = ""
        self.original_last_name = ""

    async def client_ready(self, client, db):
        self._db = db
        self._client = client
        me = await client.get_me()
        self.original_first_name = me.first_name
        self.original_last_name = me.last_name or ""

    async def update_name(self, afk: bool):
        """Обновляет имя с префиксом или восстанавливает оригинал"""
        new_first = f"{self.config['name_prefix']}{self.original_first_name}" if afk else self.original_first_name
        await self._client(UpdateProfileRequest(
            first_name=new_first,
            last_name=self.original_last_name
        ))

    async def afkcmd(self, message: Message):
        """Активировать AFK режим"""
        reason = utils.get_args_raw(message) or "Не указана"
        self._db.set(__name__, "afk", True)
        self._db.set(__name__, "reason", reason)
        self._db.set(__name__, "time", time.time())
        self.notified_chats.clear()
        
        await self.update_name(True)
        await utils.answer(
            message,
            self.config["afk_message"].format(reason=reason)
        )

    async def unafkcmd(self, message: Message):
        """Деактивировать AFK режим"""
        if not self._db.get(__name__, "afk"):
            await utils.answer(message, "❌ Я и так не в AFK!")
            return
        
        duration = self.format_duration(time.time() - self._db.get(__name__, "time"))
        self._db.set(__name__, "afk", False)
        
        await self.update_name(False)  # Важное исправление здесь
        await utils.answer(
            message,
            f"✨ <b>Я вернулся!</b>\n⏱ <b>Отсутствовал:</b> <i>{duration}</i>"
        )

    def format_duration(self, seconds: float) -> str:
        """Форматирует время в ЧЧ:ММ:СС"""
        hours, remainder = divmod(int(seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    async def watcher(self, message: Message):
        """Обработчик сообщений"""
        if not isinstance(message, Message) or not self._db.get(__name__, "afk"):
            return

        chat_id = utils.get_chat_id(message)
        if chat_id in self.notified_chats:
            return

        sender = getattr(message, "sender", None)
        me = await self._client.get_me()
        if not sender or sender.id == me.id:
            return

        mentioned = me.username and f"@{me.username}" in (message.text or "").lower()
        is_pm = message.is_private

        if mentioned or is_pm:
            reason = self._db.get(__name__, "reason", "Не указана")
            duration = self.format_duration(time.time() - self._db.get(__name__, "time"))
            
            await message.reply(
                f"⚡ <b>Я в AFK!</b>\n"
                f"📌 <b>Причина:</b> <i>{reason}</i>\n"
                f"⏳ <b>Прошло:</b> <i>{duration}</i>"
            )
            self.notified_chats.add(chat_id)

    async def on_unload(self):
        """Гарантированное восстановление имени при выгрузке"""
        if self._db.get(__name__, "afk"):
            await self.update_name(False)
