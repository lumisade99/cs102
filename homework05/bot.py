import config
import telebot
from bs4 import BeautifulSoup
import requests

access_token = '512638430:AAEniUwuaCe7q8TAaociCAUsRfqkA7jyDJ8'
bot = telebot.TeleBot(config.access_token)

def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page

'''
def parse_schedule_for_a_monday(web_page):
    soup = BeautifulSoup(web_page, "html5lib")
    # Получаем таблицу с расписанием на понедельник
    schedule_table = soup.find("table", attrs={"id": "1day"})
    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]
    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]
    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]
    return times_list, locations_list, lessons_list


@bot.message_handler(commands=['monday'])
def get_monday(message):
    """ Получить расписание на понедельник """
    _, group = message.text.split()
    web_page = get_page(group)
    times_lst, locations_lst, lessons_lst = \
        parse_schedule_for_a_monday(web_page)
    resp = ''
    for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')

'''
def parse_schedule_for_a_necessary_day(web_page, day):
    soup = BeautifulSoup(web_page, "html5lib")
    # Получаем таблицу с расписанием на необходимый день
    if day == '/monday' or day == '/sunday':
        schedule_table = soup.find("table", attrs={"id": "1day"})
    elif day == '/tuesday':
        schedule_table = soup.find("table", attrs={"id": "2day"})
    elif day == '/wednesday':
        schedule_table = soup.find("table", attrs={"id": "3day"})
    elif day == '/thursday':
        schedule_table = soup.find("table", attrs={"id": "4day"})
    elif day == '/friday':
        schedule_table = soup.find("table", attrs={"id": "5day"})
    elif day == '/saturday':
        schedule_table = soup.find("table", attrs={"id": "6day"})
    if not schedule_table:
        return None
    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]
    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]
    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]
    return times_list, locations_list, lessons_list


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    """ Получить расписание на указанный день """
    day, week, group = message.text.split()
    web_page = get_page(week, group)
    schedule = \
        parse_schedule_for_a_necessary_day(web_page, day)
    if not schedule:
        bot.send_message(message.chat.id, 'Расписание не найдено')
        return
    times_lst, locations_lst, lessons_lst = schedule
    resp = ''
    for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    import datetime
    from datetime import time
    _, group = message.text.split()
    today = datetime.datetime.now().weekday() 
    if today == 6:
        bot.send_message(message.chat.id, 'Ты чего!? Сегодня воскресенье')
    else:
        if today == 0:
           today = '/monday'
        elif today == 1:
            today = '/tuesday'
        elif today == 2:
            today = '/wednesday'
        elif today == 3:
            today = '/thursday'
        elif today == 4:
            today = '/friday'
        elif today == 5:
            today = '/saturday'

    if int(datetime.datetime.today().strftime('%W')) % 2 == 1:
        week = 2
    else:
        week = 1
    web_page = get_page(week, group)
    schedule = parse_schedule_for_a_necessary_day(web_page, today)
    if not schedule:
        bot.send_message(message.chat.id, 'Нет занятий, отдыхай')
        return None
        bot.send_message(message.chat.id, sch, parse_mode='HTML')


@bot.message_handler(commands=['tomorrow'])
def get_tommorow(message):
    """ Получить расписание на следующий день """
    import datetime
    from datetime import time
    _, group = message.text.split()
    if int(datetime.datetime.today().strftime('%W')) % 2 == 1: 
        week = 2
    else:
        week = 1
    web_page = get_page(week, group)
    today = datetime.datetime.now()
    tomorrow = today
    if today.weekday() == 5:
        tomorrow += datetime.timedelta(days=2)
    else:
        tomorrow += datetime.timedelta(days=1)
    if tomorrow.weekday() == 0:
        tomorrow = '/monday'
    elif tomorrow.weekday() == 1:
        tomorrow = '/tuesday'
    elif tomorrow.weekday() == 2:
        tomorrow = '/wednesday'
    elif tomorrow.weekday() == 3:
        tomorrow = '/thursday'
    elif tomorrow.weekday() == 4:
        tomorrow = '/friday'
    elif tomorrow.weekday() == 5:
        tomorrow = '/saturday'
    schedule = parse_schedule_for_a_necessary_day(web_page, tomorrow)
    if not schedule:
        bot.send_message(message.chat.id, 'Не нашел расписание')
        return None
    times_lst, locations_lst, lessons_lst = schedule
    resp = 'Заврашние занятия:'
    for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    if len(message.text.split()) != 1:
        _, week, group = message.text.split()  
        web_page = get_page(week, group)
        if int(week) == 1:
            resp = '<b>Расписание на четную неделю:</b>\n\n'
        elif int(week) == 2:
            resp = '<b>Расписание на нечетную неделю:</b>\n\n'
        elif int(week) == 0:
            resp = '<b>Общее расписание:</b>\n\n'
    week_list = ['/monday', '/tuesday', '/wednesday', '/thursday', '/friday', '/saturday']
    visual_list = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
    for i in range(6):
        resp += '<b>' + visual_list[i] + '</b>' + ':\n'
        schedule = parse_schedule_for_a_necessary_day(web_page, week_list)
        if not schedule:
            bot.send_message(message.chat.id, 'Не нашел расписание')
            return None
    times_lst, locations_lst, lessons_lst = schedule
    for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)









