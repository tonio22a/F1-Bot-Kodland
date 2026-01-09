# config.py

F1_TEAMS_2026 = {
    'mercedes': {
        'emoji': '⚫',
        'history': 'Немецкая команда-чемпион, доминировала в гибридную эру.',
        'drivers': ['Джордж Рассел', 'Кими Антоннелли'],
        'engine': 'Mercedes',
        'lvl': 83,
        'championships': 8,
        'budget': 16500000,
        'budget_display': '16.5 миллионов $',
        'expectations': 'Вернуть чемпионский титул',
        'car_params': {
            'aerodynamics': 82,
            'engine': 88,
            'chassis': 85,
            'reliability': 80
        }
    },
    'red bull': {
        'emoji': '🟠',
        'history': 'Австрийская команда, доминирующая с 2022 года.',
        'drivers': ['Макс Ферстаппен', 'Исак Хаджар'],
        'engine': 'Red Bull Powertrains',
        'lvl': 88,
        'championships': 6,
        'budget': 15500000,
        'budget_display': '15.5 миллионов $',
        'expectations': 'Продолжить доминирование',
        'car_params': {
            'aerodynamics': 92,
            'engine': 90,
            'chassis': 87,
            'reliability': 85
        }
    },
    'ferrari': {
        'emoji': '🔴',
        'history': 'Самая старая и успешная команда в Ф1.',
        'drivers': ['Шарль Леклер', 'Льюис Хэмилтон'],
        'engine': 'Ferrari',
        'lvl': 82,
        'championships': 16,
        'budget': 17000000,
        'budget_display': '17 миллионов $',
        'expectations': 'Выиграть чемпионство',
        'car_params': {
            'aerodynamics': 85,
            'engine': 86,
            'chassis': 83,
            'reliability': 78
        }
    },
    'mclaren': {
        'emoji': '🟠',
        'history': 'Британская команда с богатой историей.',
        'drivers': ['Ландо Норрис', 'Оскар Пиастри'],
        'engine': 'Mercedes',
        'lvl': 89,
        'championships': 8,
        'budget': 15000000,
        'budget_display': '15 миллионов $',
        'expectations': 'Бороться за чемпионство',
        'car_params': {
            'aerodynamics': 84,
            'engine': 83,
            'chassis': 88,
            'reliability': 82
        }
    },
    'aston martin': {
        'emoji': '🔘',
        'history': 'Британская команда, бывшая Racing Point.',
        'drivers': ['Фернандо Алонсо', 'Лэнс Стролл'],
        'engine': 'Honda',
        'lvl': 81,
        'championships': 0,
        'budget': 14000000,
        'budget_display': '14 миллионов $',
        'expectations': 'Добиться первых побед',
        'car_params': {
            'aerodynamics': 79,
            'engine': 81,
            'chassis': 80,
            'reliability': 77
        }
    },
    'alpine': {
        'emoji': '🔵',
        'history': 'Французская команда, заводская команда Renault.',
        'drivers': ['Пьер Гасли', 'Франко Колапинто'],
        'engine': 'Mercedes',
        'lvl': 78,
        'championships': 2,
        'budget': 13000000,
        'budget_display': '13 миллионов $',
        'expectations': 'Регулярно бороться за подиумы',
        'car_params': {
            'aerodynamics': 77,
            'engine': 78,
            'chassis': 76,
            'reliability': 75
        }
    },
    'williams': {
        'emoji': '🔵',
        'history': 'Легендарная британская команда.',
        'drivers': ['Александр Албон', 'Карлос Сайнс'],
        'engine': 'Mercedes',
        'lvl': 78,
        'championships': 9,
        'budget': 12000000,
        'budget_display': '12 миллионов $',
        'expectations': 'Вернуться в середину пелотона',
        'car_params': {
            'aerodynamics': 75,
            'engine': 76,
            'chassis': 74,
            'reliability': 72
        }
    },
    'haas': {
        'emoji': '🔴',
        'history': 'Американская команда, дебютировала в 2016 году.',
        'drivers': ['Эстебан Окон', 'Питер Пор'],
        'engine': 'Ferrari',
        'lvl': 78,
        'championships': 0,
        'budget': 11000000,
        'budget_display': '11 миллионов $',
        'expectations': 'Набирать очки регулярно',
        'car_params': {
            'aerodynamics': 72,
            'engine': 74,
            'chassis': 71,
            'reliability': 70
        }
    },
    'rb academy': {
        'emoji': '🟣',
        'history': 'Команда Red Bull, ранее AlphaTauri.',
        'drivers': ['Арвид Линдблад', 'Лиам Лоусон'],
        'engine': 'Honda',
        'lvl': 76,
        'championships': 0,
        'budget': 10000000,
        'budget_display': '10 миллионов $',
        'expectations': 'Бороться за очки',
        'car_params': {
            'aerodynamics': 73,
            'engine': 72,
            'chassis': 74,
            'reliability': 71
        }
    },
    'audi': {
        'emoji': '⚪',
        'history': 'Немецкий автопроизводитель входит в Ф1 с 2026 года.',
        'drivers': ['Габриэль Бортолето', 'Нико Хюлькенберг'],
        'engine': 'Audi',
        'lvl': 81,
        'championships': 0,
        'budget': 16000000,
        'budget_display': '16 миллионов $',
        'expectations': 'Показать хороший результат',
        'car_params': {
            'aerodynamics': 78,
            'engine': 80,
            'chassis': 79,
            'reliability': 76
        }
    },
    'cadillac': {
        'emoji': '⚪',
        'history': 'Американский автоконцерн General Motors.',
        'drivers': ['Валттери Боттас', 'Серхио Перес'],
        'engine': 'General Motors',
        'lvl': 82,
        'championships': 0,
        'budget': 15000000,
        'budget_display': '15 миллионов $',
        'expectations': 'Заявить о себе',
        'car_params': {
            'aerodynamics': 80,
            'engine': 79,
            'chassis': 81,
            'reliability': 78
        }
    }
}

user_teams = {}
user_data = {}
mailbox = {}