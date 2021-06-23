from flask import Flask, request, Response
import dbh
import json
import traceback
import sys
import mariadb
import users
import login
import follows
import followers
import tweets

app = Flask(__name__)


# ? --------------------------------------------------------
# ? --------------------- /API/USERS -----------------------
# ? --------------------------------------------------------


@app.get('/api/users')
def call_list_users():
  return users.list_users()


@app.post('/api/users')
def call_create_user():
  return users.create_user()


@app.patch('/api/users')
def call_update_user():
  return users.update_user()


@app.delete('/api/users')
def call_delete_user():
  return users.delete_user()

# * --------------------------------------------------------
# * -------------------- /API/LOGIN ------------------------
# * --------------------------------------------------------


@app.post('/api/login')
def call_login_user():
  return login.login_user()


@app.delete('/api/login')
def call_logout_user():
  return login.logout_user()

# ! --------------------------------------------------------
# ! -------------------- /API/FOLLOWS ----------------------
# ! --------------------------------------------------------


@app.get('/api/follows')
def call_list_follows():
  return follows.list_follows()


@app.post('/api/follows')
def call_new_follow():
  return follows.new_follow()


@app.delete('/api/follows')
def call_remove_follow():
  return follows.remove_follow()


# ? --------------------------------------------------------
# ? -------------------- /API/FOLLOWERS --------------------
# ? --------------------------------------------------------

@app.get('/api/followers')
def call_list_followers():
  return followers.list_followers()


# * --------------------------------------------------------
# * ------------------- /API/TWEETS ------------------------
# * --------------------------------------------------------

@app.get('/api/tweets')
def call_list_tweets():
  return tweets.list_tweets()


@app.post('/api/tweets')
def call_create_tweet():
  return tweets.create_tweet()


@app.patch('/api/tweets')
def call_update_tweet():
  return tweets.update_tweet()


@app.delete('/api/tweets')
def call_delete_tweet():
  return tweets.delete_tweet()


if(len(sys.argv) > 1):
  mode = sys.argv[1]
else:
  print("No mode argument, please pass a mode argument when invoking the file!")
  exit()

if(mode == "prod"):
  import bjoern  # type: ignore
  bjoern.run(app, "0.0.0.0", 5015)
elif(mode == "test"):
  from flask_cors import CORS
  CORS(app)
  app.run(debug=True)
else:
  print("Invalid mode, please select either 'prod' or 'test'")
  exit()
