from __future__ import print_function
import io
import os
import re
import requests
import sys
from bs4 import BeautifulSoup
from collections import deque


def build_absolute_url(base, extension):
    """Return an absolute url given a base url and a relative url."""
    print('\nbase:\t\t{}'.format(base))
    print('extension:\t{}'.format(extension))
    if extension == '/':
        url = base
    elif extension[:3] == '../':
        # safe to mutate base, extension
        base = re.sub(r'[^/]*$', '', base)
        while extension[:3] == r'../':
            extension = extension[3:]
            base = re.sub(r'[^/]*/$', '', base)
        url = ''.join([base, extension])
    elif extension[:2] == '//':
        base = re.sub(r':.*$', ':', base)
        url = ''.join([base, extension])
    elif extension[0] != r'/':
        url = re.sub(r'[^/]*\.[^/]*$', extension, base)
    else:
        url = '/'.join([base, extension])
    url = re.sub(r'(?<!\:)/{2,}', '/', url)  # remove extra forward slashes
    print('url:\t\t{}'.format(url))
    return url


def get_links(root_url):
    """Yield links on page for given url."""
    response = requests.get(root_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    a_tags = soup.find_all('a', href=True)
    for a_tag in a_tags:
        link = a_tag['href']
        if 'http' in link and root_url in link and '#' not in link:
            yield link
        elif 'http' not in link and '/' in link and '#' not in link:
            absolute_link = build_absolute_url(response.url, link)
            yield absolute_link


def write_to_file(url):
    """Write vanilla html file to disk for given url."""
    # TODO: deal with url forward slashes better
    # TODO: write filenames such that links in response.content work
    # TODO: write files into a directory structure (not flatly)
    try:
        filename = ''.join(['../data/',
                            url.replace(r'/', '_'),
                            '.html'])
        if os.path.isfile(filename):
            return print('File found: {}'.format(url))
        response = requests.get(url)
        good_response = response.status_code // 100 in set([2, 3])
        if good_response:
            with io.open(filename, 'wb') as fh:
                for chunk in response.iter_content(8192):
                    fh.write(chunk)
            print('Wrote {}'.format(filename))
    except requests.exceptions.RequestException as e:
        print(e)


def scrape(root_url):
    """Write html file for all pages containing given root url.

    Uses breadth first traversal."""
    queue = deque()
    visited = set()  # order unimportant
    queue.appendleft(root_url)
    # TODO: determine depth from root for given node
    try:
        while queue:
            cursor = queue.pop()
            write_to_file(cursor)
            for link in get_links(cursor):
                if link not in visited:
                    visited.add(link)
                    queue.appendleft(link)
    finally:
        print(visited)


if __name__ == '__main__':
    scrape(*sys.argv[1:])
