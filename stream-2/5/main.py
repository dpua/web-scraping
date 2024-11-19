import requests
import re
import csv
import json
from pprint import pprint
import xml.etree.ElementTree as ET
import sqlite3

def get_content(url):
    # методом get робимо запит на сторінку
    response = requests.get(url)
    print('request was sent\nresponse status code:',response.status_code, "\n")
    # повертаємо отриманний текстовий html контент сторінки
    return response.text

def get_vacancy_list_of_objects(text):
    # знаходимо в html контенті всі батьківські теги article з id яке почінається з "post-"
    # в ньому шукаємо єдиний тег "a", і з нього вілучаємо посилання на вакансію href
    # та тег h3 з классом "jobCard_title m-0" і вилучаємо з нього весь контент
    pattern = '<article id="post-\d+"[\s\S]+?<a href="(.*?)"[\s\S]+?<h3 class="jobCard_title m-0">(.*?)</h3>'
    # re.findall повертає массив всіх знайдених назв вакансій та їх посилань
    matches = re.findall(pattern, text)
    # формуємо массив об'єктів з назвами та посиланнями на вакансію
    vacancy_list_of_objects = [{"id": index + 1, "title": title, "url": url}  for index, (url, title) in enumerate(matches)]
    return vacancy_list_of_objects

def write_json(filename, data):
    pprint(data, "\n")
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def write_sqlite_vacancy(filename, data):
    # створюємо з'єднання з sqlite
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    # створюємо таблицю vacancy, якщо такої щє не існує
    sql = """
        create table if not exists vacancy (
            id integer primary key,
            title text,
            url text
        )
    """
    cursor.execute(sql)
    # запісуємо в таблицю по одному перелік назв вакансій та url
    for entry in data:
        cursor.execute("""
            insert into vacancy (title, url)
            values (?, ?)
        """, (entry["title"], entry["url"]))
    conn.commit()
    conn.close()

def read_sqlite_vacancy(filename):
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    # 1. get all data
    sql = """
        select id, title, url
        from vacancy
    """
    rows = cursor.execute(sql).fetchall()
    print(rows, "\n")
    conn.close()

def write_csv_vacancy(filename, data):
    vacancy_list = [[str(entry["id"]), entry["title"], str(entry["url"])] for entry in data]
    print("vacancy_list:", "\n", vacancy_list, "\n")
    with open(filename, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'title', 'url'])
        writer.writerows(vacancy_list)

def write_xml_vacancy(filename, data):
    root = ET.Element('VacancyList')
    for entry in data:
        person = ET.SubElement(root, 'Vacancy')
        ET.SubElement(person, 'ID').text = str(entry["id"])
        ET.SubElement(person, 'Title').text = entry["title"]
        ET.SubElement(person, 'URL').text = str(entry["url"])

    tree = ET.ElementTree(root)
    tree.write(filename, encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
    text = get_content('https://www.lejobadequat.com/emplois')
    print("1 контент першої сторінки сайту https://www.lejobadequat.com/emplois:\n", text[:15], "...\n")
    vacancy_list_of_objects = get_vacancy_list_of_objects(text)
    print("2 список із назв вакансій і посилань на вакансії:\n", vacancy_list_of_objects, "\n")
    path = 'web-scraping/stream-2/5/'
    write_json(path+'vacancy.json', vacancy_list_of_objects)
    print("3 збережено результат у форматі JSON", "\n")
    write_sqlite_vacancy(path+'vacancy.db', vacancy_list_of_objects)
    print("4 збережено результат в базі даних SQLite", "\n")
    read_sqlite_vacancy(path+'vacancy.db')
    write_csv_vacancy(path+'vacancy.csv', vacancy_list_of_objects)
    print("5 збережено результат у форматі CSV", "\n")
    write_xml_vacancy(path+'vacancy.xml', vacancy_list_of_objects)
    print("6 збережено результат у форматі XML", "\n")