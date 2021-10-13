
**Depreciation Note:   
Please note, this repo was part of an implementation study and is not longer maintained.
Please do not use for production.** 

---

# sandbox-notification

This is the microservice that sends out notifications to the recipients such as Data steward, Data requester or
Data submitter. The notifications can be triggered by underlying events such as requests, submission or
Data processing. The notification calls are almost always Asynchronous calls.

First you need to provide the environment variables for the SMTP server configuration. You must do this by creating a `.env` file in `.devcontainer` with the following content (replacing the placeholder brackets with the actual values):

```sandbox-notification_smtpserv=[SMTP server]
sandbox-notification_smtpport=[SMTP port]
sandbox-notification_smtpusername=[SMTP username]
sandbox-notification_smtppassword=[SMTP password]
```

To run the application

    cd sandbox-notification
    docker build -t sandbox-notification .
    docker run -d -p 8000:8000 sandbox-notification

To run unit test

    cd test
    pytest filename.py

alternatively to run all tests at once

    pytest *.py
