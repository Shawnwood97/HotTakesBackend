from flask import Flask, request, Response
import dbh
import json
import traceback
import sys
import users
import login
import follows
import followers
import tweets
import tweetlikes
import comments
import commentlikes
import messages

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


# ! --------------------------------------------------------
# ! ----------------- /API/TWEET-LIKES ---------------------
# ! --------------------------------------------------------

@app.get('/api/tweet-likes')
def call_list_tweet_likes():
  return tweetlikes.list_tweet_likes()


@app.post('/api/tweet-likes')
def call_add_tweet_like():
  return tweetlikes.add_tweet_like()


@app.delete('/api/tweet-likes')
def call_remove_tweet_like():
  return tweetlikes.remove_tweet_like()


# ? --------------------------------------------------------
# ? -------------------- /API/COMMENTS ---------------------
# ? --------------------------------------------------------

@app.get('/api/comments')
def call_list_comments():
  return comments.list_comments()


@app.post('/api/comments')
def call_create_comment():
  return comments.create_comment()


@app.patch('/api/comments')
def call_update_comment():
  return comments.update_comment()


@app.delete('/api/comments')
def call_delete_comment():
  return comments.delete_comment()

# * --------------------------------------------------------
# * ---------------- /API/COMMENT-LIKES --------------------
# * --------------------------------------------------------


@app.get('/api/comment-likes')
def call_list_comment_likes():
  return commentlikes.list_comment_likes()


@app.post('/api/comment-likes')
def call_add_comment_like():
  return commentlikes.add_comment_like()


@app.delete('/api/comment-likes')
def call_remove_comment_like():
  return commentlikes.remove_comment_like()

# ! --------------------------------------------------------
# ! ------------------ /API/MESSAGES -----------------------
# ! --------------------------------------------------------


@app.get('/api/messages')
def call_list_messages():
  return messages.list_messages()


@app.post('/api/messages')
def call_send_message():
  return messages.send_message()


@app.delete('/api/messages')
def call_delete_message():
  return messages.delete_message()


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
