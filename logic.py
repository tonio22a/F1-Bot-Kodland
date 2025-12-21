# тут вспомогательные функции
from config import F1_TEAMS_2026
import math
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot_instance import *

bot = telebot.TeleBot(BOT_TOKEN)

def get_team_display_name(team_key):
    """получить красивое название команды с эмодзи"""
    team = F1_TEAMS_2026.get(team_key, {})
    emoji = team.get('emoji', '🏎️')
    return f"{emoji} {team_key.title()}"

def get_team_info_text(team_key):
    """получить текст с информацией о команде"""
    team = F1_TEAMS_2026.get(team_key)
    if not team:
        return "Команда не найдена"
    
    drivers = ", ".join(team['drivers'])
    
    return f"""{team['emoji']} **{team_key.title()}**

📜 *История команды:*
{team['history']}

👥 *Пилоты (2026 сезон):* {drivers}
🏆 *Конструкторские чемпионства:* {team['championships']}
⚙️ *Двигатель:* {team['engine']}
💰 *Бюджет:* {team['budget']}
🎯 *Ожидания руководства:* {team['expectations']}

Готовы стать менеджером этой команды?"""

###############################

parameparameters = { #начальные настройки болида
    "aerodynamics": 75,
    "engine": 80,
    "chassis": 90,
    "reliability": 80
}

values = parameparameters.values()

srz = sum(values) / len(values)

car_quality = round(srz) - 1 # качество болида

textcarqual = f'Качество болида: {car_quality:.1f}'

##############################################

def aerosettings(call):
    """настройки аэродинамики"""
    markup = InlineKeyboardMarkup(row_width=2)

    frontwing_btn = InlineKeyboardButton('🪽 Переднее антикрыло', callback_data='frontwing_btn')
    backwing_btn = InlineKeyboardButton('🪽 Заднее антикрыло', callback_data='backwing_btn')
    effect_btn = InlineKeyboardButton('💯 Эффективность', callback_data='effect_btn')
    brake_btn = InlineKeyboardButton('🍃 Тормозные воздуховоды', callback_data='brake_btn')
    back_btn = InlineKeyboardButton('🔙 Назад', callback_data='develop_back')
    
    markup.add(frontwing_btn, backwing_btn, effect_btn, brake_btn, back_btn)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="🌀 *Настройки аэродинамики*\n\n"
             "Выберите элемент для улучшения:\n\n"
             "• 🪽 Переднее антикрыло - баланс машины\n"
             "• 🪽 Заднее антикрыло - прижимная сила\n"
             "• 💯 Эффективность - общая аэродинамика\n"
             "• 🍃 Тормозные воздуховоды - охлаждение тормозов",
        reply_markup=markup,
        parse_mode='Markdown'
    )

def enginesettings(call):
    """настройки двигателя"""
    markup = InlineKeyboardMarkup(row_width=2)

    buyengine_btn = InlineKeyboardButton('💰 Приобрести', callback_data='buyengine_btn')
    back_btn = InlineKeyboardButton('🔙 Назад', callback_data='develop_back')
    
    markup.add(buyengine_btn, back_btn)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="⚙️ *Настройки двигателя*\n\n"
             "Вы можете приобрести двигатель по кнопке ниже. Там у вас будет возможность выбрать тип мотора - Режим скорости, режим защиты, баланс\n\n",
        reply_markup=markup,
        parse_mode='Markdown')
    
def chassissettings(call):
    """настройки шасси"""
    markup = InlineKeyboardMarkup(row_width=2)

    buyengine_btn = InlineKeyboardButton('💰 Приобрести', callback_data='buyengine_btn')
    back_btn = InlineKeyboardButton('🔙 Назад', callback_data='develop_back')
    
    markup.add(buyengine_btn, back_btn)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="🔩 *Настройки шасси*\n\n"
             "Вы можете приобрести новые шасси по кнопке ниже",
        reply_markup=markup,
        parse_mode='Markdown')
    