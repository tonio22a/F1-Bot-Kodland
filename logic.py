from config import F1_TEAMS_2026, user_teams, user_data, mailbox
import math
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot_instance import *
import random

bot = telebot.TeleBot(BOT_TOKEN)

TRACKS = [
    {"name": "Бахрейн", "circuit": "Сахир", "laps": 57, "length": 5.412},
    {"name": "Италия", "circuit": "Монца", "laps": 53, "length": 5.793},
    {"name": "Монако", "circuit": "Монте-Карло", "laps": 78, "length": 3.337},
    {"name": "Япония", "circuit": "Сузука", "laps": 53, "length": 5.807}
]

RACE_EVENTS = [
    ("🏎️", "Отличный старт", 2),
    ("💥", "Авария в первом повороте", -3),
    ("🔄", "Удачный обгон", 1),
    ("🔧", "Проблемы с тормозами", -2),
    ("💨", "Установил быстрейший круг!", 2),
    ("⛈️", "Пошел дождь", 0),
    ("🛑", "Выезд безопасности", 0),
    ("🔥", "Пожар на пит-стопе", -4),
    ("🎯", "Идеальная стратегия", 3),
    ("⚡", "Обогнал двух соперников", 2)
]

def get_car_rating(car_params):
    values = car_params.values()
    return round(sum(values) / len(values))

def calculate_improvement_cost(current_value, improvement_amount, param_name):
    """Рассчитывает стоимость улучшения в зависимости от текущего уровня"""
    base_costs = {
        'aerodynamics': 1000000,  # 1 млн базовая стоимость
        'engine': 2000000,        # 2 млн базовая стоимость
        'chassis': 1500000,       # 1.5 млн базовая стоимость
        'reliability': 800000     # 800к базовая стоимость
    }
    
    base_cost = base_costs.get(param_name, 1000000)
    
    # Чем выше текущий уровень, тем дороже улучшение
    multiplier = 1 + (current_value / 100) * 2  # От 1x до 3x
    
    # Чем больше улучшение, тем дороже
    improvement_multiplier = 1 + (improvement_amount / 10)
    
    cost = base_cost * multiplier * improvement_multiplier
    
    # Округляем до 100к
    return round(cost / 100000) * 100000

def simulate_race(user_id):
    if user_id not in user_data:
        return None
    
    user_team = user_data[user_id]['team']
    user_car = user_data[user_id]['car_params']
    user_rating = get_car_rating(user_car)
    
    all_drivers = []
    driver_teams = {}
    base_ratings = {}
    
    for team_key in F1_TEAMS_2026:
        team = F1_TEAMS_2026[team_key]
        if team_key == user_team:
            car_params = user_car
        else:
            car_params = team['car_params']
        
        rating = get_car_rating(car_params)
        
        for driver in team['drivers']:
            all_drivers.append(driver)
            driver_teams[driver] = team_key
            base_ratings[driver] = rating
    
    race_positions = {}
    
    for driver in all_drivers:
        team_key = driver_teams[driver]
        base_rating = base_ratings[driver]
        
        qualifying = base_rating + random.randint(-15, 15)
        
        race_performance = qualifying
        
        events = random.sample(RACE_EVENTS, random.randint(1, 3))
        event_log = []
        
        for emoji, text, effect in events:
            race_performance += effect
            if effect != 0:
                event_log.append(f"{emoji} {text}")
        
        pit_stop = random.randint(-2, 2)
        race_performance += pit_stop
        
        if random.random() < 0.1:
            dnf = True
            race_performance = -100
        else:
            dnf = False
        
        race_positions[driver] = {
            'performance': race_performance,
            'qualifying': qualifying,
            'events': event_log,
            'dnf': dnf,
            'team': team_key
        }
    
    sorted_drivers = sorted(race_positions.items(), key=lambda x: x[1]['performance'], reverse=True)
    
    final_positions = {}
    position = 1
    for driver, data in sorted_drivers:
        if data['dnf']:
            final_positions[driver] = "DNF"
        else:
            final_positions[driver] = position
            position += 1
    
    return final_positions, race_positions

def get_team_display_name(team_key):
    team = F1_TEAMS_2026.get(team_key, {})
    emoji = team.get('emoji', '🏎️')
    return f"{emoji} {team_key.title()}"

