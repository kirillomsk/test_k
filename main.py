from selenium import webdriver
import psycopg2


driver = webdriver.Chrome()
driver.get('https://checkme.kavichki.com/')

conn = psycopg2.connect(host="127.0.0.1", port='5432', database="postgres", user="postgres", password="123456789")
cur = conn.cursor()

res = {}
for i in range(len(driver.find_elements_by_css_selector('tr')) - 1):
    _ = []
    for j in range(3):
        _.append(driver.find_element_by_css_selector(f'tr:nth-child({i+1}) > td:nth-child({j+1})').text)
    res[i] = _

cur.execute('CREATE TABLE shopping_list (buy text, how text, price text);')
conn.commit()

for i in res:
    cur.execute(f"INSERT INTO shopping_list (buy, how, price) VALUES ('{res[i][0]}', '{res[i][1]}', '{res[i][2]}');")
    conn.commit()

cur.close()
conn.close()
driver.close()
