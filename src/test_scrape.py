import pytest
import requests

BUILD_URL = [
    ('http://website.com', '/', 'http://website.com'),
    ('http://website.com/dir/page.html',
     '../another_page.html',
     'http://website.com/another_page.html'),
    ('http://website.com/dir/another_dir/page.html',
     '../../another_page.html',
     'http://website.com/another_page.html'),
    ('http://website.com',
     '//another_website.com',
     'http://another_website.com'),
    ('http://website.com/page.html',
     'another_page.html',
     'http://website.com/another_page.html'),
    ('http://website.com',
     '/another_page.html',
     'http://website.com/another_page.html'),
    ('http://website.com',
     '/dir///another_dir//another_page.html',
     'http://website.com/dir/another_dir/another_page.html'),
]

GET_LINKS = [
    ('http://www.google.com',
     ['http://www.google.com/services/',
      'http://www.google.com/intl/en/about.html',
      'http://www.google.com/preferences?hl=en',
      'http://www.google.com/intl/en/policies/terms/']),
]


@pytest.mark.parametrize(('base', 'extension', 'expected'), BUILD_URL)
def test_build_absolute_url(base, extension, expected):
    from scrape import build_absolute_url
    assert build_absolute_url(base, extension) == expected


@pytest.mark.parametrize(('root_url', 'expected'), GET_LINKS)
def test_get_links(root_url, expected):
    from scrape import get_links
    links = [l for l in get_links(root_url)]
    for expected in expected:
        assert expected in links


# def test_write_to_file():
#     assert False
# 
# 
# def test_scrape():
#     assert False
