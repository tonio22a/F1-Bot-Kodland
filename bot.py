from bot_instance import bot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import F1_TEAMS_2026, user_teams, game_started
from logic import *

# обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup(row_width=2)
    
    # создаем кнопки
    play_btn = InlineKeyboardButton('🏎️ Начать карьеру', callback_data='start_career')
    channel_btn = InlineKeyboardButton('📢 наш канал', url='https://t.me/projectauoff')
    
    # добавляем кнопки в меню
    markup.add(play_btn, channel_btn)
    
    # отправляем приветственное сообщение
    bot.send_message(
        message.chat.id,
        "🏁 *Добро пожаловать в мир формулы 1!*\n\n"
        "Вы — менеджер команды формулы 1 в сезоне 2026 года. "
        "Ваша задача — привести свою команду к победе в чемпионате мира!\n\n"
        "Примите стратегические решения, управляйте разработкой болида, "
        "Общайтесь с пилотами и докажите, что вы — лучший командир в paddock!",
        reply_markup=markup,
        parse_mode='Markdown'
    )

# обработчик всех нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    # если нажали "начать карьеру"
    if call.data == 'start_career':
        bot.answer_callback_query(call.id, "Выбор команды...")
        show_all_teams(call)
    
    # если нажали на команду (все команды обрабатываем одинаково)
    elif call.data in F1_TEAMS_2026.keys():
        team_name = call.data
        bot.answer_callback_query(call.id, f"Вы выбрали {team_name}")
        user_teams[call.message.chat.id] = team_name
        show_team_details(call, team_name)
    
    # если нажали "принять должность"
    elif call.data == 'accept_team':
        team_name = user_teams.get(call.message.chat.id, 'Неизвестная команда')
        bot.answer_callback_query(call.id, f"Добро пожаловать в {team_name}!")
        start_game(call, team_name)
    
    # если нажали "назад к выбору"
    elif call.data == 'back_to_teams':
        bot.answer_callback_query(call.id, "Выбор команды")
        show_all_teams(call)
    
    # если нажали кнопки в игре
    elif call.data == 'race_btn':
        bot.answer_callback_query(call.id, "Подготовка к гонке...")
        race_menu(call)
    
    elif call.data == 'develop_btn':
        bot.answer_callback_query(call.id, "Центр разработки")
        develop_menu(call)
    
    elif call.data == 'manage_btn':
        bot.answer_callback_query(call.id, "Управление командой")
        manage_menu(call)
    
    elif call.data == 'back_to_game':
        team_name = user_teams.get(call.message.chat.id, 'Ваша команда')
        show_game_menu(call, team_name)

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

def show_all_teams(call):
    """показать все команды для выбора"""
    markup = InlineKeyboardMarkup(row_width=2)
    
    # создаем кнопки для всех команд
    buttons = []
    teams_list = list(F1_TEAMS_2026.keys())
    
    # добавляем кнопки по две в ряд
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
    
    # добавляем все строки в разметку
    for row in buttons:
        markup.add(*row)
    
    # меняем сообщение
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="🏎️ *Выберите команду, которой будете управлять:*\n\n"
             "Каждая команда имеет свою историю, бюджет и ожидания. "
             "Выбирайте мудро — от этого зависит ваша карьера!",
        reply_markup=markup,
        parse_mode='Markdown'
    )

def show_team_details(call, team_key):
    """показать детальную информацию о команде"""
    markup = InlineKeyboardMarkup(row_width=2)
    
    # кнопки выбора
    accept_btn = InlineKeyboardButton('✅ Принять должность', callback_data='accept_team')
    back_btn = InlineKeyboardButton('🔙 Выбрать другую', callback_data='back_to_teams')
    
    markup.add(accept_btn, back_btn)
    
    # получаем текст о команде
    team_text = get_team_info_text(team_key)
    
    # меняем сообщение
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=team_text,
        reply_markup=markup,
        parse_mode='Markdown'
    )

def start_game(call, team_name):
    """начать игру с выбранной командой"""
    global game_started
    game_started = 1
    
    # создаем меню игры
    markup = InlineKeyboardMarkup(row_width=2)
    
    race_btn = InlineKeyboardButton('🏁 Гонка', callback_data='race_btn')
    develop_btn = InlineKeyboardButton('🔧 Разработка', callback_data='develop_btn')
    manage_btn = InlineKeyboardButton('💼 Управление', callback_data='manage_btn')
    calendar_btn = InlineKeyboardButton('📅 Календарь', callback_data='calendar_btn')
    
    markup.add(race_btn, develop_btn, manage_btn, calendar_btn)
    
    # приветствие менеджера
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"👋 *добро пожаловать в {team_name.title()}!*\n\n"
             f"Вы официально назначены менеджером команды. сезон 2026 начинается!\n\n"
             f"Ваши задачи:\n"
             f"• Приводить команду к победам\n"
             f"• Управлять разработкой болида\n"
             f"• Общаться с пилотами и спонсорами\n"
             f"• Принимать тактические решения\n\n"
             f"Удачи, босс! время показать, на что вы способны!",
        reply_markup=markup,
        parse_mode='Markdown'
    )