def get_team_info_text(team_key):
    team = F1_TEAMS_2026.get(team_key)
    if not team:
        return "Команда не найдена"
    
    drivers = ", ".join(team['drivers'])
    car_rating = get_car_rating(team['car_params'])
    
    return f"""{team['emoji']} **{team_key.title()}**

📜 *История:*
{team['history']}

👥 *Пилоты:* {drivers}
🏆 *Чемпионства:* {team['championships']}
⚙️ *Двигатель:* {team['engine']}
💰 *Бюджет:* {team['budget_display']}
🎯 *Ожидания:* {team['expectations']}
📊 *Рейтинг болида:* {car_rating}/100

Готовы стать менеджером?"""

def init_user_data(user_id, team_key):
    team = F1_TEAMS_2026[team_key]
    team_budget = team['budget']
    
    user_data[user_id] = {
        'team': team_key,
        'balance': team_budget,
        'car_params': team['car_params'].copy(),
        'points': 0,
        'team_budget': team_budget,
        'budget_requests': 0,
        'last_budget_request': None,
        'races_completed': 0,
        'total_earnings': 0
    }
    mailbox[user_id] = []

def get_user_car_quality(user_id):
    if user_id not in user_data:
        return 0
    car_params = user_data[user_id]['car_params']
    values = car_params.values()
    summ = sum(values) / len(values)
    return round(summ)

def aerosettings(call):
    user_id = call.message.chat.id
    if user_id not in user_data:
        return
    
    current_aero = user_data[user_id]['car_params']['aerodynamics']
    cost_2percent = calculate_improvement_cost(current_aero, 2, 'aerodynamics')
    cost_3percent = calculate_improvement_cost(current_aero, 3, 'aerodynamics')
    
    markup = InlineKeyboardMarkup(row_width=2)
    frontwing_btn = InlineKeyboardButton(f'🪽 Переднее крыло (+2%) - {cost_2percent:,}$', callback_data='frontwing_btn')
    backwing_btn = InlineKeyboardButton(f'🪽 Заднее антикрыло (+2%) - {cost_2percent:,}$', callback_data='backwing_btn')
    effect_btn = InlineKeyboardButton(f'💯 Эффективность (+3%) - {cost_3percent:,}$', callback_data='effect_btn')
    brake_btn = InlineKeyboardButton(f'🍃 Воздуховоды (+2%) - {calculate_improvement_cost(user_data[user_id]["car_params"]["reliability"], 2, "reliability"):,}$', callback_data='brake_btn')
    back_btn = InlineKeyboardButton('🔙 Назад', callback_data='develop_back')
    markup.add(frontwing_btn, backwing_btn, effect_btn, brake_btn, back_btn)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"🌀 *Настройки аэродинамики*\n\n"
             f"*Текущий уровень:* {current_aero}/100\n\n"
             f"*Доступные улучшения:*\n"
             f"• 🪽 Переднее крыло: +2% аэродинамики ({cost_2percent:,}$)\n"
             f"• 🪽 Заднее антикрыло: +2% аэродинамики ({cost_2percent:,}$)\n"
             f"• 💯 Эффективность: +3% аэродинамики ({cost_3percent:,}$)\n"
             f"• 🍃 Тормозные воздуховоды: +2% надежности ({calculate_improvement_cost(user_data[user_id]['car_params']['reliability'], 2, 'reliability'):,}$)\n\n"
             f"*Примечание:* Стоимость улучшений растет с повышением уровня параметра.",
        reply_markup=markup,
        parse_mode='Markdown'
    )

def enginesettings(call):
    user_id = call.message.chat.id
    if user_id not in user_data:
        return
    
    current_engine = user_data[user_id]['car_params']['engine']
    cost_5percent = calculate_improvement_cost(current_engine, 5, 'engine')
    
    markup = InlineKeyboardMarkup(row_width=2)
    buyengine_btn = InlineKeyboardButton(f'⚙️ Улучшить двигатель (+5%) - {cost_5percent:,}$', callback_data='buyengine_btn')
    back_btn = InlineKeyboardButton('🔙 Назад', callback_data='develop_back')
    markup.add(buyengine_btn, back_btn)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"⚙️ *Настройки двигателя*\n\n"
             f"*Текущий уровень:* {current_engine}/100\n\n"
             f"*Доступные улучшения:*\n"
             f"• ⚙️ Улучшить двигатель: +5% мощности двигателя ({cost_5percent:,}$)\n\n"
             f"*Примечание:* Стоимость улучшений растет с повышением уровня параметра.",
        reply_markup=markup,
        parse_mode='Markdown'
    )

