from gevent import monkey
monkey.patch_all()

# Third party imports
import gevent
import requests


DUMMY_MODERATOR_ENDPOINT = 'http://testingtestingtesting.com/'  # dummy endpoint
MODERATION_TIMEOUT_SEC = 5


def moderate_sentence(sentence, moderator_endpoint=DUMMY_MODERATOR_ENDPOINT):
    data = {"fragment": sentence}

    try:
        resp = requests.post(moderator_endpoint,
                             json=data,
                             timeout=MODERATION_TIMEOUT_SEC)
        if resp.status_code != 200:
            return  {"has_foul_language": None}
        return resp
    except requests.exceptions.RequestException as e:
        return {"has_foul_language": None}


def moderate_entry(entry, moderator_endpoint=DUMMY_MODERATOR_ENDPOINT):
    print(f"RECEIVED ENTRY: {entry}")
    entry_has_foul = False
    moderator_greenlets = []
    for paragraph in entry["paragraphs"]:
        moderator_greenlets.append(gevent.spawn(moderate_sentence, paragraph, moderator_endpoint))
    gevent.joinall(moderator_greenlets)
    responses = [r.value.json().get("has_foul_language") for r in moderator_greenlets]
    print(f"RESPONSES: {responses}")
    if True in responses:
        entry_has_foul = True
    elif None in responses:
        entry_has_foul = None
    entry["has_foul_language"] = entry_has_foul
    return entry
