from flask import request, Response
import dbh
import json
import traceback

# ! Less comments here since this is basically a copy of tweets.py
# ? maybe refactor later!


def list_comments():
  try:
    tweet_id = int(request.args['tweetId'])
    if(tweet_id <= 0):
      return Response("Invalid tweetId", mimetype="text/plain", status=422)
  except ValueError:
    return Response("Error: tweetId is NaN", mimetype="text/plain", status=422)
  except KeyError:
    traceback.print_exc()
    return Response("Error: tweetId cannot be empty", mimetype="text/plain", status=422)
  except:
    traceback.print_exc()
    return Response("Unknown error with tweetId", mimetype="text/plain", status=400)

  # Base for SELECT query
  sql = "SELECT c.id AS commentId, c.take_id AS tweetId, c.user_id AS userId, u.username, u.profile_pic_path AS userImageUrl, c.content, c.created_at AS createdAt FROM comments c INNER JOIN users u ON c.user_id = u.id WHERE c.take_id = ?"

  comments = dbh.run_query(sql, [tweet_id, ])

  if(comments['success'] == False):
    return comments['error']

  # I think all errors are caught by this point.
  comments_json = json.dumps(comments['data'], default=str)
  return Response(comments_json, mimetype='application/json', status=200)


def create_comment():
  try:
    # Get all required inputs.
    login_token = request.json['loginToken']
    tweet_id = int(request.json['tweetId'])
    content = request.json['content']
    if(tweet_id <= 0):
      return Response("Invalid tweetId", mimetype="text/plain", status=422)
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

  # set user_id, get errors for login token, this makes sense to me since I do need this later, so verification here seems ok.
  results = dbh.run_query(user_sql, [login_token, ])

  if(results['success'] == False):
    return results['error']

  try:
    user_id = results['data'][0]['user_id']
  except:
    traceback.print_exc()
    return Response("Authorization Error", mimetype="text/plain", status=403)

  # Insert Query
  sql = "INSERT INTO comments (user_id, take_id, content) VALUES (?,?,?)"
  # starting point for params to pass to run_query helper function
  # includes content because content is mandatory.
  params = [user_id, tweet_id, content]

  result = dbh.run_query(sql, params)

  if(result['success'] == False):
    return result['error']

  new_comment_id = result['data']

  if(new_comment_id != None):
    new_comment_info = dbh.run_query(
        "SELECT c.id AS commentId, c.take_id AS tweetId, c.user_id AS userId, u.username, u.profile_pic_path AS userImageUrl, c.content, c.created_at AS createdAt FROM comments c INNER JOIN users u ON c.user_id = u.id WHERE c.id = ?", [new_comment_id, ])

    if(new_comment_info['success'] == False):
      return new_comment_info['error']

    new_comment_json = json.dumps(new_comment_info['data'][0], default=str)
    return Response(new_comment_json, mimetype="application/json", status=201)
  else:
    return Response("Error getting comment after insert!", mimetype="text/plain", status=404)


def update_comment():
  try:
    # Get required inputs
    login_token = request.json['loginToken']
    comment_id = int(request.json['commentId'])
    content = request.json['content']
    if(comment_id <= 0):
      return Response("Invalid commentId", mimetype="text/plain", status=422)
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

  # run the update, update variable will equal the rowcount. Should be 1 if successful!
  result = dbh.run_query(
      sql, [content, login_token, comment_id])

  if(result['success'] == False):
    return result['error']

  # only happens if update was successful.
  # on update use == 1 instead of != 0
  if(result['data'] == 1):
    updated_comment_info = dbh.run_query(
        "SELECT c.id AS commentId, c.take_id AS tweetId, c.user_id AS userId, u.username, c.content, c.created_at AS createdAt FROM comments c INNER JOIN users u ON c.user_id = u.id WHERE c.id = ?", [comment_id, ])
  else:
    traceback.print_exc()
    return Response("Authorization Error", mimetype="text/plain", status=403)

  # extra error handling, maybe not needed, butttt
  if(updated_comment_info['success'] == False):
    return updated_comment_info['error']

  # no more errors can happen
  updated_comment_json = json.dumps(updated_comment_info['data'], default=str)
  return Response(updated_comment_json, mimetype="application/json", status=200)


def delete_comment():
  try:
    login_token = request.json['loginToken']
    comment_id = int(request.json['commentId'])
    if(comment_id <= 0):
      return Response("Invalid commentId", mimetype="text/plain", status=422)
  except ValueError:
    traceback.print_exc()
    return Response("One or more of the inputs is invalid!", mimetype="text/plain", status=422)
  except KeyError:
    traceback.print_exc()
    return Response("One or more required fields are empty!", mimetype="text/plain", status=422)
  except:
    traceback.print_exc()
    return Response("Unknown error with an input!", mimetype="text/plain", status=400)

  deleted_comment = dbh.run_query(
      "DELETE c FROM comments c INNER JOIN `session` s ON c.user_id = s.user_id WHERE c.id = ? AND s.token = ?", [comment_id, login_token])

  if(deleted_comment['success'] == False):
    return deleted_comment['error']

  if(deleted_comment['data'] == 1):
    return Response(status=204)
  else:
    traceback.print_exc()
    return Response("Authorization Error", mimetype='text/plain', status=400)
