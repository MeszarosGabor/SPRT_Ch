# SPRT_Ch

## SUMMARY

The service powers a blog site backend where blog entries can be enteres and retrieved via the listed endpoints. 


## PREREQUISITES

The service was written in Python 3.8;
Run the following command from the repo root to set the PYTHONPATH env variable:
$ export PYTHONPATH=.:$PYTHONPATH

To install the necessary packages run:
$ pip3.8 install -r requirements.txt


## RUNNING THE APPLICATION

With the PYTHONPATH already set, run the following command from the repo root to launch the main application; note that you need to configure the following parameters on the command line: host of the application, port the application is running on, as well as the enpoint of the 
content moderator API.

$ python3.8 app.py --host localhost --port 6006 --moderator_
endpoint  http://localhost:5555/

## ENDPOINTS

[POST] <host>/posts/: enters and persists the blog entry, keyed by the instertion timestamp (int), with the corresponding body as JSON value. It supports JSON format only (see example below):

$ curl -X POST -H 'Content-Type: application/json' -d '{"title":"foo","paragraphs":["par1","par2"]}'  "http://localhost:6006/posts/"

[GET] <host>/posts/: return the dictionary content of the so far registered entries.


## TESTING

Due to the scope of the project, limited testing is provided.
Unit tests of the main moderator functionality are available under tests/test_unit_language_moderator.py and can be executed from repo root as follows:
$ pytest tests/test_unit_language_moderator.py

In order to verify end-to-end functionality, the tests/ folder offers a dummy moderator service implementation which identifies 
foul sentences based on exact string matches of trigger words.

Manual testing with the above tools can be carried out as follows:
1. Launch the moderator (hardcoded host/port)
$ python3.8 tests/run_test_moderator.py
2. Launch the main service
$ python3.8 app.py --host localhost --port 6006 --moderator_
endpoint  http://localhost:5555/
3. Use the above curl requests to enter blog entries (POST) and verify their population (GET).


## PROPOSED ADDITIONAL WORK
- data persistence in Redis/ MySQL with JSON fields.
- GET endpoint with title-search and regex match
- Additional unit test coverage
- Automated full functional testing with app context managers

