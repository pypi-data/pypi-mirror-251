"""umami - Umami Analytics Client for Python"""

from umami import impl

__author__ = 'Michael Kennedy <michael@talkpython.fm>'
__version__ = impl.__version__
user_agent = impl.user_agent

from .impl import set_url_base  # noqa: F401
from .impl import login_async, login  # noqa: F401
from .impl import websites_async, websites  # noqa: F401
from .impl import new_event_async, new_event  # noqa: F401
from . import models

__all__ = [
    models,
    set_url_base,
    login_async, login,
    websites_async, websites,
    new_event_async, new_event,
]