def chassissettings(call):
    user_id = call.message.chat.id
    if user_id not in user_data:
        return
    
    current_chassis = user_data[user_id]['car_params']['chassis']
    cost_5percent = calculate_improvement_cost(current_chassis, 5, 'chassis')
    
    markup = InlineKeyboardMarkup(row_width=2)
    buychassis_btn = InlineKeyboardButton(f'🔩 Улучшить шасси (+5%) - {cost_5percent:,}$', callback_data='buychassis_btn')
    back_btn = InlineKeyboardButton('🔙 Назад', callback_data='develop_back')
    markup.add(buychassis_btn, back_btn)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"🔩 *Настройки шасси*\n\n"
             f"*Текущий уровень:* {current_chassis}/100\n\n"
             f"*Доступные улучшения:*\n"
             f"• 🔩 Улучшить шасси: +5% качества шасси ({cost_5percent:,}$)\n\n"
             f"*Примечание:* Стоимость улучшений растет с повышением уровня параметра.",
        reply_markup=markup,
        parse_mode='Markdown'
    )

def improve(user_id, param, value):
    if user_id not in user_data:
        return False
    
    current_value = user_data[user_id]['car_params'][param]
    
    # Рассчитываем стоимость улучшения
    cost = calculate_improvement_cost(current_value, value, param)
    
    if user_data[user_id]['balance'] < cost:
        return "no_money"
    
    if current_value >= 100 and value > 0:
        return "max"
    
    new_value = current_value + value
    
    if new_value > 100:
        new_value = 100
    
    user_data[user_id]['car_params'][param] = new_value
    user_data[user_id]['balance'] -= cost
    user_data[user_id]['total_earnings'] -= cost
    
    # Соперники тоже улучшаются, но медленнее и дешевле
    for team_key in F1_TEAMS_2026:
        if team_key != user_data[user_id]['team']:
            opponent_params = F1_TEAMS_2026[team_key]['car_params']
            for param_key in opponent_params:
                if random.random() < 0.15:  # 15% шанс
                    improvement = random.randint(1, 2)
                    opponent_params[param_key] += improvement
                    if opponent_params[param_key] > 100:
                        opponent_params[param_key] = 100
    
    return True, cost

def show_mailbox(call):
    user_id = call.message.chat.id
    if user_id not in mailbox:
        mailbox[user_id] = []
    
    messages = mailbox[user_id]
    
    if not messages:
        text = "📭 *Почтовый ящик пуст*\n\nЗдесь будут появляться сообщения от пилотов, спонсоров и руководства команды"
    else:
        text = "📬 *Ваши сообщения:*\n\n"
        for i, msg in enumerate(messages[-10:], 1):
            text += f"{i}. {msg}\n"
    
    markup = InlineKeyboardMarkup(row_width=2)
    clear_btn = InlineKeyboardButton('🗑️ Очистить почту', callback_data='clear_mailbox')
    back_btn = InlineKeyboardButton('🔙 Назад', callback_data='back_to_game')
    markup.add(clear_btn, back_btn)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=markup,
        parse_mode='Markdown'
    )

def clear_mailbox(user_id):
    if user_id in mailbox:
        mailbox[user_id] = []
        return True
    return False

def add_message(user_id, message):
    if user_id not in mailbox:
        mailbox[user_id] = []
    mailbox[user_id].append(message)
    if len(mailbox[user_id]) > 50:
        mailbox[user_id] = mailbox[user_id][-50:]

def manage_team(call):
    user_id = call.message.chat.id
    if user_id not in user_data:
        return
    
    team_name = user_data[user_id]['team']
    team = F1_TEAMS_2026[team_name]
    
    markup = InlineKeyboardMarkup(row_width=2)
    
    drivers_btn = InlineKeyboardButton('👥 Управление пилотами', callback_data='manage_drivers')
    staff_btn = InlineKeyboardButton('👔 Персонал', callback_data='manage_staff')
    sponsors_btn = InlineKeyboardButton('💰 Спонсоры', callback_data='manage_sponsors')
    contracts_btn = InlineKeyboardButton('📝 Контракты', callback_data='manage_contracts')
    finances_btn = InlineKeyboardButton('💳 Финансы', callback_data='manage_finances')
    back_btn = InlineKeyboardButton('🔙 Назад', callback_data='back_to_game')
    
    markup.add(drivers_btn, staff_btn, sponsors_btn, contracts_btn, finances_btn, back_btn)
    
    drivers_text = ", ".join(team['drivers'])
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"💼 *Управление командой — {team_name.title()}*\n\n"
             f"👥 *Пилоты:* {drivers_text}\n"
             f"🏆 *Очки в чемпионате:* {user_data[user_id]['points']}\n"
             f"💰 *Бюджет команды:* {team['budget_display']}\n"
             f"💵 *Ваш баланс:* {user_data[user_id]['balance']:,}$\n".replace(",", ".") +
             f"📊 *Рейтинг болида:* {get_user_car_quality(user_id)}/100\n"
             f"🎯 *Ожидания руководства:* {team['expectations']}\n\n"
             f"Выберите раздел управления:",
        reply_markup=markup,
        parse_mode='Markdown'
    )

