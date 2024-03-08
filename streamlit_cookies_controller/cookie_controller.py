# Author    : Nathan Chen
# Date      : 08-Mar-2024


import os
from datetime import datetime, timedelta
import streamlit as st
import streamlit.components.v1 as components
from typing import Literal, Optional, Union, Any, Dict


_RELEASE = True


if not _RELEASE:
    _cookie_controller = components.declare_component("cookie_controller", url="http://localhost:3001")
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _cookie_controller = components.declare_component("cookie_controller", path=build_dir)


class CookieController:
    """ Hook cookies get/set on Express for server-rendering
    """
    __key: str
    __cookies: Dict[str, Any]

    def __init__(self, key: str = 'cookies'):
        """ Initialize cookie controller

        ### Arguments
        key: str
            the session state key name to store the cookies
        """
        self.__key = key
        if key not in st.session_state:
            self.__cookies: Dict[str, Any] = _cookie_controller(method='getAll', key=key, default={})
        else:
            self.__cookies: Dict[str, Any] = st.session_state[key]

            # Require this as the key tie to the controller is remove from session sate when the controller widget is removed on the subsequence iteration
            st.session_state[key] = self.__cookies

    def refresh(self):
        """ Refresh the cookie cache located in streamlit session state with the actual browser cache
        """
        self.__cookies: Dict[str, Any] = _cookie_controller(method='getAll', key=self.__key, default={})

    def getAll(self):
        """ Get all cookie for the domain

        ### Returns : dict[str, any]
        All client cookie for the site in dictionary
        """
        return self.__cookies

    def get(self, name: str):
        """ Gets a cookie with the name

        ### Arguments
        name: str
            Name of the cookie

        ### Returns
            The value of the cookie with the given name
        """
        if name not in self.__cookies:
            return None
        return self.__cookies[name]
    

    def __getOptions(self,
            path: str = '/',
            expires: Optional[datetime] = None,
            max_age: Optional[float] = None,
            domain: Optional[str] = None,
            secure: Optional[bool] = None,
            same_site: Union[bool, None, Literal['lax', 'strict']] = 'strict',
            partitioned: Optional[bool] = None):
        if expires is None:
            expires = datetime.now() + timedelta(days=1)
        options = {
            "path": path,
            "expires": expires.isoformat(),
            "maxAge": max_age,
            "domain": domain,
            "secure": secure,
            "sameSite": same_site,
            "partitioned": partitioned
        }
        # Remove None from options
        return {k: v for k, v in options.items() if v is not None}

    def set(self,
            name: str,
            value: Any,
            path: str = '/',
            expires: Optional[datetime] = None,
            max_age: Optional[float] = None,
            domain: Optional[str] = None,
            secure: Optional[bool] = None,
            same_site: Union[bool, None, Literal['lax', 'strict']] = 'strict',
            partitioned: Optional[bool] = None):
        """ Sets given `value` to cookie with given name

        ### Arguments
        name: str
            Name of the cookie
        value: any
            Value of the cookie
        path: str
            Cookie path, use '/' as the path if you want your cookie to be accessible on all pages
        expires: datetime | None
            Absolute expiration date for the cookie. If `None` or default, it will be a day from now.
        max_age: float | None
            Relative maximum age of the cookie from the client receives it in seconds.
        domain: str | None
            Domain for the cookie (sub.domain.com or .allsubdomains.com)
        secure: bool | None
            Is only accessible through HTTPS?
        sameSite: bool | None | 'strict' | 'lax'
            Strict or Lax enforcement
        partitioned: bool
            Indicates that the cookie should be stored using partitioned storage
        """

        if name is None or name == "": return
        options = self.__getOptions(path, expires, max_age, domain, secure, same_site, partitioned)

        # set to cookie in the client browser
        _cookie_controller(method='set', name=name, value=value, options=options)

        # set to streamlit environment copy
        self.__cookies[name] = value

    def remove(self, name: str,
            path: str = '/',
            domain: Optional[str] = None,
            secure: Optional[bool] = None,
            same_site: Union[bool, None, Literal['lax', 'strict']] = 'strict',
            partitioned: Optional[bool] = None):
        """ Remove the cookie with the given name

        ### Arguments
        name: str
            Name of the cookie
        path: str
            Cookie path, use '/' as the path if you want your cookie to be accessible on all pages
        domain: str | None
            Domain for the cookie (sub.domain.com or .allsubdomains.com)
        secure: bool | None
            Is only accessible through HTTPS?
        sameSite: bool | None | 'strict' | 'lax'
            Strict or Lax enforcement
        partitioned: bool
            Indicates that the cookie should be stored using partitioned storage
        """
        if name is None or name == "": return
        options = self.__getOptions(path, None, None, domain, secure, same_site, partitioned)

        _cookie_controller(method='remove', name=name, options=options)
        self.__cookies.pop(name)
