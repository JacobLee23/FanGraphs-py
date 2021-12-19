#! usr/bin/env python
# fangraphs/selectors.py

"""

"""

from typing import *

import bs4

from .logger import logger


class FilterWidget:
    """

    """
    _descendants: tuple[str]

    def options(self) -> tuple[Union[str, bool]]:
        """

        :return:
        """
        raise NotImplementedError

    def current(self, page) -> Union[str, bool]:
        """

        :type page: playwright.sync_api._generated.Page
        :return:
        """
        raise NotImplementedError

    async def acurrent(self, page) -> Union[str, bool]:
        """

        :type page: playwright.async_api._generated.Page
        :return:
        """
        raise NotImplementedError

    def configure(self, page, option: Union[str, bool]) -> None:
        """

        :type page: playwright.sync_api._generated.Page
        :param option:
        """
        raise NotImplementedError

    async def aconfigure(self, page, option: Union[str, bool]) -> None:
        """

        :type page: playwright.async_api._generated.Page
        :param option:
        """
        raise NotImplementedError


class Selection(FilterWidget):
    """

    """
    _descendants = (
        "ul > li", "a", "div.button-green.fgButton"
    )

    def __init__(self, soup: bs4.BeautifulSoup, root: Union[str, Sequence[str]]):
        """
        :param soup:
        :param root:
        """
        self.soup = soup

        self.root = root
        self.descendant = ""

    def options(self) -> tuple[str]:
        """

        :return:
        """
        options = ()

        if isinstance(self.root, str):
            root_elem = self.soup.select_one(self.root)
            for desc in self._descendants:
                if elems := root_elem.select(desc):
                    options = [e.text for e in elems]
                    self.descendant = desc
        else:
            options = [
                e.text for e in [
                    self.soup.select_one(s) for s in self.root
                ]
            ]

        return tuple(options)

    def current(self, page) -> None:
        """

        :type page: playwright.sync_api._generated.Page
        :return:
        """
        current = ""

        if isinstance(self.root, str):
            if self.descendant:
                _ = self.options()

            root_elem = self.soup.select_one(self.root)

            if self.descendant == self._descendants[0]:
                current = e.text if (
                    e := root_elem.select_one(".rtsLink.rtsSelected")
                ) else ""
            elif self.descendant == self._descendants[1]:
                elems = root_elem.select(self.descendant)
                for elem in elems:
                    if "active" in elem.attrs.get("class"):
                        current = elem.text
            elif self.descendant == self._descendants[2]:
                elem = root_elem.select_one(
                    "div.button-green.fgButton.active.isActive"
                )
                current = elem.text
        else:
            for path in self.root:
                elem = self.soup.select_one(path)
                if "active" in elem.attrs.get("class"):
                    current = elem.text
                    break

        return current

    async def acurrent(self, page) -> None:
        """

        :type page: playwright.async_api._generated.Page
        :return:
        """
        current = ""

        if isinstance(self.root, str):
            root_elem = self.soup.select_one(self.root)

            if self.descendant == self._descendants[0]:
                current = e.text if (
                    e := root_elem.select_one(".rtsLink.rtsSelected")
                ) else ""
            elif self.descendant == self._descendants[1]:
                elems = root_elem.select(self.descendant)
                for elem in elems:
                    if "active" in elem.attrs.get("class"):
                        current = elem.text
            elif self.descendant == self._descendants[2]:
                elem = root_elem.select_one(
                    "div.button-green.fgButton.active.isActive"
                )
                current = elem.text
        else:
            for path in self.root:
                elem = self.soup.select_one(path)
                if "active" in elem.attrs.get("class"):
                    current = elem.text
                    break

        return current

    def configure(self, page, option: str) -> None:
        """

        :type page: playwright.sync_api._generated.Page
        :param option:
        """
        options = [o.lower() for o in self.options()]
        try:
            index = options.index(option)
        except ValueError as err:
            raise Exception(option) from err        # TODO: Raise custom exception

        if isinstance(self.root, str):
            root_elem = page.query_selector(self.root)
            opt_elem = root_elem.query_selector_all(self.descendant)[index]
            opt_elem.click()
        else:
            page.click(self.root[index])

    async def aconfigure(self, page, option: str) -> None:
        """

        :type page: playwright.async_api._generated.Page
        :param option:
        """
        options = [o.lower() for o in self.options()]
        try:
            index = options.index(option)
        except ValueError as err:
            raise Exception(option) from err        # TODO: Raise custom exception

        if isinstance(self.root, str):
            root_elem = await page.query_selector(self.root)
            opt_elem = (await root_elem.query_selector_all(self.descendant))[index]
            await opt_elem.click()
        else:
            await page.click(self.root[index])


