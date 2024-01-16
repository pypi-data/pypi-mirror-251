import logging
import re
from html import unescape

MENTION_REGEX = re.compile("^<@(|[WU].+?)>(.*)")
LINK_REGEX = re.compile(r"<(http.*?)(\|.*?)?>", re.DOTALL)

logger = logging.getLogger(__name__)


def parse_direct_mention(message_text):
    """
    Finds a direct mention (a mention that is at the beginning) in message text
    and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = MENTION_REGEX.search(message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)


# Parse URLs
# https://api.slack.com/docs/message-formatting#linking_to_urls
def parse_links(message_text):
    for m in LINK_REGEX.findall(message_text):
        logger.debug("Found match %s", m)
        # Links in text sometimes have their enti
        yield unescape(m[0])


def is_bot(message) -> bool:
    return all(
        (
            "bot_id" in message,
            "bot_profile" in message,
            "user" in message,
        )
    )


def is_workflow(message) -> bool:
    return all(
        (
            message.get("subtype", "") == "bot_message",
            "bot_id" in message,
            "user" not in message,
        )
    )