def show_game_menu(call, team_name):
    """показать главное меню игры"""
    markup = InlineKeyboardMarkup(row_width=2)
    
    race_btn = InlineKeyboardButton('🏁 Гонка', callback_data='race_btn')
    develop_btn = InlineKeyboardButton('🔧 Разработка', callback_data='develop_btn')
    manage_btn = InlineKeyboardButton('💼 Управление', callback_data='manage_btn')
    calendar_btn = InlineKeyboardButton('📅 Календарь', callback_data='calendar_btn')
    
    markup.add(race_btn, develop_btn, manage_btn, calendar_btn)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"🏎️ *Главное меню — {team_name.title()}*\n\n"
             f"Выберите действие:",
        reply_markup=markup,
        parse_mode='Markdown'
    )

def race_menu(call):
    """меню гонки"""
    markup = InlineKeyboardMarkup(row_width=2)
    
    strategy_btn = InlineKeyboardButton('📊 Стратегия', callback_data='strategy_btn')
    pitstop_btn = InlineKeyboardButton('⏱️ Пит-стоп', callback_data='pitstop_btn')
    overtake_btn = InlineKeyboardButton('💨 Обгон', callback_data='overtake_btn')
    back_btn = InlineKeyboardButton('🔙 Назад', callback_data='back_to_game')
    
    markup.add(strategy_btn, pitstop_btn, overtake_btn, back_btn)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="🏁 *Подготовка к гонке*\n\n"
             "Предстоящая гонка: Бахрейн\n"
             "Трасса: Сахир\n"
             "Длина круга: 5.412 км\n"
             "Количество кругов: 57\n\n"
             "Выберите действие:",
        reply_markup=markup,
        parse_mode='Markdown'
    )

def develop_menu(call):
    """меню разработки"""
    markup = InlineKeyboardMarkup(row_width=2)
    
    aero_btn = InlineKeyboardButton('🌀 Аэродинамика', callback_data='aero_btn')
    engine_btn = InlineKeyboardButton('⚙️ Двигатель', callback_data='engine_btn')
    chassis_btn = InlineKeyboardButton('🔩 Шасси', callback_data='chassis_btn')
    back_btn = InlineKeyboardButton('🔙 Назад', callback_data='back_to_game')
    
    markup.add(aero_btn, engine_btn, chassis_btn, back_btn)
    

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"🔧 *Центр разработки*\n\n"
             f"💰 Доступный бюджет: 25 млн $\n"
             f"⛓️‍💥 {textcarqual}\n"
             f"⚙️ Характеристики: Аэродинамика - {parameparameters['aerodynamics']}%, Мотор - {parameparameters['engine']}%, Шасси - {parameparameters['chassis']}%, Надёжность - {parameparameters['reliability']}%\n"
             f"Выберите область для улучшения:",
        reply_markup=markup,
        parse_mode='Markdown'

    )

def manage_menu(call):
    """меню управления командой"""
    markup = InlineKeyboardMarkup(row_width=2)
    
    drivers_btn = InlineKeyboardButton('👥 Пилоты', callback_data='drivers_btn')
    staff_btn = InlineKeyboardButton('👔 Персонал', callback_data='staff_btn')
    sponsors_btn = InlineKeyboardButton('💰 Спонсоры', callback_data='sponsors_btn')
    back_btn = InlineKeyboardButton('🔙 Назад', callback_data='back_to_game')
    
    markup.add(drivers_btn, staff_btn, sponsors_btn, back_btn)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="💼 *Управление командой*\n\n"
             "Здесь вы можете управлять всеми аспектами команды:\n"
             "• Общаться с пилотами\n"
             "• Нанимать персонал\n"
             "• Искать спонсоров\n\n"
             "Выберите раздел:",
        reply_markup=markup,
        parse_mode='Markdown'
    )

# обработка текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    """обработка обычных сообщений"""
    bot.reply_to(
        message, 
        "Используйте кнопки меню для навигации или /start для перезапуска бота"
    )

# запуск бота
if __name__ == "__main__":
    print("Бот запущен")
    print("Напишите /start в телеграме, чтобы начать")
    bot.polling(none_stop=True)