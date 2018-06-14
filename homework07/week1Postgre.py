import psycopg2
import psycopg2.extras
from pprint import pprint as pp
from tabulate import tabulate


conn = psycopg2.connect("host=localhost port=5432 dbname=odscourse user=postgres password=secret")
cursor = conn.cursor()

query = """
CREATE TABLE IF NOT EXISTS train (
    id INTEGER PRIMARY KEY,
    age INTEGER,
    gender INTEGER,
    height REAL,
    weight REAL,
    ap_hi INTEGER,
    ap_lo INTEGER,
    cholesterol INTEGER,
    gluc INTEGER,
    smoke BOOLEAN,
    alco BOOLEAN,
    active BOOLEAN,
    cardio BOOLEAN
)
"""
cursor.execute(query)
conn.commit()

with open('mlbootcamp5_train.csv', 'r') as f:
    reader = csv.reader(f)
    # Skip the header row
    next(reader)
    for Id, row in enumerate(reader):
        cursor.execute(
            "INSERT INTO train VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            [Id] + row
        )
conn.commit()

def fetch_all(cursor):
    colnames = [desc[0] for desc in cursor.description]
    records = cursor.fetchall()
    return [{colname:value for colname, value in zip(colnames, record)} for record in records]

"""
Посмотрим на первые пять записей
cursor.execute("SELECT * FROM train LIMIT 5")
records = cursor.fetchall()
print(records) 
"""

"""Вопрос 1. Сколько мужчин и женщин представлено в этом наборе данных?"""
cursor.execute( """
SELECT gender, AVG(height), COUNT(gender) 
FROM train 
GROUP BY gender
""")
print(tabulate(fetch_all(cursor), "keys", "psql"))


"""Вопрос 2. Кто в среднем реже указывает, что употребляет алкоголь – мужчины или женщины??"""
cursor.execute( """
SELECT COUNT(alco)
FROM train 
WHERE gender = '1' and alco = '1'

SELECT COUNT(alco)
FROM train 
WHERE gender = '2' and alco = '1'
""")
print(tabulate(fetch_all(cursor), "keys", "psql"))


"""Вопрос 3.Во сколько раз процент курящих среди мужчин больше, чем процент курящих среди женщин?"""
cursor.execute( """
SELECT(((SELECT COUNT(smoke) FROM train WHERE gender = '2' and smoke = '1')/(SELECT COUNT(gender) FROM train WHERE gender = '2'))/
((SELECT COUNT(smoke) FROM train WHERE gender = '1' and smoke = '1')/(SELECT COUNT(gender) FROM train WHERE gender = '1'))) 
FROM train
""")
print(tabulate(fetch_all(cursor), "keys", "psql"))


"""Функция, находящее медианное знаечение(aggregate median)"""
function = """
CREATE FUNCTION _final_median(anyarray) RETURNS float8 AS $$ 
  WITH q AS
  (
     SELECT val
     FROM unnest($1) val
     WHERE VAL IS NOT NULL
     ORDER BY 1
  ),
  cnt AS
  (
    SELECT COUNT(*) AS c FROM q
  )
  SELECT AVG(val)::float8
  FROM 
  (
    SELECT val FROM q
    LIMIT  2 - MOD((SELECT c FROM cnt), 2)
    OFFSET GREATEST(CEIL((SELECT c FROM cnt) / 2.0) - 1,0)  
  ) q2;
$$ LANGUAGE SQL IMMUTABLE;
 
CREATE AGGREGATE median(anyelement) (
  SFUNC=array_append,
  STYPE=anyarray,
  FINALFUNC=_final_median,
  INITCOND='{}'
);
"""
cursor.execute(function)
conn.commit()


"""Вопрос 4.Догадайтесь, в чём здесь измеряется возраст, и ответьте, 
на сколько месяцев (примерно) отличаются медианные значения возраста курящих и некурящих."""
cursor.execute("""
SELECT(((SELECT median(age)/365.25 FROM train WHERE smoke = '0') - (SELECT median(age)/365.25 FROM train WHERE smoke = '1')) * 12)
FROM train
""")
print(tabulate(fetch_all(cursor), "keys", "psql"))


