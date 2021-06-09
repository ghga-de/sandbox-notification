# sandbox-notification

This is the microservice that sends out notifications to the recipients such as Data steward, Data requester or 
Data submitter. The notifications can be triggered by underlying events such as requests, submission or 
Data processing. The notification calls are almost always Asynchronous calls.

To run the application

    cd sandbox-notification
    docker build -t sandbox-notification . 
    docker run -d -p 5000:5000 sandbox-notification

To run unit test

    cd test
    pytest filename.py

alternatively to run all tests at once

    pytest *.py
