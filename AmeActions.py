#     _    _      _                       _     
# ___| | _(_)_ __(_)  _ __ ___   ___   __| |___ 
#/ __| |/ / | '__| | | '_ ` _ \ / _ \ / _` / __|
#\__ \   <| | |  | | | | | | | | (_) | (_| \__ \
#|___/_|\_\_|_|  |_| |_| |_| |_|\___/ \__,_|___/

# meta developer: @AmekaMods & @SkiriMods
# scope: hikka_only

from hikkatl.types import Message
from .. import utils, loader
import random

@loader.tds
class AmeActions(loader.Module):
    """AmeActions - Модуль для RP-взаимодействий"""
    strings = {
        "name": "AmeActions — Действия",
        "need_reply": "❌ | <b>Команда работает в ответ на сообщение пользователя.</b>",
        "self_action": "❌ | <b>Нельзя выполнить это действие на себе!</b>"
    }

    async def get_username(self, user):
        """Получает username или first_name"""
        return f"@{user.username}" if user.username else user.first_name

    async def rp_action(self, message: Message, action: str, emoji: str, self_msg: str = None):
        """Общая функция для RP-действий"""
        me = await self._client.get_me()
        reply = await message.get_reply_message()
        
        if not reply:
            return await utils.answer(message, self.strings["need_reply"])
            
        if reply.sender_id == me.id:
            msg = self_msg or self.strings["self_action"]
            return await utils.answer(message, msg)
            
        sender = await self.get_username(me)
        target = await self.get_username(reply.sender)
        
        await utils.answer(message, f"{emoji} | <b>{sender} {action} {target}</b>")

    @loader.command()
    async def kiss(self, message: Message):
        """- Поцеловать пользователя"""
        await self.rp_action(
            message,
            "поцеловал(а)",
            "<emoji document_id=5222102889547185747>💋</emoji>",
            "❌ | <b>Самолюбие конечно хорошо, но держи его при себе.</b>"
        )

    @loader.command()
    async def hug(self, message: Message):
        """- Обнять пользователя"""
        await self.rp_action(
            message,
            "обнял(а)",
            "<emoji document_id=5222325171284622461>💘</emoji>",
            "❌ | <b>Кто тебе запрещает обняться с самим собой в реальной жизни?</b>"
        )

    @loader.command()
    async def push(self, message: Message):
        """- Толкнуть пользователя"""
        await self.rp_action(
            message,
            "толкнул(а)",
            "<emoji document_id=5449552292980214333>🙌</emoji>",
            "❌ | <b>Покажи всем как ты толкаешь самого себя.</b>"
        )

    @loader.command()
    async def hit(self, message: Message):
        """- Ударить пользователя"""
        await self.rp_action(
            message,
            "ударил(а)",
            "<emoji document_id=5404854933402965409>💔</emoji>",
            "❌ | <b>Мазохизм не приветствуется.</b>"
        )

    @loader.command()
    async def scold(self, message: Message):
        """- Наругать пользователя"""
        await self.rp_action(
            message,
            "наругал(а)",
            "<emoji document_id=5307772890255876438>👊</emoji>",
            "❌ | <b>Я посмотрю как ты наругаешь самого себя.</b>"
        )

    @loader.command()
    async def kill(self, message: Message):
        """- Убить пользователя"""
        await self.rp_action(
            message,
            "убил(а)",
            "<emoji document_id=5449603119623193071>⚰️</emoji>",
            "❌ | <b>Суицид?</b>"
        )

    @loader.command()
    async def bite(self, message: Message):
        """- Укусить пользователя"""
        await self.rp_action(
            message,
            "укусил(а)",
            "<emoji document_id=5197689837258275092>👄</emoji>",
            "❌ | <b>Это какой-то фетиш?</b>"
        )

    # Новые команды
    @loader.command()
    async def pet(self, message: Message):
        """- Погладить пользователя"""
        await self.rp_action(
            message,
            "погладил(а)",
            "<emoji document_id=5373127970509317126>🐾</emoji>",
            "❌ | <b>Сам себя гладить - странно.</b>"
        )

    @loader.command()
    async def feed(self, message: Message):
        """- Накормить пользователя"""
        foods = ["🍎", "🍕", "🍔", "🍜", "🍫"]
        await self.rp_action(
            message,
            f"накормил(а) {random.choice(foods)}",
            "<emoji document_id=5361837246438794755>🍽️</emoji>",
            "❌ | <b>Сам себя кормить не умеешь?</b>"
        )

    @loader.command()
    async def cry(self, message: Message):
        """- Поплакать на пользователя"""
        await self.rp_action(
            message,
            "заплакал(а) из-за",
            "<emoji document_id=5472100874918517128>😭</emoji>",
            "❌ | <b>Не стоит плакать из-за себя.</b>"
        )

    @loader.command()
    async def dance(self, message: Message):
        """- Потанцевать с пользователем"""
        dances = ["💃", "🕺", "👯", "🎶"]
        await self.rp_action(
            message,
            f"станцевал(а) {random.choice(dances)} с",
            "<emoji document_id=5258010731197455865>✨</emoji>",
            "❌ | <b>Танцуй перед зеркалом.</b>"
        )

    @loader.command()
    async def gift(self, message: Message):
        """- Подарить подарок пользователю"""
        gifts = ["🎁", "🎀", "🎊", "🎉", "💝"]
        await self.rp_action(
            message,
            f"подарил(а) {random.choice(gifts)}",
            "<emoji document_id=5420316241916290636>🎈</emoji>",
            "❌ | <b>Сам себе подарок купи.</b>"
        )

    @loader.command()
    async def marry(self, message: Message):
        """- Пожениться на пользователе"""
        await self.rp_action(
            message,
            "поженился(ась) на",
            "<emoji document_id=5424882251115754249>💍</emoji>",
            "❌ | <b>Самому с собой жениться нельзя.</b>"
        )

    @loader.command()
    async def slap(self, message: Message):
        """- Дать пощечину пользователю"""
        await self.rp_action(
            message,
            "дал(а) пощечину",
            "<emoji document_id=5471995475737885377>👋</emoji>",
            "❌ | <b>Себя бить - последнее дело.</b>"
        )

    @loader.command()
    async def lick(self, message: Message):
        """- Лизнуть пользователя"""
        await self.rp_action(
            message,
            "лизнул(а)",
            "<emoji document_id=5197689837258275092>👅</emoji>",
            "❌ | <b>Фу, лизать себя!</b>"
        )
