# Elite Lab 5: Forms, APIs, and Ajax

## Intro
In this lab, we will be building our first chatrooms. We have provided a template files to get you started. By the end, you should be able to have a fully functioning group chatroom working.

I've prepped some quick reference links down below to help you out:

* https://www.python.org/doc/
* https://www.tutorialspoint.com/python/python_functions.htm
* https://realpython.com/python-for-loop/
* https://flask.palletsprojects.com/en/1.1.x/quickstart/
* https://flask.palletsprojects.com/en/1.1.x/quickstart/#routing

* https://realpython.com/instance-class-and-static-methods-demystified/

* https://flask-wtf.readthedocs.io/en/stable/quickstart.html

* https://api.jquery.com/jquery.ajax/


Remember to always use Google and StackOverflow as a resource if you are not sure how to implement something. Feel free to reach out to me as well.


## Objective
### Task
Your goal is to build the routing and controllers to support our chatroom client.

Lab is complete when you are able to succesfully:
* Enter a chatroom with a username
* Send messages
* Receive messages

If you look closely into the client JS file, it will require these APIs to work:
* delete a message (`DELETE /messages/<message_id>`)
* create message (`POST /messages/`)
* get last messages in a chat (`GET /chat/<chat_id>/last?count=<number of message>`)
* get the messages newer than ref_id (`GET /chat/<chat_id>/updates?ref_id=<id>`)

### Context
We have provided you with starter and demo code. You do NOT need to change anything in the `app/models.py` file. You also do not need to change anything in the `static/` and `templates/` directory (But take a look through them, especially `chat.js`, knowing how the client works will be valuable).

All of your work should go into `app/controllers.py` file. 

We have also provided `scripts/util.py` that you can run in the command line. This script can help insert test messages into your database and also delete all messages (so you can start fresh if need be). This is to help you out, but not needed for completion.


## Set Up
* Fork and clone the repository to your local dev environment

* Activate your virtual environment
```
python3 -m venv venv
source venv/bin/activate
```

* Install the dependencies to your virtual environment
```
pip3 install -r requirements.txt
```

* Start up your SQLite database with:
```
python3 -m flask db init
python3 -m flask db migrate -m "my first migration"
python3 -m flask db upgrade
```

* Spin up the local web server with:
```
python3 -m flask run
```


## Lab Steps
* Look through the `app/static/js/chat.js` file to get an idea how these APIs are being called.

* Look through `app/models.py` file and notice the new manager functions that are provided
  * get_last_messages_in_chat(chat_id, num_messages)
  * get_message_updates_in_chat(chat_id, last_id)

* (Optional) Run the `scripts/util.py` script to seed your database with test messages

* Implement the API for `GET /chat/<chat_id>/last?count=<number of message>`

* Enter the chatroom and validate that you can load messages into the chatbox

* Implement the create API (use last week's lab answer)

* Validate success by sending a message in the chatroom

* Implement the API for `GET /chat/<chat_id>/updates?ref_id=<id>`

* Validate success by opening a new chatroom and sending messages to yourself


## Lab Advice
* Feel free to copy paste last week's lab code into the controller (it should work the same)

* Get an idea for how the client works:
  * Before entering the chatroom, you must submit a username (this will be stored in the backend)
  * The backend will give you a token that can be used to find your username
  * When loading the page for the first time, the client will try to figure out which user you are (through your token)
  * The page will then load the most recent messages
  * At a regular interval, the page will also ask the backend if there are new messages since the last time it checked
    * It does this through providing the last message ID it had received. The backend finds that message for the message ID and then returns any messages with a more recent timestamp.
  * Entering a message in the chatroom will create a new message in the backend first. Then the client will poll for new messages using the step above.

* You do not need to modify `models.py`. I have already provided all the functions needed to complete the lab. Instead, use it as a reference for what you can retrieve from the database.

* You should not need to modify the schema, but if your database goes out of sync with your schema, you can run these commands:
```
python3 -m flask db stamp head
python3 -m flask db migrate
python3 -m flask db upgrade
```