class Dropdown(FilterWidget):
    """

    """
    _descendants = (
        "ul > li", "a", "option"
    )

    def __init__(
            self, soup: bs4.BeautifulSoup, root: str,
            *, dropdown: Optional[str] = None, button: Optional[str] = None
    ):
        """
        :param soup:
        :param root:
        :param dropdown:
        :param button:
        """
        self.soup = soup

        self.root = root
        self.dropdown, self.button = dropdown, button
        self.descendant = ""

        self.options = ()
        self.current, self.currents = "", ()

    def options(self) -> tuple[str]:
        """

        :return:
        """
        options = ()

        if self.dropdown:
            root_elem = self.soup.select_one(self.dropdown)
            self.descendant = self._descendants[0]
            options = [e.text for e in root_elem.select(self.descendant)]
        else:
            root_elem = self.soup.select_one(self.root)
            for desc in self._descendants:
                if elems := root_elem.select(desc):
                    options = [e.text for e in elems]
                    self.descendant = desc

        return tuple(options)

    def current(self, page) -> str:
        """

        :type page: playwright.sync_api._generated.Page
        :return:
        """
        option = ""

        root_elem = self.soup.select_one(self.root)

        if self.descendant == self._descendants[0]:
            if self.dropdown is not None:
                option = root_elem.attrs.get("value")
            else:
                options = [
                    e.text for e in root_elem.select("ul > li")
                    if "highlight" in e.attrs.get("class")
                ]
                option = options[0]
                self.currents = tuple(options)
        elif self.descendant == self._descendants[1]:
            option = root_elem.select_one("span").text
        elif self.descendant == self._descendants[2]:
            option = page.eval_on_selector(
                self.root, "el => el.value"
            )

        return option

    async def acurrent(self, page) -> str:
        """

        :type page: playwright.async_api._generated.Page
        :return:
        """
        option = ""

        root_elem = self.soup.select_one(self.root)

        if self.descendant == self._descendants[0]:
            if self.dropdown is not None:
                option = root_elem.attrs.get("value")
            else:
                options = [
                    e.text for e in root_elem.select("ul > li")
                    if "highlight" in e.attrs.get("class")
                ]
                option = options[0]
                self.currents = tuple(options)
        elif self.descendant == self._descendants[1]:
            option = root_elem.select_one("span").text
        elif self.descendant == self._descendants[2]:
            option = await page.eval_on_selector(
                self.root, "el => el.value"
            )

        return option

    def configure(self, page, option: str) -> None:
        """

        :type page: playwright.sync_api._generated.Page
        :param option:
        """
        if self.descendant in self._descendants[:3]:
            options = [o.lower() for o in self.options]
            try:
                index = options.index(option.lower())
            except ValueError as err:
                raise Exception(option) from err        # TODO: Raise custom exception

            page.click(self.root)

            root_elem = page.query_selector(self.root)
            opt_elem = root_elem.query_selector_all(self.descendant)[index]
            opt_elem.click()

            if self.button is not None:
                page.click(self.button)

        elif self.descendant == self._descendants[3]:
            for opt in self.options:
                if opt.lower() == option.lower():
                    page.select_option(self.root, label=opt)
                    return
            raise Exception(option)

    async def aconfigure(self, page, option: str) -> None:
        """

        :type page: playwright.async_api._generated.Page
        :param option:
        """
        if self.descendant in self._descendants[:3]:
            options = [o.lower() for o in self.options]
            try:
                index = options.index(option.lower())
            except ValueError as err:
                raise Exception(option) from err        # TODO: Raise custom exception

            await page.click(self.root)

            root_elem = await page.query_selector(self.root)
            opt_elem = (await root_elem.query_selector_all(self.descendant))[index]
            await opt_elem.click()

            if self.button is not None:
                await page.click(self.button)

        elif self.descendant == self._descendants[3]:
            for opt in self.options:
                if opt.lower() == option.lower():
                    await page.select_option(self.root, label=opt)
                    return
            raise Exception(option)


