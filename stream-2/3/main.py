# Домашнє завдання
# Опис завдання:

# У цьому домашньому завданні ви зможете попрактикуватися в різних методах вилучення даних. Домашнє завдання складається з двох частин

# 1 Використовуючи отримані знання на занятті, напишіть регулярні вирази для парсингу email та дати.
#   - Файл із вправами https://docs.google.com/document/d/1xO-xH6IAvDYRxei4FBpGOOB4J_a3mqrsJQoB7jlMQQo/edit
# 2 Також попрактикуйтеся в написанні XPath для HTML-сторінки https://br.indeed.com/
#   - Input для введення пошукового запиту
#   - Input для введення регіону
#   - Кнопка пошуку

# Завдання з *
# (не обовʼязкове)
# Спробуйте написати regexp для номерів телефону та посилань URL
# Формат здачі завдання:
# Отриманий результат прикріпіть у відповідне поле в LMS до даного заняття за допомогою посилання на github.


import re
# import xml.etree.ElementTree as ET
from lxml import etree
import requests
import hashlib

text = """Welcome to the Regex Training Center! 

01/02/2021, 12-25-2020, 2021.03.15, 2022/04/30, 2023.06.20, and 2021.07.04. You can
also find dates with words: March 14, 2022, and December 25, 2020. 

(123) 456-7890, +1-800-555-1234, 800.555.1234, 800-555-1234, and 123.456.7890. 
Other formats include international numbers: +44 20 7946 0958, +91 98765 43210.

john.doe@example.com, jane_doe123@domain.org, support@service.net, info@company.co.uk, 
and contact.us@my-website.com. You might also find these tricky: weird.address+spam@gmail.com,
"quotes.included@funny.domain", and this.one.with.periods@weird.co.in.

http://example.com, https://secure.website.org, http://sub.domain.co, 
www.redirect.com, and ftp://ftp.downloads.com. Don't forget paths and parameters:
https://my.site.com/path/to/resource?param1=value1&param2=value2, 
http://www.files.net/files.zip, https://example.co.in/api/v1/resource, and 
https://another-site.org/downloads?query=search#anchor. 

0x1A3F, 0xBEEF, 0xDEADBEEF, 0x123456789ABCDEF, 0xA1B2C3, and 0x0. 

#FF5733, #C70039, #900C3F, #581845, #DAF7A6, and #FFC300. RGB color codes can be tricky: 
rgb(255, 99, 71), rgba(255, 99, 71, 0.5).

123-45-6789, 987-65-4321, 111-22-3333, 555-66-7777, and 999-88-7777. Note that Social 
Security numbers might also be written like 123 45 6789 or 123456789.

Let's throw in some random sentences for good measure:
- The quick brown fox jumps over the lazy dog.
- Lorem ipsum dolor sit amet, consectetur adipiscing elit.
- Jack and Jill went up the hill to fetch a pail of water.
- She sells seashells by the seashore.

1234567890, !@#$%^&*()_+-=[]{}|;':",./<>?, 3.14159, 42, and -273.15.
"""

def use_re():
    print("1 регулярні вирази для парсингу email та дати.\n")
    # Регулярний вираз для пошуку email
    emails = re.findall(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', text)
    print("emails:", emails, "\n")

    #   re.findall(r'\d{2}[\/\-]\d{2}[\/\-]\d{4}', text)  # — для дат у форматі DD/MM/YYYY або MM-DD-YYYY.
    #   re.findall(r'\d{4}[\/\.]\d{2}[\/\.]\d{2}', text)  # — для дат у форматі YYYY.MM.DD або YYYY/MM/DD.
    #   re.findall(r'\b(January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}\b', text)  # — для дат з місяцями у текстовому форматі

    # Об'єднаний регулярний вираз для всіх тіпів дат
    dates = re.findall(r'\b(\d{2}[\/\-]\d{2}[\/\-]\d{4}|\d{4}[\/\.]\d{2}[\/\.]\d{2}|(January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4})\b', text)
    # Перебор массиву для отримання тільки дат (Match), без додаткових рядків підпошуку (Group)
    dates = [date[0] for date in dates] 
    print("dates:", dates, "\n")

def use_re_2():
    print("3 regexp для номерів телефону та посилань URL.\n")
    # Регулярний вираз для номерів телефону
    phones = re.findall(r'((\+\d{1,3}[-.\s]?)?[0-9]{3}?[-.\s][0-9]{3}[-.\s][0-9]{4}\b|\(\d{3}\)[\s]?[0-9]{3}[-]?[0-9]{4}\b|\+\d{10,12}\b|\+[\d\s]{14,15})\b', text)
    phones = [phone[0] for phone in phones]
    print("phones:", phones, "\n")

    # Регулярний вираз  для посилань URL 
    urls = re.findall(r'\b(?:(?:https?|ftp):\/\/|www\.)[a-zA-Z0-9-]+(?:\.[a-zA-Z]{2,})+(?:\/[^\s]*)?(?:\?[^\s#]*)?(?:#[^\s]*)?\b', text)
    print("urls:", urls, "\n")


def get_content(url):
    name = "web-scraping/stream-2/3/"+hashlib.md5(url.encode('utf-8')).hexdigest()
    try:
        with open(name, 'r') as f:
            content = f.read()
            return content
    except:
        response = requests.get(url)  # 'https://br.indeed.com/ return status_code 403 
        print('request was sent')
        with open(name, 'w') as f:
            f.write(response.text)
        return response.text

def parse_html(html):
    tree = etree.HTML(html)

    xpath_form = '//form[@id="jobsearch"]'
    xpath_form_input_what = xpath_form+'//input[@id="text-input-what"]'
    xpath_form_input_where = xpath_form+'//input[@id="text-input-where"]'
    xpath_form_input_button = xpath_form+'//button[@type="submit"]'

    tag_form_input_what = tree.xpath(xpath_form_input_what)
    tag_form_input_where = tree.xpath(xpath_form_input_where)
    tag_form_input_button = tree.xpath(xpath_form_input_button)

    print("2 XPath для HTML-сторінки https://br.indeed.com/ \n")
    print("text-input-what:", tag_form_input_what[0], "\n   label:", tree.xpath(xpath_form_input_what+"/@aria-label"), "\n")
    print("text-input-where:", tag_form_input_where[0], "\n   label:", tree.xpath(xpath_form_input_where+"/@aria-label"), "\n")
    print("submit-button:", tag_form_input_button[0], "\n   text:", tag_form_input_button[0].text, "\n")


if __name__ == '__main__':
    use_re()
    html = get_content('https://br.indeed.com/')
    parse_html(html)
    use_re_2()