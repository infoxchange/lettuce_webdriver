# pylint:disable=invalid-name,missing-docstring
import os

from lettuce import world

import lettuce_webdriver

here = os.path.dirname(__file__)
html_pages = os.path.join(here, 'html_pages')

def setUp():
    world.browser = lettuce_webdriver.initialize(
        os.path.join(here, 'browsers.yaml'),
        'firefox')


def tearDown():
    world.browser.quit()
