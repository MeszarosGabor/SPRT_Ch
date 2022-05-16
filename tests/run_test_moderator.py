""" Minimalist moderator service runner (with hardcoded host&port). """

from tests.dummy_testing_moderator import TestModeratorRunner


tmr = TestModeratorRunner('localhost', 5555, 'foo')
tmr.run_service()
