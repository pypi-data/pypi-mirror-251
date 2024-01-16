import logging
from functools import wraps

from slack_sdk.errors import SlackApiError

from dsbot import util
from dsbot.conf import settings

from .exceptions import CommandError, channel_errors

logger = logging.getLogger(__name__)


def ignore_users(ignore_user_list=settings.SLACK_IGNORE_USERS):
    def _outer(func):
        @wraps(func)
        def _inner(*args, message, **kwargs):
            if message.get("user") in ignore_user_list:
                logger.debug("%s ignores user %s", func, message["user"])
            else:
                return func(*args, message=message, **kwargs)

        return _inner

    return _outer


def ignore_bots(func):
    @wraps(func)
    def _inner(*args, message, **kwargs):
        if util.is_bot(message):
            logger.debug("%s skips bot messages %s", func, message["user"])
        else:
            return func(*args, message=message, **kwargs)

    return _inner


def ignore_subtype(func):
    @wraps(func)
    def __inner(*args, message, **kwargs):
        if subtype := message.get("subtype", None):
            logger.debug("%s skips subtype message %s", func, subtype)
        else:
            return func(*args, message=message, **kwargs)

    return __inner


def api_error(func):
    @wraps(func)
    def __inner(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except SlackApiError as e:
            if e.response.data["error"] in channel_errors:
                raise channel_errors[e.response.data["error"]](response=e.response, **kwargs) from e
            raise e

    return __inner


def command(func):
    @wraps(func)
    def _inner(*args, client, message, **kwargs):
        try:
            func(*args, client=client, message=message, **kwargs)
        except CommandError as e:
            logger.warning("Command Error")
            return client.web_client.chat_postEphemeral(
                as_user=True,
                channel=message["channel"],
                user=message["user"],
                attachments=[
                    {
                        "color": "warning",
                        "title": "Command Error",
                        "text": str(e),
                    }
                ],
            )
        except Exception as e:
            logger.exception("Unknown Error")
            return client.web_client.chat_postEphemeral(
                as_user=True,
                channel=message["channel"],
                user=message["user"],
                attachments=[
                    {
                        "color": "danger",
                        "title": "Unknown Error",
                        "text": str(e),
                    }
                ],
            )

    return _inner