class Checkbox(FilterWidget):
    """

    """
    _descendants = ()

    def __init__(
            self, soup: bs4.BeautifulSoup, root: str
    ):
        """
        :param soup:
        :param root:
        """
        self.soup = soup

        self.root = root

    def options(self) -> tuple[bool, bool]:
        """

        :return:
        """
        return True, False

    def current(self, page) -> bool:
        """

        :type page: playwright.sync_api._generated.Page
        :return:
        """
        option = page.query_selector(self.root).is_checked()
        return option

    async def acurrent(self, page) -> bool:
        """

        :type page: playwright.async_api._generated.Page
        :return:
        """
        option = await (await page.query_selector(self.root)).is_checked()
        return option

    def configure(self, page, option: bool) -> None:
        """

        :type page: playwright.sync_api._generated.Page
        :param option:
        """
        if option is not self.current(page):
            page.click(self.root)

    async def aconfigure(self, page, option: bool) -> None:
        """

        :type page: playwright.async_api._generated.Page
        :param option:
        """
        if option is not (await self.acurrent(page)):
            await page.click(self.root)


class Switch(FilterWidget):
    """

    """
    _descendants = ()

    def __init__(
            self, soup: bs4.BeautifulSoup, root: str
    ):
        """
        :param soup:
        :param root:
        """
        self.soup = soup

        self.root = root

    def options(self) -> tuple[bool, bool]:
        """

        :return:
        """
        return True, False

    def current(self, page) -> bool:
        """

        :type page: playwright.sync_api._generated.Page
        :return:
        """
        root_elem = self.soup.select_one(self.root)
        option = "isActive" in root_elem.attrs.get("class")
        return option

    async def acurrent(self, page) -> bool:
        """

        :type page: playwright.async_api._generated.Page
        :return:
        """
        root_elem = self.soup.select_one(self.root)
        option = "isActive" in root_elem.attrs.get("class")
        return option

    def configure(self, page, option: bool) -> None:
        """

        :type page: playwright.sync_api._generated.Page
        :param option:
        """
        if option is not self.current(page):
            page.click(self.root)

    async def aconfigure(self, page, option: bool) -> None:
        """

        :type page: playwright.async_api._generated.Page
        :param option:
        """
        if option is not (await self.acurrent(page)):
            await page.click(self.root)


class Selectors:
    """

    """
    widget_types = {
        "selections": Selection,
        "dropdowns": Dropdown,
        "checkboxes": Checkbox,
        "switches": Switch
    }

    filter_widgets: dict[str, dict]

    def __init__(self, soup: bs4.BeautifulSoup):
        """
        :param soup:
        """
        self.soup = soup

        for wname, wclass in self.widget_types.items():
            if (d := self.filter_widgets.get(wname)) is not None:
                for attr, kwargs in d.items():
                    self.__setattr__(attr, wclass(self.soup, **kwargs))

        self.widgets = self.compile_widgets()

    def compile_widgets(self) -> dict[str, Any]:
        """

        :return:
        """
        widgets = {}
        for wtype in list(self.widget_types):
            if (wnames := self.filter_widgets.get(wtype)) is not None:
                logger.debug("Processing filter widget type: %s", wtype)
                for name in wnames:
                    wclass = self.__dict__.get(name)
                    widgets.update({name: wclass})
                    logger.debug("Processed filter widget: %s (%s)", name, wclass)

        return widgets

    def configure(self, page, **kwargs) -> None:
        """

        :type page: playwright.sync_api._generated.Page
        :param kwargs:
        """
        for wname, option in kwargs.items():
            logger.debug("Configure '%s' to '%s'", wname, option)
            widget = self.widgets.get(wname)
            widget.configure(page, option)

    async def aconfigure(self, page, **kwargs) -> None:
        """

        :type page: playwright.async_api._generated.Page
        :param kwargs:
        """
        for wname, option in kwargs.items():
            logger.debug("Configure '%s' to '%s'", wname, option)
            widget = self.widgets.get(wname)
            await widget.aconfigure(page, option)
