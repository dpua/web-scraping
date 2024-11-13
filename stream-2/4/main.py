import requests
import re

def get_vacancy_list(text):
    # знаходимо в html контенті всі теги h3 з классом "jobCard_title m-0" і вилучаємо з них весь контент 
    pattern = '<h3 class="jobCard_title m-0">(.+?)</h3>'
    # re.findall повертає массив всіх знайдених назв вакансій
    vacancies = re.findall(pattern, text) 
    return vacancies

def get_vacancy_list_of_objects(text):
    # знаходимо в html контенті всі батьківські теги article з id яке почінається з "post-"
    # в ньому шукаємо єдиний тег "a", і з нього вілучаємо посилання на вакансію href
    # та тег h3 з классом "jobCard_title m-0" і вилучаємо з нього весь контент
    pattern = '<article id="post-\d+"[\s\S]+?<a href="(.*?)"[\s\S]+?<h3 class="jobCard_title m-0">(.*?)</h3>'
    # re.findall повертає массив всіх знайдених назв вакансій та їх посилань
    matches = re.findall(pattern, text)
    # формуємо массив об'єктів з назвами та посиланнями на вакансію
    vacancy_list_of_objects = [{"title": title, "url": url} for url, title in matches]
    return vacancy_list_of_objects

def get_content(url):
    # методом get робимо запит на сторінку
    response = requests.get(url)
    print('request was sent\nresponse status code:',response.status_code, "\n")
    # повертаємо отриманний текстовий html контент сторінки
    return response.text

if __name__ == '__main__':
    text = get_content('https://www.lejobadequat.com/emplois')
    print("1 контент першої сторінки сайту https://www.lejobadequat.com/emplois:\n", text[:15], "...\n")
    vacancy_list = get_vacancy_list(text)
    print("2 перелік назв вакансій:\n", vacancy_list, "\n")
    vacancy_list_of_objects = get_vacancy_list_of_objects(text)
    print("3 список із назв вакансій і посилань на вакансії:\n", vacancy_list_of_objects, "\n")
