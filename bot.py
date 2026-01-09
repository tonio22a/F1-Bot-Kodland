from bot_instance import bot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import *
from logic import *
import random

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup(row_width=2)
    play_btn = InlineKeyboardButton('🏎️ Начать карьеру', callback_data='start_career')
    channel_btn = InlineKeyboardButton('📢 Наш канал', url='https://t.me/projectauoff')
    markup.add(play_btn, channel_btn)
    
    bot.send_message(
        message.chat.id,
        "🏁 *Добро пожаловать в мир формулы 1!*\n\nВы — менеджер команды формулы 1 в сезоне 2026 года.",
        reply_markup=markup,
        parse_mode='Markdown'
    )

@bot.message_handler(commands=['mailbox'])
def mailbox_command(message):
    user_id = message.chat.id
    if user_id not in mailbox:
        mailbox[user_id] = []
    
    messages = mailbox[user_id]
    
    if not messages:
        text = "📭 *Почтовый ящик пуст*"
    else:
        text = "📬 *Ваши сообщения:*\n\n"
        for i, msg in enumerate(messages[-10:], 1):
            text += f"{i}. {msg}\n"
    
    bot.send_message(user_id, text, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    try:
        if call.data == 'start_career':
            bot.answer_callback_query(call.id, "Выбор команды...")
            show_all_teams(call)
        
        elif call.data in F1_TEAMS_2026.keys():
            team_name = call.data
            bot.answer_callback_query(call.id, f"Вы выбрали {team_name}")
            show_team_details(call, team_name)
        
        elif call.data == 'accept_team':
            team_name = user_teams.get(call.message.chat.id)
            if team_name:
                init_user_data(call.message.chat.id, team_name)
                bot.answer_callback_query(call.id, f"Добро пожаловать в {team_name}!")
                start_game(call, team_name)
                add_message(call.message.chat.id, "🏁 Добро пожаловать в команду! Начинаем сезон 2026.")
                add_message(call.message.chat.id, f"💰 На ваш счет зачислено {F1_TEAMS_2026[team_name]['budget_display']} для развития болида.")
            else:
                bot.answer_callback_query(call.id, "❌ Сначала выберите команду!")
        
        elif call.data == 'back_to_teams':
            bot.answer_callback_query(call.id, "Выбор команды")
            show_all_teams(call)
        
        elif call.data == 'race_btn':
            bot.answer_callback_query(call.id, "Подготовка к гонке...")
            race_menu(call)
        
        elif call.data == 'develop_btn':
            bot.answer_callback_query(call.id, "Центр разработки")
            develop_menu(call)
        
        elif call.data == 'manage_btn':
            bot.answer_callback_query(call.id, "Управление командой")
            manage_team(call)
        
        elif call.data == 'mailbox_btn':
            bot.answer_callback_query(call.id, "Почтовый ящик")
            show_mailbox(call)
        
        elif call.data == 'back_to_game':
            user_id = call.message.chat.id
            if user_id in user_data:
                team_name = user_data[user_id]['team']
            else:
                team_name = 'Ваша команда'
            show_game_menu(call, team_name)
        
        elif call.data == 'manage_back':
            bot.answer_callback_query(call.id, "Назад к управлению")
            manage_team(call)

        elif call.data == 'aero_btn':
            bot.answer_callback_query(call.id, "Настройки аэродинамики")
            aerosettings(call)

        elif call.data == 'engine_btn':
            bot.answer_callback_query(call.id, "Настройки двигателя")
            enginesettings(call)

        elif call.data == 'chassis_btn':
            bot.answer_callback_query(call.id, "Настройки шасси")
            chassissettings(call)
        
        elif call.data == 'develop_back':
            bot.answer_callback_query(call.id, "Назад к разработке")
            develop_menu(call)

        elif call.data == 'frontwing_btn':
            result = improve(call.message.chat.id, 'aerodynamics', 2)
            if isinstance(result, tuple):
                success, cost = result
                handle_improvement_result(call, success, cost, "Переднее антикрыло улучшено на 2%")
            else:
                handle_improvement_result(call, result, 0, "")
        
        elif call.data == 'backwing_btn':
            result = improve(call.message.chat.id, 'aerodynamics', 2)
            if isinstance(result, tuple):
                success, cost = result
                handle_improvement_result(call, success, cost, "Заднее антикрыло улучшено на 2%")
            else:
                handle_improvement_result(call, result, 0, "")
        
        elif call.data == 'effect_btn':
            result = improve(call.message.chat.id, 'aerodynamics', 3)
            if isinstance(result, tuple):
                success, cost = result
                handle_improvement_result(call, success, cost, "Аэродинамическая эффективность улучшена на 3%")
            else:
                handle_improvement_result(call, result, 0, "")
        
        elif call.data == 'brake_btn':
            result = improve(call.message.chat.id, 'reliability', 2)
            if isinstance(result, tuple):
                success, cost = result
                handle_improvement_result(call, success, cost, "Тормозные воздуховоды улучшены на 2%")
            else:
                handle_improvement_result(call, result, 0, "")
        
        elif call.data == 'buyengine_btn':
            result = improve(call.message.chat.id, 'engine', 5)
            if isinstance(result, tuple):
                success, cost = result
                handle_improvement_result(call, success, cost, "Двигатель улучшен на 5%")
            else:
                handle_improvement_result(call, result, 0, "")
        
        elif call.data == 'buychassis_btn':
            result = improve(call.message.chat.id, 'chassis', 5)
            if isinstance(result, tuple):
                success, cost = result
                handle_improvement_result(call, success, cost, "Шасси улучшено на 5%")
            else:
                handle_improvement_result(call, result, 0, "")
        
        elif call.data == 'simulate_race':
            bot.answer_callback_query(call.id, "Симуляция гонки...")
            race_menu(call)
        
        elif call.data == 'manage_drivers':
            bot.answer_callback_query(call.id, "Управление пилотами")
            manage_drivers(call)
        
        elif call.data == 'manage_sponsors':
            bot.answer_callback_query(call.id, "Поиск спонсоров")
            manage_sponsors(call)
        
        elif call.data == 'manage_finances':
            bot.answer_callback_query(call.id, "Финансы команды")
            manage_finances(call)
        
        elif call.data == 'clear_mailbox':
            user_id = call.message.chat.id
            if clear_mailbox(user_id):
                bot.answer_callback_query(call.id, "✅ Почта очищена")
                add_message(user_id, "🗑️ Почтовый ящик очищен")
                show_mailbox(call)
            else:
                bot.answer_callback_query(call.id, "❌ Ошибка очистки")
        
        elif call.data == 'request_budget':
            user_id = call.message.chat.id
            if user_id in user_data:
                budget_requests = user_data[user_id].get('budget_requests', 0)
                
                if budget_requests >= 3:
                    bot.answer_callback_query(call.id, "❌ Лимит запросов исчерпан (3/3)")
                    add_message(user_id, "❌ Руководство отказало: лимит запросов бюджета исчерпан")
                    manage_finances(call)
                    return
                
                user_data[user_id]['budget_requests'] = budget_requests + 1
                
                points = user_data[user_id]['points']
                success_chance = 0.4 + min(points / 100, 0.3)  # От 40% до 70%
                
                if random.random() < success_chance:
                    if points > 50:
                        amount = random.randint(800000, 1500000)  # 800к-1.5 млн для успешных команд
                    else:
                        amount = random.randint(300000, 800000)   # 300к-800к для остальных
                    
                    user_data[user_id]['balance'] += amount
                    if 'total_earnings' in user_data[user_id]:
                        user_data[user_id]['total_earnings'] += amount
                    bot.answer_callback_query(call.id, f"✅ Получено +{amount:,}$")
                    add_message(user_id, f"💰 Руководство выделило дополнительные {amount:,}$")
                else:
                    bot.answer_callback_query(call.id, "❌ Руководство отказало в запросе")
                    add_message(user_id, f"❌ Руководство отказало в запросе бюджета. Очков команды: {points}")
                
                manage_finances(call)
        
        elif call.data.startswith('driver_'):
            driver_name = call.data.replace('driver_', '')
            bot.answer_callback_query(call.id, f"Общение с {driver_name}")
            
            messages = [
                f"{driver_name} доволен машиной",
                f"{driver_name} просит улучшить баланс болида",
                f"{driver_name} готов к следующей гонке",
                f"{driver_name} хочет обсудить контракт"
            ]
            
            markup = InlineKeyboardMarkup()
            back_btn = InlineKeyboardButton('🔙 Назад к пилотам', callback_data='manage_drivers')
            markup.add(back_btn)
            
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"👤 *Общение с {driver_name}*\n\n{random.choice(messages)}\n\nВы можете обсудить:\n• Мотивацию\n• Контракт\n• Технические пожелания",
                reply_markup=markup,
                parse_mode='Markdown'
            )
        
        elif call.data in ['petronas_sponsor', 'shell_sponsor', 'pirelli_sponsor', 'monster_sponsor', 'huawei_sponsor']:
            user_id = call.message.chat.id
            if user_id in user_data:
                sponsor_amounts = {
                    'petronas_sponsor': 500000,    
                    'shell_sponsor': 400000,
                    'pirelli_sponsor': 300000,
                    'monster_sponsor': 600000, 
                    'huawei_sponsor': 450000 
                }
                
                sponsor_names = {
                    'petronas_sponsor': 'Petronas',
                    'shell_sponsor': 'Shell',
                    'pirelli_sponsor': 'Pirelli',
                    'monster_sponsor': 'Monster',
                    'huawei_sponsor': 'Huawei'
                }
                
                amount = sponsor_amounts.get(call.data, 100000)
                sponsor_name = sponsor_names.get(call.data, 'Спонсор')
                
                # Шанс успеха зависит от рейтинга команды
                car_rating = get_user_car_quality(user_id)
                success_chance = 0.3 + (car_rating / 200)  # От 30% до 80%
                
                success = random.random() < success_chance
                
                if success:
                    user_data[user_id]['balance'] += amount
                    if 'total_earnings' in user_data[user_id]:
                        user_data[user_id]['total_earnings'] += amount
                    bot.answer_callback_query(call.id, f"✅ Успех! +{amount:,}$")
                    add_message(user_id, f"💰 Подписан спонсорский контракт с {sponsor_name} на {amount:,}$")
                else:
                    bot.answer_callback_query(call.id, f"❌ {sponsor_name} отказался")
                    add_message(user_id, f"❌ Спонсор {sponsor_name} отказался от сотрудничества")
                
                manage_sponsors(call)
        
        elif call.data in ['manage_staff', 'manage_contracts', 'view_expenses']:
            bot.answer_callback_query(call.id, "Раздел в разработке")
            
            markup = InlineKeyboardMarkup()
            back_btn = InlineKeyboardButton('🔙 Назад к управлению', callback_data='manage_back')
            markup.add(back_btn)
            
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="🔧 *Раздел в разработке*\n\nЭта функция будет доступна в следующем обновлении!",
                reply_markup=markup,
                parse_mode='Markdown'
            )
    
    except Exception as e:
        print(f"Error in callback: {e}")

