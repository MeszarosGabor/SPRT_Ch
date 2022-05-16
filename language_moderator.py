"""
Language moderator utilily module; supports the utilization of the
provided 3rd party moderator API on sentence and entry levels.
"""

from gevent import monkey
monkey.patch_all()

# Standard library imports
import logging

# Third party imports
import gevent
import requests


logger = logging.getLogger()

# TODO: could be CLI parameter.
MODERATION_TIMEOUT_SEC = 5


def moderate_sentence(sentence, moderator_endpoint):
    """
    Calls the provided API and returns if a sentence contains foul words.
    """
    data = {"fragment": sentence}
    logger.debug(f"Received fragment {sentence}")
    try:
        resp = requests.post(moderator_endpoint,
                             json=data,
                             timeout=MODERATION_TIMEOUT_SEC)
        if resp.status_code != 200:
            return  {"has_foul_language": None}
        return resp
    except requests.exceptions.RequestException as e:
        return {"has_foul_language": None}


def moderate_entry(entry, moderator_endpoint):
    """
    Calls the provided API and returns if a blog entry contains foul words.
    In case no foul sentence is found but not all sentences received
    confirmation, the entry will be recorded as 'None' (= unknown).

    NOTE: paragraphs are processed through parallel API calls for
          performance reasons.
    """
    logger.debug(f"RECEIVED ENTRY: {entry}")
    entry_has_foul = False
    moderator_greenlets = []
    for paragraph in entry["paragraphs"]:
        moderator_greenlets.append(gevent.spawn(moderate_sentence, paragraph, moderator_endpoint))
    gevent.joinall(moderator_greenlets)
    responses = [r.value.json().get("has_foul_language") for r in moderator_greenlets]
    logger.debug(f"RESPONSES: {responses}")
    if True in responses:
        entry_has_foul = True
    elif None in responses:
        entry_has_foul = None
    entry["has_foul_language"] = entry_has_foul
    return entry