"""Вопрос 5.Интересуют 2 подвыборки курящих мужчин возраста от 60 до 64 лет включительно: 
первая с верхним артериальным давлением строго меньше 120 мм рт.ст. и концентрацией холестерина – 4 ммоль/л, 
а вторая – с верхним артериальным давлением от 160 (включительно) до 180 мм рт.ст. (не включительно) и концентрацией холестерина – 8 ммоль/л."""
cursor.execute("""
SELECT(SELECT AVG(cardio) FROM train WHERE gender = '2' AND age >= '21915' AND age <= '23376' 
AND ap_hi >= 160 AND ap_hi < 180 AND smoke = '1' AND cholesterol = '1' )/
(SELECT AVG(cardio) FROM train WHERE gender = '2' AND age >= '21915' AND age <= '23376' 
AND ap_hi < 120 AND smoke = '1' AND cholesterol = '3' ) 
FROM train
""")
print(tabulate(fetch_all(cursor), "keys", "psql"))


"""Вопрос 6.Постройте новый признак – BMI (Body Mass Index).
Для этого надо вес в килограммах поделить на квадрат роста в метрах. 
Нормальными считаются значения BMI от 18.5 до 25.Выберите верные утверждения
 6.1. Медианный BMI по выборке превышает норму
"""
cursor.execute("""
SELECT median((SELECT weight :: int8 FROM train)/(SELECT (height/100)^2 FROM train)) AS med_BMI
FROM train
""")
print(tabulate(fetch_all(cursor), "keys", "psql"))

"""Вопрос 6.2.У женщин в среднем BMI ниже, чем у мужчин"""
cursor.execute("""
SELECT ((SELECT AVG(weight/(height/100)^2) FROM train WHERE gender = '1')/
(SELECT AVG(weight/(height/100)^2) FROM train WHERE gender = '2')) 
FROM train
""")
print(tabulate(fetch_all(cursor), "keys", "psql"))

"""Вопрос 6.3. У здоровых в среднем BMI выше, чем у больных"""
cursor.execute("""
SELECT ((SELECT AVG(weight/(height/100)^2) FROM train WHERE cardio = '0')/
(SELECT AVG(weight/(height/100)^2) FROM train WHERE cardio = '1')) 
FROM train
""") 
print(tabulate(fetch_all(cursor), "keys", "psql"))

"""Вопрос 6.4. В сегменте здоровых и непьющих мужчин 
в среднем BMI ближе к норме, чем в сегменте здоровых и непьющих женщин"""
cursor.execute("""
SELECT AVG(weight/(height/100)^2) FROM train WHERE gender = '2' AND alco = '0' AND cardio = '0'
SELECT AVG(weight/(height/100)^2) FROM train WHERE gender = '1' AND alco = '0' AND cardio = '0'
""")
print(tabulate(fetch_all(cursor), "keys", "psql"))


"""Вопрос 7 Отфильтруйте следующие сегменты пациентов (считаем это ошибками в данных)
   1)Указанное нижнее значение артериального давления строго выше верхнего
   2)Рост строго меньше 2.5%-перцентили или строго больше 97.5%-перцентили (используйте pd.Series.quantile, если не знаете, что это такое – прочитайте)
   3)Вес строго меньше 2.5%-перцентили или строго больше 97.5%-перцентили"""
cursor.execute("""
SELECT COUNT(height) as all, PERCENTILE_CONT(0.025) within group (ORDER BY height) as h_25,
PERCENTILE_CONT(0.975) within group (ORDER BY height) as h_975, 
PERCENTILE_CONT(0.025) within group (ORDER BY weight) as w_25,
PERCENTILE_CONT(0.975) within group (ORDER BY weight) as w_975
FROM train LIMIT 1 
"""
)
print(tabulate(fetch_all(cursor), "keys", "psql"))

""" Выборки показали , что в предложенных для анализа данных рост и вес должны соответствовать следующим неравенствам :
    150 <= Рост <=180
    51 <= Вес <= 108
    """

cursor.execute("""
SELECT DISTINCT ( 100 - (SELECT DISTINCT COUNT(*) * 100 FROM train WHERE ap_hi >= ap_lo AND height >= 150 
AND height <= 180 AND weight >= 51 AND weight <= 108) / (SELECT COUNT(*) FROM train ))) AS answer FROM train
"""
 )
print(tabulate(fetch_all(cursor), "keys", "psql")) 












