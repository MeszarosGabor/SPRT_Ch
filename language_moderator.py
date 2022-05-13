# Third party imports
import requests


MODERATOR_ENDPOINT = ""
MODERATION_TIMEOUT_SEC = 5


def moderate_sentence(sentence):
    data = {"fragment": sentence}
    try:
        resp = requests.post(MODERATOR_ENDPOINT,
                             json=data,
                             timeout=MODERATION_TIMEOUT_SEC)
    except requests.exceptions.RequestException as e:
        return {"has_foul_language": None}


def moderate_entry(entry):
    entry_has_foul = False
    for paragraph in entry["paragraphs"]:
        sentence_has_foul = moderate_sentence(paragraph).get("has_foul_language")
        if sentence_has_foul:
            entry_has_foul = True
            break
        elif sentence_has_foul is None:
            # failed to verify a sentence;
            # we can only return None/True from now on.
            entry_has_foul = None
    entry["has_foul_language"] = entry_has_foul
    return entry