def handle_improvement_result(call, result, cost, success_message):
    user_id = call.message.chat.id
    if result == "no_money":
        bot.answer_callback_query(call.id, f"❌ Недостаточно средств! Нужно {cost:,}$")
    elif result == "max":
        bot.answer_callback_query(call.id, "⚠️ Параметр уже на максимуме!")
    elif result == True:
        bot.answer_callback_query(call.id, f"✅ Улучшение за {cost:,}$ применено!")
        add_message(user_id, f"🔧 {success_message} ({cost:,}$)")
        develop_menu(call)
    else:
        bot.answer_callback_query(call.id, "❌ Ошибка улучшения")

def show_all_teams(call):
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = []
    teams_list = list(F1_TEAMS_2026.keys())
    
    for i in range(0, len(teams_list), 2):
        row = []
        if i < len(teams_list):
            team1 = teams_list[i]
            display_name1 = get_team_display_name(team1)
            row.append(InlineKeyboardButton(display_name1, callback_data=team1))
        
        if i + 1 < len(teams_list):
            team2 = teams_list[i + 1]
            display_name2 = get_team_display_name(team2)
            row.append(InlineKeyboardButton(display_name2, callback_data=team2))
        
        buttons.append(row)
    
    for row in buttons:
        markup.add(*row)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="🏎️ *Выберите команду, которой будете управлять:*",
        reply_markup=markup,
        parse_mode='Markdown'
    )

