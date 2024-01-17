An extension for PageFactory class (selenium-page-factory)

Main class:

**ExtendedPageFactory(AssertPageMixin, NavLocatorsMixin, FormButtonsMixin, PageFactory)**

Mixins:

**AssertPageMixin** (title) -> Checks if the current page has the same title as given. The "assert_page" method verifies
if the title of the html page is the same as the title property of this class. It accepts a string as its argument
title_extension which will be concatenated to the title property.

**NavLocatorsMixin** (nav_locators) -> Provides a class attribute to be added to PageFactory attribute locators. This is
a convenient way to add common navbar locators to several Page classes.

**FormButtonsMixin** (form_buttons) -> Provides a list of form inputs such as save (value='Save'), save_and_new (
value='Save & New'), delete (value='Delete') etc. as a class attribute (form_buttons=[save, save_and_new, delete]). If
a tuple is given the second value indicates the locator. For example if the cancel button is in reality a
link: `<a href="">Cancel</a>`, add (cancel, "LINK_TEXT") to form_buttons.

