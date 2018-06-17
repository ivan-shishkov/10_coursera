import argparse
import random
import sys

from lxml import etree
import requests
from requests import ConnectionError
from bs4 import BeautifulSoup
from openpyxl import Workbook


def fetch_content(url):
    try:
        response = requests.get(url)
        return response.content if response.ok else None
    except ConnectionError:
        return None


def get_random_urls(urls, random_urls_count):
    if len(urls) > random_urls_count:
        return random.sample(urls, random_urls_count)
    else:
        return urls


def get_urls_from_xml_content(xml_content):
    urlset = etree.fromstring(xml_content)

    return [loc.text for url in urlset for loc in url]


def get_coursera_courses_urls(random_urls_count):
    xml_content = fetch_content(
        url='https://www.coursera.org/sitemap~www~courses.xml',
    )
    if xml_content is None:
        return None

    return get_random_urls(
        urls=get_urls_from_xml_content(xml_content),
        random_urls_count=random_urls_count,
    )


def get_tag_text(tag):
    return None if tag is None else tag.text


def fetch_course_info(course_page_content):
    soup = BeautifulSoup(course_page_content, 'lxml')

    title = get_tag_text(tag=soup.find('h1', class_='title'))
    language = get_tag_text(tag=soup.find('div', class_='rc-Language'))
    start_date = get_tag_text(tag=soup.find(id='start-date-string'))
    weeks_count = len(soup.find_all('div', class_='week'))
    average_rating = get_tag_text(tag=soup.find(class_='ratings-text'))

    return [title, language, start_date, weeks_count, average_rating]


def get_coursera_courses_info(courses_urls):
    coursera_courses_info = []

    for course_url in courses_urls:
        course_page_content = fetch_content(course_url)

        if course_page_content is None:
            return None

        course_info = fetch_course_info(course_page_content)
        course_info.append(course_url)

        coursera_courses_info.append(course_info)

    return coursera_courses_info


def add_course_info(excel_worksheet, course_info):
    excel_worksheet.append(
        ['N/A' if element is None else element for element in course_info],
    )


def save_excel_workbook(excel_workbook, xlsx_filepath):
    try:
        excel_workbook.save(xlsx_filepath)
        return True
    except PermissionError:
        return False


def write_courses_info_to_excel_workbook(courses_info):
    excel_workbook = Workbook()
    excel_worksheet = excel_workbook.active

    excel_worksheet.title = 'Info About Coursera Courses'

    excel_worksheet.append(
        ('Title', 'Language', 'Starts', 'Weeks', 'Average Rating', 'URL'),
    )

    for course_info in courses_info:
        add_course_info(excel_worksheet, course_info)

    return excel_workbook


def parse_command_line_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--output',
        help='a xlsx file to save info about Coursera courses',
        default='coursera_courses_info.xlsx',
        type=str,
    )
    parser.add_argument(
        '--count',
        help='a count of randomly selected Coursera courses (default: 20)',
        default=20,
        type=int,
    )
    command_line_arguments = parser.parse_args()

    return command_line_arguments


def main():
    command_line_arguments = parse_command_line_arguments()

    output_filepath = command_line_arguments.output
    courses_count = command_line_arguments.count

    coursera_courses_urls = get_coursera_courses_urls(
        random_urls_count=courses_count,
    )

    if coursera_courses_urls is None:
        sys.exit('Could not get Coursera courses URLs')

    print('Getting info about Coursera courses...')

    courses_info = get_coursera_courses_info(
        courses_urls=coursera_courses_urls,
    )

    if courses_info is None:
        sys.exit('Could not get info about Coursera courses')

    if not save_excel_workbook(
            excel_workbook=write_courses_info_to_excel_workbook(courses_info),
            xlsx_filepath=output_filepath):
        sys.exit('Could not save file to given directory. Permission denied.')

    print('Info about Coursera courses successfully saved to {}'.format(
        output_filepath,
    ))


if __name__ == '__main__':
    main()