def show_team_details(call, team_key):
    user_teams[call.message.chat.id] = team_key
    
    markup = InlineKeyboardMarkup(row_width=2)
    accept_btn = InlineKeyboardButton('✅ Принять должность', callback_data='accept_team')
    back_btn = InlineKeyboardButton('🔙 Выбрать другую', callback_data='back_to_teams')
    markup.add(accept_btn, back_btn)
    
    team_text = get_team_info_text(team_key)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=team_text,
        reply_markup=markup,
        parse_mode='Markdown'
    )

def start_game(call, team_name):
    team_emoji = F1_TEAMS_2026[team_name]['emoji']
    
    markup = InlineKeyboardMarkup(row_width=2)
    race_btn = InlineKeyboardButton('🏁 Гонка', callback_data='race_btn')
    develop_btn = InlineKeyboardButton('🔧 Разработка', callback_data='develop_btn')
    manage_btn = InlineKeyboardButton('💼 Управление', callback_data='manage_btn')
    mailbox_btn = InlineKeyboardButton('📬 Почта', callback_data='mailbox_btn')
    markup.add(race_btn, develop_btn, manage_btn, mailbox_btn)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"{team_emoji} *Добро пожаловать в {team_name.title()}!*\n\nДобро пожаловать в сезон 2026! Начинайте свой путь в Ф1!",
        reply_markup=markup,
        parse_mode='Markdown'
    )

