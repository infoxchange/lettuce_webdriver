"""
Lettuce Webdriver
"""

import os
import yaml

import selenium.webdriver

from lettuce import world, after

import webdriver


__all__ = ['initialize']


class ConfigError(Exception):
    """
    A YAML config error
    """

    pass


# pylint:disable=too-many-branches, too-many-statements
def initialize(config, default):
    """
    Initialize lettuce-webdriver using specified config.

    Config is specified in YAML.
    """

    with open(config) as file_:
        data = yaml.load(file_)

        try:
            browser = os.environ.get('WEBDRIVER', default)
            browser = data[browser]
        except KeyError:
            raise ConfigError("Unknown browser '{browser}'".format(
                browser=browser))

    remote = browser.get('remote', False)
    config = {}

    # determine base capabilities
    try:
        if browser['webdriver'] == 'ie':
            caps_str = 'INTERNETEXPLORER'
        else:
            caps_str = browser['webdriver'].upper()

        caps = getattr(selenium.webdriver.DesiredCapabilities, caps_str)
    except KeyError:
        raise ConfigError("Must specify 'driver'")
    except AttributeError:
        raise ConfigError("Unknown driver: {driver}".format(
            browser['driver']))

    # merge capabilities overrides
    caps.update(browser.get('capabilities', {}))

    if remote:
        hub = None
        hub_fmt = 'http://{host}:4444/wd/hub'

        if 'WEBDRIVER_HUB' in os.environ:
            hub = os.environ['WEBDRIVER_HUB']
        elif 'WEBDRIVER_HOST' in os.environ:
            hub = hub_fmt.format(host=os.environ['WEBDRIVER_HOST'])
        elif 'hub' in browser:
            hub = browser['hub']
        elif 'host' in browser:
            hub = hub_fmt.format(host=browser['host'])
        elif 'command_executor' in browser:
            hub = browser['command_executor']
        else:
            raise ConfigError("Must specify a hub or host to connect to")

        config['command_executor'] = hub

    if remote or \
       browser['webdriver'] == 'chrome' or \
       browser['webdriver'] == 'phantomjs':
        config['desired_capabilities'] = caps
    else:
        config['capabilities'] = caps

    # determine WebDriver
    if remote:
        driver = selenium.webdriver.Remote
    else:
        driver = browser['webdriver']

        if driver == 'phantomjs':
            driver = 'PhantomJS'
        else:
            driver = driver.capitalize()

        driver = getattr(selenium.webdriver, driver)

    return driver(**config)


@after.each_scenario  # pylint:disable=no-member
def disable_beforeunload(scenario):
    """
    Disable before unload after a scenario so that the next scenario can
    reload the site.
    """

    world.browser.execute_script("""
try {
    $(window).off('beforeunload');
} catch (e) {
}
    """)
