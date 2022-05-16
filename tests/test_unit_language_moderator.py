# Standard library imports
from copy import copy

# Third party imports
import pytest
import responses

from language_moderator import moderate_entry, moderate_sentence


DUMMY_MODERATOR_ENDPOINT = 'http://testingtestingtesting.com/'


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
    responses.add(responses.POST, DUMMY_MODERATOR_ENDPOINT,
                  json={"has_foul_language": api_resp}, status=200)
    moderated = moderate_sentence('All men must die', DUMMY_MODERATOR_ENDPOINT)

    assert moderated.json().get("has_foul_language") == api_resp


@responses.activate
@pytest.mark.parametrize("api_resp", [True, False,  None])
def test_moderate_entry_all_same(entry, api_resp, mocked_responses):
    moderated_entry = copy(entry)
    moderated_entry["has_foul_language"] = api_resp
    responses.add(responses.POST, DUMMY_MODERATOR_ENDPOINT,
                  json={"has_foul_language": api_resp}, status=200)
    moderated = moderate_entry(entry, DUMMY_MODERATOR_ENDPOINT)
    assert moderated.get("has_foul_language") == api_resp
