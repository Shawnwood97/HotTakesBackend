from flask import request, Response
import dbh
import json
import traceback

# ! Less comments here since this is basically a copy of tweets.py
# ? maybe refactor later!


def list_comments():
  # set user_id using args.get so it's not mandatory.
  try:
    tweet_id = int(request.args['tweetId'])
  except ValueError:
    return Response("Error: tweetId is NaN", mimetype="text/plain", status=422)
  except KeyError:
    traceback.print_exc()
    return Response("Error: tweetId cannot be empty", mimetype="text/plain", status=422)
  except:
    traceback.print_exc()
    return Response("Unknown error with tweetId", mimetype="text/plain", status=400)

  # Base for SELECT query
  sql = "SELECT c.id AS commentId, c.take_id AS tweetId, c.user_id AS userId, u.username, c.content, c.created_at AS createdAt FROM comments c INNER JOIN users u ON c.user_id = u.id WHERE c.take_id = ?"

  # this try ensures we can error catch in a decent way
  try:
    tweet_id = dbh.run_query(
        "SELECT t.id from takes t WHERE t.id = ?", [tweet_id, ])[0]['id']
  except IndexError:
    return Response("Not a valid tweetId", mimetype="text/plain", status=400)
  except:
    return Response("Unknown error with tweetId", mimetype="text/plain", status=400)

  if(type(tweet_id) is str):
    return dbh.exc_handler(tweet_id)

  comments = dbh.run_query(sql, [tweet_id, ])

  if(type(comments) is str):
    return dbh.exc_handler(comments)

  # I think all errors are caught by this point.
  comments_json = json.dumps(comments, default=str)
  return Response(comments_json, mimetype='application/json', status=200)


def create_comment():
  try:
    # Get all required inputs.
    login_token = request.json['loginToken']
    tweet_id = int(request.json['tweetId'])
    content = request.json['content']
  except ValueError:
    traceback.print_exc()
    return Response("Error: One or more of the inputs is invalid!", mimetype="text/plain", status=422)
  except KeyError:
    traceback.print_exc()
    return Response("Error: One or more required fields are empty!", mimetype="text/plain", status=422)
  except:
    traceback.print_exc()
    return Response("Error: Unknown error with an input!", mimetype="text/plain", status=400)

  # query to get user id using the loginToken
  user_sql = "SELECT user_id FROM `session` WHERE token = ?"

  # set user_id, get errors for login token
  try:
    user_id = dbh.run_query(user_sql, [login_token, ])[0]['user_id']
  # not sure if this is right, but when testing for errors, IndexError only ever came up when there was a wrong loginToken used, So I used that as the error here!
  except IndexError:
    traceback.print_exc()
    return Response("Error: Login Token invalid, please relog", mimetype="text/plain", status=404)
  except:
    traceback.print_exc()
    return Response("Error: Unkown Error", mimetype="text/plain", status=400)

  if(type(user_id) is str):
    return dbh.exc_handler(user_id)

  # verify tweet id against the DB
  try:
    tweet_id = dbh.run_query(
        "SELECT t.id from takes t WHERE t.id = ?", [tweet_id, ])[0]['id']
  except IndexError:
    return Response("Invalid tweetId", mimetype="text/plain", status=400)
  except:
    return Response("Unknown error with tweetId", mimetype="text/plain", status=400)

  if(type(tweet_id) is str):
    return dbh.exc_handler(tweet_id)

  # Insert Query
  sql = "INSERT INTO comments (user_id, take_id, content) VALUES (?,?,?)"
  # starting point for params to pass to run_query helper function
  # includes content because content is mandatory.
  params = [user_id, tweet_id, content]

  new_comment_id = dbh.run_query(sql, params)

  if(type(new_comment_id) is str):
    return dbh.exc_handler(new_comment_id)

  if(new_comment_id != None):
    new_comment_info = dbh.run_query(
        "SELECT c.id AS commentId, c.take_id AS tweetId, c.user_id AS userId, u.username, c.content, c.created_at AS createdAt FROM comments c INNER JOIN users u ON c.user_id = u.id WHERE c.id = ?", [new_comment_id, ])

    if(type(new_comment_info) is str):
      return dbh.exc_handler(new_comment_info)

    new_comment_json = json.dumps(new_comment_info, default=str)
    return Response(new_comment_json, mimetype="application/json", status=201)
  else:
    return Response("Failed to create tweet", mimetype="text/plain", status=400)