def show_game_menu(call, team_name):
    team_emoji = F1_TEAMS_2026.get(team_name, {}).get('emoji', '🏎️')
    
    markup = InlineKeyboardMarkup(row_width=2)
    race_btn = InlineKeyboardButton('🏁 Гонка', callback_data='race_btn')
    develop_btn = InlineKeyboardButton('🔧 Разработка', callback_data='develop_btn')
    manage_btn = InlineKeyboardButton('💼 Управление', callback_data='manage_btn')
    mailbox_btn = InlineKeyboardButton('📬 Почта', callback_data='mailbox_btn')
    markup.add(race_btn, develop_btn, manage_btn, mailbox_btn)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"{team_emoji} *Главное меню — {team_name.title()}*",
        reply_markup=markup,
        parse_mode='Markdown'
    )

def race_menu(call):
    user_id = call.message.chat.id
    if user_id not in user_data:
        bot.answer_callback_query(call.id, "❌ Сначала начните карьеру")
        return
    
    track = random.choice(TRACKS)
    results, race_data = simulate_race(user_id)
    
    if not results:
        bot.answer_callback_query(call.id, "❌ Ошибка")
        return
    
    user_team = user_data[user_id]['team']
    user_drivers = F1_TEAMS_2026[user_team]['drivers']
    
    team_display_names = {}
    for team_key in F1_TEAMS_2026:
        team_display_names[team_key] = get_team_display_name(team_key)
    
    result_text = "🏁 *Результаты гонки:*\n\n"
    
    position_counter = 1
    for driver, position in results.items():
        team_key = race_data[driver]['team']
        team_display = team_display_names.get(team_key, team_key)
        
        if driver in user_drivers:
            if position == "DNF":
                result_text += f"💥 *DNF: {driver}* ({team_display}) - Авария\n"
            else:
                result_text += f"▶️ *P{position}: {driver}* ({team_display}) - ваш пилот\n"
        else:
            if position == "DNF":
                result_text += f"💥 DNF: {driver} ({team_display})\n"
            else:
                result_text += f"P{position}: {driver} ({team_display})\n"
    
    user_car_rating = get_user_car_quality(user_id)
    
    pointsstart = 0
    points = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}
    
    prize_money = {
        1: 1800000,
        2: 1500000,
        3: 1200000,   
        4: 1000000,
        5: 980000, 
        6: 950000,   
        7: 900000,    
        8: 880000,    
        9: 800000,    
        10: 600000    
    }
    
    money_earned = 0
    user_positions = []
    
    for driver, position in results.items():
        if driver in user_drivers and position != "DNF":
            if position <= 10:
                pointsstart += points.get(position, 0)
                money_earned += prize_money.get(position, 0)
                user_positions.append(position)
    
    # бонус за участие
    if money_earned == 0 and user_positions:
        money_earned = 250000
    
    user_data[user_id]['points'] += pointsstart
    user_data[user_id]['balance'] += money_earned
    if 'total_earnings' in user_data[user_id]:
        user_data[user_id]['total_earnings'] += money_earned
    user_data[user_id]['races_completed'] = user_data[user_id].get('races_completed', 0) + 1
    
    event_log = ""
    for driver in user_drivers:
        if driver in race_data:
            events = race_data[driver]['events']
            if events:
                event_log += f"\n*{driver}:*\n"
                for event in events[:2]:
                    event_log += f"• {event}\n"
    
    markup = InlineKeyboardMarkup(row_width=2)
    back_btn = InlineKeyboardButton('🔙 Назад', callback_data='back_to_game')
    race_again_btn = InlineKeyboardButton('🔄 Еще гонку', callback_data='simulate_race')
    markup.add(race_again_btn, back_btn)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"{result_text}\n"
             f"🌍 *Трасса:* {track['name']}\n"
             f"🏟️ *Тип:* {track['circuit']}\n"
             f"📏 *Длина круга:* {track['length']} км\n"
             f"🔁 *Кругов:* {track['laps']}\n\n"
             f"📊 *Рейтинг вашего болида:* {user_car_rating}/100\n"
             f"🏅 *Заработано очков:* +{pointsstart}\n"
             f"💰 *Призовые за гонку:* +{money_earned:,}$\n".replace(",", ".") +
             f"💵 *Текущий баланс:* {user_data[user_id]['balance']:,}$\n".replace(",", ".") +
             f"📈 *Всего очков:* {user_data[user_id]['points']}\n"
             f"🏎️ *Гонок завершено:* {user_data[user_id]['races_completed']}\n"
             f"{event_log if event_log else ''}",
        reply_markup=markup,
        parse_mode='Markdown'
    )