def manage_drivers(call):
    user_id = call.message.chat.id
    if user_id not in user_data:
        return
    
    team_name = user_data[user_id]['team']
    team = F1_TEAMS_2026[team_name]
    
    markup = InlineKeyboardMarkup(row_width=2)
    
    for driver in team['drivers']:
        driver_btn = InlineKeyboardButton(f'👤 {driver}', callback_data=f'driver_{driver}')
        markup.add(driver_btn)
    
    back_btn = InlineKeyboardButton('🔙 Назад к управлению', callback_data='manage_back')
    markup.add(back_btn)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"👥 *Управление пилотами — {team_name.title()}*\n\n"
             f"Выберите пилота для управления:\n\n"
             f"• {team['drivers'][0]} — основной пилот\n"
             f"• {team['drivers'][1]} — второй пилот\n\n"
             f"Здесь вы можете общаться с пилотами, менять контракты и мотивировать команду.",
        reply_markup=markup,
        parse_mode='Markdown'
    )

def manage_sponsors(call):
    user_id = call.message.chat.id
    if user_id not in user_data:
        return
    
    team_name = user_data[user_id]['team']
    
    sponsors = [
        ("🏎️ Petronas", "+500,000$", "petronas_sponsor"),
        ("🛢️ Shell", "+400,000$", "shell_sponsor"),
        ("🛞 Pirelli", "+300,000$", "pirelli_sponsor"),
        ("⚫ Monster", "+600,000$", "monster_sponsor"),
        ("📱 Huawei", "+450,000$", "huawei_sponsor")
    ]
    
    markup = InlineKeyboardMarkup(row_width=2)
    
    for name, amount, callback in sponsors:
        sponsor_btn = InlineKeyboardButton(f'{name} {amount}', callback_data=callback)
        markup.add(sponsor_btn)
    
    back_btn = InlineKeyboardButton('🔙 Назад к управлению', callback_data='manage_back')
    markup.add(back_btn)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"💰 *Поиск спонсоров — {team_name.title()}*\n\n"
             f"Выберите спонсора для переговоров:\n\n"
             f"• 🏎️ Petronas — +500,000$\n"
             f"• 🛢️ Shell — +400,000$\n"
             f"• 🛞 Pirelli — +300,000$\n"
             f"• ⚫ Monster — +600,000$\n"
             f"• 📱 Huawei — +450,000$\n\n"
             f"Успешные переговоры пополнят ваш бюджет",
        reply_markup=markup,
        parse_mode='Markdown'
    )

def manage_finances(call):
    user_id = call.message.chat.id
    if user_id not in user_data:
        return
    
    team_name = user_data[user_id]['team']
    team = F1_TEAMS_2026[team_name]
    
    markup = InlineKeyboardMarkup(row_width=2)
    
    request_budget_btn = InlineKeyboardButton('📈 Запросить бюджет', callback_data='request_budget')
    view_expenses_btn = InlineKeyboardButton('📊 Расходы', callback_data='view_expenses')
    back_btn = InlineKeyboardButton('🔙 Назад к управлению', callback_data='manage_back')
    
    markup.add(request_budget_btn, view_expenses_btn, back_btn)
    
    budget_requests = user_data[user_id].get('budget_requests', 0)
    requests_left = max(0, 3 - budget_requests)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"💳 *Финансы — {team_name.title()}*\n\n"
             f"💰 *Ваш баланс:* {user_data[user_id]['balance']:,}$\n".replace(",", ".") +
             f"🏆 *Очки в чемпионате:* {user_data[user_id]['points']}\n"
             f"📊 *Запросов бюджета осталось:* {requests_left}/3\n\n"
             f"📈 *Запросить бюджет можно до 3 раз за сезон*\n"
             f"💰 *Возможная сумма:* 2-10 миллионов $\n\n"
             f"Руководство может отказать в запросе, если команда показывает плохие результаты.",
        reply_markup=markup,
        parse_mode='Markdown'
    )