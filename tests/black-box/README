Blackbox tests
==============

The tests in this section are _"black box"_ tests or, put another way, tests
which test the system as a whole without concerning the code behind the module.

To run the tests, you will need to have node installed (obviously!) and have a
version of python as the SMTP client uses the built in one in python's standard
library. The tests have all been verified with python 2.5.

The tests require the testing server to be running. In the current directory:

	$ node test-server.js

Sequential tests
----------------

These tests probe the functionality of the server in a sequential manner, i.e.
each test is run one after the other. These tests cover all of the underlying
javascript code from an external perspective. To run them:

	$ python sequential.py

If you want more information, do:

	$ python sequential.py -v

The second set of tests are the concurrency tests. These verify that multiple
clients can access the server at the same time. They are quite intensive as 300
threads are spawned to simulate multiple connections. The output shows each
thread being created and then finishing up. To run: 

	$ python concurrent.py

For unit tests, see the _"unit tests"_ section.