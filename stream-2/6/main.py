import os
import hashlib
import requests
import json
import sqlite3
from bs4 import BeautifulSoup

path = 'web-scraping/stream-2/6/'

def write_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def get_content(url):
    filename = path+"cache/"+hashlib.md5(url.encode('utf-8')).hexdigest()

    if os.path.exists(filename):
        with open(filename, 'r') as f:
            content = f.read()
        return content

    response = requests.get(
        url=url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        }
    )
    with open(filename, 'w') as f:
        f.write(response.text)
    return response.text


def parse_related_topics(url):
    # Завантажуємо HTML сторінку
    content = get_content(url)
    soup = BeautifulSoup(content, 'lxml')
    # Знаходимо блок з атрибутом data-component="topic-list" так як класси можуть бути динамічними
    topic_list_block = soup.find('div', {'data-component': 'topic-list'})
    # Якщо блок знайдено, шукаємо посилання всередині
    if topic_list_block:
        topics = topic_list_block.find_all('a')
        related_topics = [topic.text.strip() for topic in topics]
    else:
        related_topics = []
    return related_topics


def parse_html():
    url = "https://www.bbc.com/sport"
    # Завантажуємо HTML сторінку
    content = get_content(url)
    soup = BeautifulSoup(content, 'lxml')
    # Знаходимо всі елементи з атрибутом data-testid="promo" так як класси можуть бути динамічними
    promo_blocks = soup.find_all('div', {'data-testid': 'promo'}) # , limit=5
    news_topics = []
    for promo in promo_blocks:
        # Збираємо посилання на перші 5 новини
        link_tag = promo.find('a', href=True)
        if link_tag:
            link = "https://www.bbc.com" + link_tag['href']
            # Парсимо "Related Topics"
            related_topics = parse_related_topics(link)
            news_topics.append({
                "Link": link,
                "Topics": related_topics
            })
            if 5 == len(news_topics): # робимо limit=5 тут на випадок, якщо "promo" буде без посилання
                break

    return news_topics

def write_sqlite(filename, data):
    # створюємо з'єднання з sqlite
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    # створюємо таблицю news_topics, якщо такої щє не існує
    sql = """
        create table if not exists news_topics (
            id integer primary key,
            link text,
            topics text
        )
    """
    cursor.execute(sql)
    # записуємо в таблицю по одному перелік назв вакансій та url
    for entry in data:
        cursor.execute("""
            insert into news_topics (link, topics)
            values (?, ?)
        """, (entry["Link"], ', '.join(entry['Topics'])))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    news_topics = parse_html()
    print("1 список із посилань і Related Topics:\n", news_topics, "\n\n")
    write_json(path+'news_topics_.json', news_topics)
    print("2 збережено результат у форматі JSON", "\n")
    write_sqlite(path+'news_topics_.db', news_topics)
    print("3 збережено результат в базі даних SQLite", "\n")