def update_comment():
  try:
    # Get required inputs
    login_token = request.json['loginToken']
    comment_id = int(request.json['commentId'])
    content = request.json['content']
  except ValueError:
    traceback.print_exc()
    return Response("Error: One or more of the inputs is invalid!", mimetype="text/plain", status=422)
  except KeyError:
    traceback.print_exc()
    return Response("Error: One or more required fields are empty!", mimetype="text/plain", status=422)
  except:
    traceback.print_exc()
    return Response("Error: Unknown error with an input!", mimetype="text/plain", status=400)

  # update Query, includes setting the was_edited to 1(true) and edit_time to the current time(even though I probably won't use it until I rebuild!)
  sql = "UPDATE comments c INNER JOIN `session` s ON c.user_id = s.user_id SET c.content = ?, c.was_edited = 1, c.edit_time = NOW() WHERE s.token = ? AND c.id = ?"

  try:
    comment_id = dbh.run_query(
        "SELECT c.id from comments c WHERE c.id = ?", [comment_id, ])[0]['id']
  except IndexError:
    return Response("Invalid tweetId", mimetype="text/plain", status=400)
  except:
    return Response("Unknown error with tweetId", mimetype="text/plain", status=400)

  if(type(comment_id) is str):
    return dbh.exc_handler(comment_id)

  # run the update, update variable will equal the rowcount. Should be 1 if successful!
  updated_rows = dbh.run_query(
      sql, [content, login_token, comment_id])

  if(type(updated_rows) is str):
    return dbh.exc_handler(updated_rows)

  # only happens if update was successful.
  # on update use == 1 instead of != 0
  if(updated_rows == 1):
    updated_comment_info = dbh.run_query(
        "SELECT c.id AS commentId, c.take_id AS tweetId, c.user_id AS userId, u.username, c.content, c.created_at AS createdAt FROM comments c INNER JOIN users u ON c.user_id = u.id WHERE c.id = ?", [comment_id, ])
  else:
    traceback.print_exc()
    return Response("Error: Invalid tweetId and loginToken combination", mimetype="text/plain", status=403)

  # extra error handling, maybe not needed, butttt
  if(type(updated_comment_info) is str):
    return dbh.exc_handler(updated_comment_info)

  # even more error handling! and return of data
  if(len(updated_comment_info) == 1):
    updated_comment_json = json.dumps(updated_comment_info, default=str)
    return Response(updated_comment_json, mimetype="application/json", status=200)
  else:
    traceback.print_exc()
    return Response("Failed to update", mimetype="text/plain", status=400)


def delete_comment():
  try:
    login_token = request.json['loginToken']
    comment_id = int(request.json['commentId'])

  except ValueError:
    traceback.print_exc()
    return Response("Error: One or more of the inputs is invalid!", mimetype="text/plain", status=422)
  except KeyError:
    traceback.print_exc()
    return Response("Error: One or more required fields are empty!", mimetype="text/plain", status=422)
  except:
    traceback.print_exc()
    return Response("Error: Unknown error with an input!", mimetype="text/plain", status=400)

  try:
    comment_id = dbh.run_query(
        "SELECT c.id from comments c WHERE c.id = ?", [comment_id, ])[0]['id']
  except IndexError:
    return Response("Invalid commentId", mimetype="text/plain", status=400)
  except:
    return Response("Unknown error with commentId", mimetype="text/plain", status=400)

  if(type(comment_id) is str):
    return dbh.exc_handler(comment_id)

  try:
    login_token = dbh.run_query(
        "SELECT s.token from `session` s WHERE s.token = ?", [login_token, ])[0]['token']
  except IndexError:
    return Response("Invalid loginToken", mimetype="text/plain", status=400)
  except:
    return Response("Unknown error with loginToken", mimetype="text/plain", status=400)

  if(type(list(login_token)) is str):
    return dbh.exc_handler(login_token)

  deleted_comment = dbh.run_query(
      "DELETE c FROM comments c INNER JOIN `session` s ON c.user_id = s.user_id WHERE c.id = ? AND s.token = ?", [comment_id, login_token])

  if(type(deleted_comment) is str):
    return dbh.exc_handler(deleted_comment)

  if(deleted_comment == 1):
    return Response("Comment Deleted Successfully!", mimetype='text/plain', status=201)
  else:
    traceback.print_exc()
    return Response("Error: commentId or loginToken invalid, Please relog and try again", mimetype='text/plain', status=400)
