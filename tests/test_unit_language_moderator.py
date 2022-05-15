from copy import copy

import pytest
import responses

from language_moderator import moderate_entry, moderate_sentence, MODERATOR_ENDPOINT

@pytest.fixture                                                                    
def mocked_responses():                                                            
    with responses.RequestsMock() as rsps:                                         
        yield rsps 

@pytest.fixture
def entry():
    return {
        "title": "Test Title",
        "paragraphs": ["par1", "par2", "par3"]
    }


@responses.activate
@pytest.mark.parametrize("api_resp", [True, False,  None])
def test_moderate_sentence(api_resp, mocked_responses):
    responses.add(responses.POST, MODERATOR_ENDPOINT,
                  json={"has_foul_language": api_resp}, status=200)
    moderated = moderate_sentence('All men must die')

    assert moderated.json().get("has_foul_language") == api_resp


@responses.activate
@pytest.mark.parametrize("api_resp", [True, False,  None])
def test_moderate_entry_all_same(entry, api_resp, mocked_responses):
    moderated_entry = copy(entry)
    moderated_entry["has_foul_language"] = api_resp
    responses.add(responses.POST, MODERATOR_ENDPOINT,
                  json={"has_foul_language": api_resp}, status=200)
    moderated = moderate_entry(entry)
    assert moderated.get("has_foul_language") == api_resp

