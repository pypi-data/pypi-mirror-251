from time import sleep
import re

from seleniumpagefactory import PageFactory


class AssertPageError(Exception):
    pass


class AssertPageMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    title = None

    def assert_page(self, title_extension=None):
        if not self.title:
            raise AttributeError(f'class attribute: title is not set!')
        title = self.title + title_extension if title_extension else self.title
        if self.driver.title != title:
            raise AssertPageError(f'title of driver: {self.driver.title} != title of page: {title}')


class NavLocatorsMixin:
    nav_locators = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.locators.update(self.nav_locators)


class FormButtonsMixin:
    form_buttons = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        form_buttons = self._create_locators(self.form_buttons)
        self.locators.update(form_buttons)

    def _create_locators(self, form_buttons):
        output = {}
        for key in form_buttons:
            if isinstance(key, tuple):
                loc = key[1]
                output[key[0]] = (
                    loc,
                    ' '.join([x.capitalize() for x in key[0].replace('and', '&').split('_')])
                )
            else:
                output[key] = (
                    "CSS",
                    f"input[value='{' '.join([x.capitalize() for x in key.replace('and', '&').split('_')])}']")
        return output

    def __getattr__(self, item):
        search = re.search(r'^click_(.*)', item)
        if search:
            locator = search.group(1)
            return self._click(loc=locator)

        return super().__getattr__(item)


class ExtendedPageFactory(AssertPageMixin, NavLocatorsMixin, FormButtonsMixin, PageFactory):
    locators = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.locators:
            print('No locators set!')
