=============================================
Lettuce steps for Web Testing with Selenium 2
=============================================

``lettuce_webdriver`` provides a set of steps for use with the `Cucumber
<http://cukes.info/>`_ BDD Python port `lettuce <http://lettuce.it/>`_ using
the `selenium 2.8 or higher Python package <http://pypi.python.org/pypi/selenium>`_.

The included matchers and syntax is inspired heavily by `cucumber_watir
<https://github.com/napcs/cucumber_watir>`_.

Requirements
============

* `lettuce <http://lettuce.it/>`_
* `selenium 2.30 or higher <http://pypi.python.org/pypi/selenium>`_

Setting Up lettuce_webdriver
============================

In your lettuce ``terrain.py`` file, add an include statement for lettuce to
learn about the additional step definitions provided by
``lettuce_webdriver`` and a setup that creates the selenium browser
desired::
    
    from lettuce import before, world
    import lettuce_webdriver

    @before.all
    def setup_browser():
        world.browser = lettuce_webdriver.initialize('browsers.yaml', 'firefox')

    @after.all
    def destroy_browser():
        world.browser.quit()


Where ``firefox`` is your default driver to use and ``browsers.yaml`` contains
your browser configurations::

    firefox:
        webdriver: firefox

    remote-ie:
        webdriver: ie
        remote: true
        host: int-selenium-hub
        capabilities:
            version: 10

Accepted parameters are ``webdriver``, ``remote``, ``host``, ``hub`` and
``capabilities``. ``browsers.yaml`` normalizes ``capabilities`` and
``desired_capabilities`` based on webdriver.

The default webdriver, host and hub can be overridden using the ``WEBDRIVER``,
``WEBDRIVER_HOST`` and ``WEBDRIVER_HUB`` environment variables respectively::

    WEBDRIVER=remote-ie lettuce

You can use YAML includes to set configuration for a common service, e.g.
your Selenium hub, or Browserstack::

    defaults:
        - &browserstack
          remote: true
          host: hub.browserstack.com
        - &browserstack_key
          browserstack.user: mr.lettuce
          browerstack.key: abcd1234

    browserstack-ie10:
        <<: *browserstack
        webdriver: ie
        capabilities:
            <<: *browserstack_key
            version: 10

The old method for setting up lettuce_webdriver, where you defined your
WebDriver yourself is still supported. Include Selenium directly and assign a
webdriver to ``world.browser``.

Usage
=====

lettuce stories are written in the standard Cucumber style of `gherkin
<https://github.com/aslakhellesoy/cucumber/wiki/gherkin>`_. For example::
    
    Scenario: Filling out the signup form
      Given I go to "http://foo.com/signup"
       When I fill in "Name" with "Foo Bar"
        And I fill in "Email" with "nospam@gmail.com"
        And I fill in "City" with "San Jose"
        And I fill in "State" with "CA"
        And I uncheck "Send me spam!"
        And I select "Male" from "Gender"
        And I press "Sign up"
       Then I should see "Thank you for signing up!"


Included Matchers
-----------------

The following lettuce step matchers are included in this package and can be
used with Given/When/Then/And as desired.

::

    # urls
    I visit "http://google.com/"
    I go to "http://google.com/"
    
    # links
    I click "Next page"
    I should see a link with the url "http://foobar.com/"
    I should see a link to "Google" with the url "http://google.com/"
    I should see a link that contains the text "Foobar" and the url "http://foobar.com/"

    # general
    I should see "Page Content"
    I see "Page Content"
    I should see "Page Content" within 4 seconds
    I should not see "Foobar"
    I should be at "http://foobar.com/"
    I should see an element with id of "http://bar.com/"
    I should see an element with id of "http://bar.com/" within 2 seconds
    I should not see an element with id of "http://bar.com/"
    The element with id of "cs_PageModeContainer" contains "Read"
    The element with id of "cs_BigDiv" does not contain "Write"

    # browser
    The browser's URL should be "http://bar.com/"
    The browser's URL should contain "foo.com"
    The browser's URL should not contain "bar.com"
    
    # forms
    I should see a form that goes to "http://bar.com/submit.html"
    I press "Submit"
    
    # checkboxes
    I check "I have a car"
    I uncheck "I have a bus"
    The "I have a car" checkbox should be checked
    The "I have a bus" checkbox should not be checked
    
    # select
    I select "Volvo" from "Car Choices"
    I select the following from "Car Choices":
        """
        Volvo
        Saab
        """
    The "Volvo" option from "Car Choices" should be selected
    The following options from "Car Choices" should be selected:
        """
        Volvo
        Saab
        """
    
    # radio buttons
    I choose "Foobar"
    The "Foobar" option should be chosen
    The "Bar" option should not be chosen
    
    # text entry fields (text, textarea, password)
    I fill in "Username" with "Smith"

Support
=======

lettuce_webdriver is maintained by Nick Pilon (@npilon on github and
npilon@lexmachina.com). Bug fixes and feature patches may be submitted using
github pull requests, and bug reports or feature requests as github issues.
