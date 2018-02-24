# -*- coding: utf-8 -*-
# pylint: disable=too-many-arguments
"""TODO: doc module"""


from qacode.core.exceptions.control_exception import ControlException
from qacode.core.webs.controls.control_base import ControlBase
from qacode.core.webs.html_tags import HtmlTag
from qacode.core.webs.html_attrs import HtmlAttr
from qacode.core.webs.strict_rules import StrictRule
from qacode.core.webs.strict_rules import StrictType
from selenium.webdriver.common.by import By


class ControlForm(ControlBase):
    """Requirements: #63"""

    strict_tags = None
    strict_attrs = None
    strict_mode = None

    # TODO: follow instructions on #63
    def __init__(self, bot, selector='', locator=By.CSS_SELECTOR, element=None,
                 search=True, wait_for_load=False,
                 strict_rules=None,
                 strict_mode=False):
        """Base class to manage form web element through page system of qacode
            library. Apply for elements tagged with
                <label> : must validate attrs= id, class, for
                <input> : must validate attrs= id, class
                <select> + <option> : must validate attrs= id, class
                <textarea> : must validate attrs= id, class
                <datalist> + <option> : must validate attrs= id, class
                <output> : must validate attrs= id, class
            Apply also on parent elements
                <form> : must validate attrs= id, class
                <legend> : must validate attrs= id, class
                <fieldset> : must validate attrs= id, class

        Usage:
            ControlBase(bot, selector, locator)
            ControlBase(bot, element)
            ControlBase(bot, element, search=True)

        Arguments:
            bot {BotBase} -- qacode bot Class to manage control validations

        Keyword Arguments:
            selector {str} -- can be empty string to use element insteadof of
                params to load WebElement
            locator {By} -- selenium search strategy
                (default: {By.CSS_SELECTOR})
            element {WebElement} -- instanced WebElement class
                (default: {None})
            search {bool} -- [description] (default: {True})
            wait_for_load {bool} -- wait for expected condition from selenium
                before to load element (default: {False})
            strict_rules {list(StrictRule)} -- a list of strict rules to be
                applied to a element
            strict_mode {bool} -- allows to raise validation when warning
                it's received

        Raises:
            CoreEx -- param 'bot' can't be None
            ControlException -- param 'selector' can't be None, don't use if
                want to instance with 'element'
            ControlException -- param 'element' can't be None, don't use if
                want to instance with 'selector'
            ControlException -- 'element' found isn't valid to use, check
                selector and element
        """
        super(ControlForm, self).__init__(
            bot,
            selector=selector,
            locator=locator,
            element=element,
            search=search,
            wait_for_load=wait_for_load)
        if not search:
            raise NotImplementedError("Open an issue on github if raise here")
        if strict_mode is None:
            raise ControlException(
                message="bad param 'strict_mode' is None")
        self.strict_mode = strict_mode
        if not isinstance(strict_rules, (list, tuple)):
            raise ControlException(
                message="bad param 'strict_rules' not tuple or list")
        self.strict_tags = []
        self.strict_attrs = []
        self._add_rules(strict_rules, strict_mode)
        if not self.is_strict_tags() and self.strict_mode:
            raise ControlException(
                message=("Tag obtained for this element html tag not "
                "in strict_tags list"))
        if not self.is_strict_attrs() and self.strict_mode:
            raise ControlException(
                message=("Tag obtained for this element html attr"
                " not in strict_attrs list"))
    def _add_rules(self, strict_rules, strict_mode):
        """Validate strict rules for each type

        Arguments:
            strict_rules {StrictRule} -- strict_rule
            strict_mode {bool} -- if enabled, load values for
                future checks
        """
        # validate rules and add object to respective lists
        for strict_rule in strict_rules:
            if strict_rule.strict_type == StrictType.TAG:
                self.strict_tags.append(strict_rule.value)
            elif strict_rule.strict_type == StrictType.HTML_ATTR:
                self.strict_attrs.append(strict_rule.value)
            elif strict_rule.strict_type == StrictType.CSS_PROP:
                raise NotImplementedError(
                    "Open an issue on github if raise here")
            elif strict_rule.strict_type == StrictType.JS_EVENT:
                raise NotImplementedError(
                    "Open an issue on github if raise here")
            elif strict_rule.strict_type == StrictType.BEHAVIOUR:
                raise NotImplementedError(
                    "Open an issue on github if raise here")
            elif strict_rule.strict_type == StrictType.USABILITY:
                raise NotImplementedError(
                    "Open an issue on github if raise here")
            elif strict_rule.strict_type == StrictType.SEO:
                raise NotImplementedError(
                    "Open an issue on github if raise here")
            else:
                raise ControlException(
                    message="bad param 'strict_type', invalid value")
    
    def is_strict_tags(self, strict_tags=None):
        """Validate if element.tag is in list of strict_tags
        
        Keyword Arguments:
            strict_tags {[type]} -- [description] (default: {None})
        
        Returns:
            [type] -- [description]
        """
        if strict_tags is None:
            strict_tags = self.strict_tags
        for strict_tag in strict_tags:
            if self.tag == strict_tag.name:
                return True
        return False

    def is_strict_attrs(self, strict_attrs=None):
        """Validate if element.attrs is in list of strict_attrs
        
        Keyword Arguments:
            strict_attrs {[type]} -- [description] (default: {None})
        
        Returns:
            [type] -- [description]
        """
        # TODO: make functional
        attrs_search = []
        attrs_found = []
        if strict_attrs is None:
            strict_attrs = self.strict_attrs
        if strict_attrs is None:
            strict_attrs = self.strict_attrs
        for strict_attr in strict_attrs:
            attr_name = self.get_attr_name(strict_attr.value)
            attrs_search.append(attr_name)
            if attr_name:
                attrs_found.append(attr_name)
        return bool(set(attrs_search).intersection(attrs_found))
