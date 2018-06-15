import argparse
import random
import sys

from lxml import etree
import requests
from requests import ConnectionError
from bs4 import BeautifulSoup


def execute_get_request(url):
    try:
        response = requests.get(url)
        return response.content if response.ok else None
    except ConnectionError:
        return None


def get_urls_from_xml_content(xml_content, random_urls_count):
    urlset = etree.fromstring(xml_content)

    urls = [loc.text for url in urlset for loc in url]

    if len(urls) > random_urls_count:
        return random.sample(urls, random_urls_count)
    else:
        return urls


def get_coursera_courses_urls(random_urls_count):
    xml_content = execute_get_request(
        url='https://www.coursera.org/sitemap~www~courses.xml',
    )
    if xml_content is None:
        return None

    return get_urls_from_xml_content(xml_content, random_urls_count)


def get_tag_text(tag):
    return None if tag is None else tag.text


def fetch_course_info(course_page_content):
    soup = BeautifulSoup(course_page_content, 'lxml')

    title = get_tag_text(tag=soup.find('h1', class_='title'))
    language = get_tag_text(tag=soup.find('div', class_='rc-Language'))
    start_date = get_tag_text(tag=soup.find(id='start-date-string'))
    weeks_count = len(soup.find_all('div', class_='week'))
    average_rating = get_tag_text(tag=soup.find(class_='ratings-text'))

    return title, language, start_date, weeks_count, average_rating


def get_coursera_courses_info(courses_urls):
    coursera_courses_info = {}

    for course_url in courses_urls:
        course_page_content = execute_get_request(course_url)

        if course_page_content is None:
            return None

        course_info = fetch_course_info(course_page_content)

        coursera_courses_info[course_url] = course_info

    return coursera_courses_info


def parse_command_line_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'output',
        help='a xlsx file to save info about Coursera courses',
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

    coursera_courses_info = get_coursera_courses_info(
        courses_urls=coursera_courses_urls,
    )

    if coursera_courses_info is None:
        sys.exit('Could not get info about Coursera courses')


if __name__ == '__main__':
    main()