def develop_menu(call):
    user_id = call.message.chat.id
    if user_id not in user_data:
        bot.answer_callback_query(call.id, "❌ Сначала начните карьеру!")
        return
    
    car_params = user_data[user_id]['car_params']
    balance = user_data[user_id]['balance']
    car_rating = get_user_car_quality(user_id)
    
    team_name = user_data[user_id]['team']
    team = F1_TEAMS_2026[team_name]
    initial_rating = get_car_rating(team['car_params'])
    
    try:
        aero_cost_2p = calculate_improvement_cost(car_params['aerodynamics'], 2, 'aerodynamics')
        aero_cost_3p = calculate_improvement_cost(car_params['aerodynamics'], 3, 'aerodynamics')
        engine_cost = calculate_improvement_cost(car_params['engine'], 5, 'engine')
        chassis_cost = calculate_improvement_cost(car_params['chassis'], 5, 'chassis')
        reliability_cost = calculate_improvement_cost(car_params['reliability'], 2, 'reliability')
    except:
        aero_cost_2p = 2000000
        aero_cost_3p = 3000000
        engine_cost = 5000000
        chassis_cost = 5000000
        reliability_cost = 2000000
    
    markup = InlineKeyboardMarkup(row_width=2)
    aero_btn = InlineKeyboardButton('🌀 Аэродинамика', callback_data='aero_btn')
    engine_btn = InlineKeyboardButton('⚙️ Двигатель', callback_data='engine_btn')
    chassis_btn = InlineKeyboardButton('🔩 Шасси', callback_data='chassis_btn')
    back_btn = InlineKeyboardButton('🔙 Назад', callback_data='back_to_game')
    markup.add(aero_btn, engine_btn, chassis_btn, back_btn)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"🔧 *Центр разработки — {team_name.title()}*\n\n"
             f"💰 *Баланс:* {balance:,}$\n".replace(",", ".") +
             f"📊 *Рейтинг болида:* {car_rating}/100\n"
             f"📈 *Начальный рейтинг команды:* {initial_rating}/100\n\n"
             f"*Текущие характеристики:*\n"
             f"🌀 Аэродинамика: {car_params['aerodynamics']}/100 (стоимость +2%: ~{aero_cost_2p:,}$)\n"
             f"⚙️ Двигатель: {car_params['engine']}/100 (стоимость +5%: ~{engine_cost:,}$)\n"
             f"🔩 Шасси: {car_params['chassis']}/100 (стоимость +5%: ~{chassis_cost:,}$)\n"
             f"🔋 Надежность: {car_params['reliability']}/100 (стоимость +2%: ~{reliability_cost:,}$)\n\n"
             f"*Выберите область для улучшения:*\n"
             f"• 🌀 Аэродинамика: улучшения +2-3% (1-3M$)\n"
             f"• ⚙️ Двигатель: улучшение +5% (2-5M$)\n"
             f"• 🔩 Шасси: улучшение +5% (1.5-4M$)\n\n"
             f"*Примечание:* Стоимость улучшений растет с повышением уровня параметра.",
        reply_markup=markup,
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    bot.reply_to(message, "Используйте /start для начала или кнопки меню")

if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)