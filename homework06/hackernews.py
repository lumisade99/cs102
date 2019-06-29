from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news, extract_news, extract_next_page
from db import News, session
import time
from bayes import NaiveBayesClassifier
import string

@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)

@route("/add_label/")
def add_label():
    # 1. Получить значения параметров label и id из GET-запроса
    # 2. Получить запись из БД с соответствующим id (такая запись только одна!)
    # 3. Изменить значение метки записи на значение label
    # 4. Сохранить результат в БД 
    label = request.query.label
    id = int(request.query.id)
    s = session()
    art = s.query(News).filter(News.id == id).one()
    art.label = label
    s.add(art)                
    s.commit()
    redirect("/news")

@route('/update')
def update_news():
    # 1. Получить данные с новостного сайта
    # 2. Проверить, каких новостей еще нет в БД. Будем считать,
    #    что каждая новость может быть уникально идентифицирована
    #    по совокупности двух значений: заголовка и автора
    # 3. Сохранить в БД те новости, которых там нет
    s = session()
    news = get_news("https://news.ycombinator.com/newest", n_pages = 1)
    titles = s.query(News.title).all()
    authors = s.query(News.author).all()
    t = []
    for i in range(len(titles)):
        t.append(titles[i][0])
    au = []
    for i in range(len(authors)):
        au.append(authors[i][0])
    for i in range(len(news)):
        a = news[i].get('title')
        b = news[i].get('author')
        if a not in t and b not in au:
            s.add(News(author = news[i]['author'], title = news[i]['title'], url = news[i]['url'],  points = news[i]['points'], comments = news[i]['comments']))
    time.sleep(0.333333334)
    s.commit()
    redirect('/news')


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


@route("/classify")
def classify_news():
    s = session()
    rows_test = s.query(News).filter(News.label == None).all()
    rows_train = s.query(News).filter(News.label != None).all()
    X_train, Y_train, Y_test = [], [], []
    for el in rows_train:
        X_train.append(el.title)
        Y_train.append(el.label)
    y_train = [clean(y).lower() for y in Y_train]
    for el in rows_test:
        Y_test.append(el.title)
    y_test = [clean(c).lower() for c in Y_test]
    model = NaiveBayesClassifier()
    model.fit(X_train, y_train)
    metki = model.predict(y_test)
    sol = zip(rows_test, metki)
    return template('b_template', rows=sol)


if __name__ == "__main__":
    run(host="localhost", port=8080)
