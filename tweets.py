from flask import request, Response
import dbh
import json
import traceback


def list_tweets():
  # set user_id using args.get so it's not mandatory.
  try:
    user_id = request.args.get('userId')
    tweet_id = request.args.get('tweetId')
  except ValueError:
    return Response("NaN", mimetype="text/plain", status=422)
  except:
    traceback.print_exc()
    return Response("Error with id", mimetype="text/plain", status=400)

  # Base for SELECT query for user Id
  # todo fix select

  sql = "SELECT t.id AS tweetId, u.id AS userId, u.username, t.content, u.profile_pic_path AS userImageUrl, t.image_path AS tweetImageUrl, t.created_at AS createdAt FROM users u INNER JOIN takes t ON u.id = t.user_id"

  # Set params to empty list to use append later
  params = []

  # If user_id does not equal an empty string and doesnt equal None, add to the end of the base query, and append user_id to params list
  if(user_id != None and user_id != ''):
    # this try ensures we can error catch in a decent way, as well allowes us to return an empty list if the user exists but has no tweets
    try:
      user_id = dbh.run_query(
          "SELECT u.id from users u WHERE u.id = ?", [user_id, ])[0]['id']
    except IndexError:
      return Response("Not a valid userId", mimetype="text/plain", status=400)
    except:
      return Response("Unknown error with userId", mimetype="text/plain", status=400)

    if(type(user_id) is str):
      return dbh.exc_handler(user_id)

    sql += " WHERE u.id = ?"
    # Don't know if this is the right spot for this try/except, doesn't feel great, but works for now!
    params.append(user_id)

  elif(tweet_id != None and tweet_id != ''):
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

    sql += " WHERE t.id = ?"
    params.append(tweet_id)

  tweets = dbh.run_query(sql, params)

  if(type(tweets) is str):
    return dbh.exc_handler(tweets)

  # I think all errors are caught by this point.
  tweets_json = json.dumps(tweets, default=str)
  return Response(tweets_json, mimetype='application/json', status=200)


def create_tweet():
  try:
    # Get all required inputs.
    login_token = request.json['loginToken']
    content = request.json['content']
    # Get optional imageUrl
    image_url = request.json.get('imageUrl')
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

  # set user_id, get errors
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

  # Insert Query
  sql = "INSERT INTO takes"
  # starting point for params to pass to run_query helper function
  # includes content because content is mandatory.
  params = [content, user_id]

  # If imageUrl param has a vaue, insert content and and image_path, otherwise, just content.
  if(image_url != None and image_url != ''):
    sql += " (content, user_id, image_path) VALUES (?,?,?)"
    params.append(image_url)
  else:
    sql += " (content, user_id) VALUES (?,?)"

  # params.extend((username, email, password, bio, birthdate))
  new_tweet_id = dbh.run_query(sql, params)

  if(type(new_tweet_id) is str):
    return dbh.exc_handler(new_tweet_id)

  if(new_tweet_id != None):
    new_tweet_info = dbh.run_query(
        "SELECT t.id AS tweetId, u.id AS userId, u.username, u.profile_pic_path AS userImageUrl, t.content, t.image_path AS imageUrl, t.created_at AS createdAt FROM takes t INNER JOIN users u ON t.user_id = u.id WHERE t.id = ?", [new_tweet_id, ])

    new_tweet_json = json.dumps(new_tweet_info, default=str)
    return Response(new_tweet_json, mimetype="application/json", status=201)
  else:
    return Response("Failed to create tweet", mimetype="text/plain", status=400)


def update_tweet():
  try:
    # Get required inputs
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

  # update Query, includes setting the was_edited to 1(true) and edit_time to the current time(even though I probably won't use it until I rebuild!)
  sql = "UPDATE takes t INNER JOIN `session` s ON t.user_id = s.user_id SET t.content = ?, t.was_edited = 1, t.edit_time = NOW() WHERE s.token = ? AND t.id = ?"

  try:
    tweet_id = dbh.run_query(
        "SELECT t.id from takes t WHERE t.id = ?", [tweet_id, ])[0]['id']
  except IndexError:
    return Response("Invalid tweetId", mimetype="text/plain", status=400)
  except:
    return Response("Unknown error with tweetId", mimetype="text/plain", status=400)

  if(type(tweet_id) is str):
    return dbh.exc_handler(tweet_id)

  # run the update, update variable will equal the rowcount. Should be 1 if successful!
  updated_rows = dbh.run_query(
      sql, [content, login_token, tweet_id])

  if(type(updated_rows) is str):
    return dbh.exc_handler(updated_rows)

  # only happens if update was successful.
  # on update use == 1 instead of != 0
  if(updated_rows == 1):
    updated_tweet_info = dbh.run_query(
        "SELECT t.id AS tweetId, u.id AS userId, u.username, u.profile_pic_path AS userImageUrl, t.content, t.image_path AS imageUrl, t.created_at AS createdAt FROM takes t INNER JOIN users u ON t.user_id = u.id WHERE t.id = ?", [tweet_id, ])
  else:
    traceback.print_exc()
    return Response("Error: Invalid tweetId and loginToken combination", mimetype="text/plain", status=403)

  # extra error handling, maybe not needed, butttt
  if(type(updated_tweet_info) is str):
    return dbh.exc_handler(updated_tweet_info)

  # even more error handling! and return of data
  if(len(updated_tweet_info) == 1):
    updated_tweet_json = json.dumps(updated_tweet_info, default=str)
    return Response(updated_tweet_json, mimetype="application/json", status=200)
  else:
    traceback.print_exc()
    return Response("Failed to update", mimetype="text/plain", status=400)


def delete_tweet():
  try:
    login_token = request.json['loginToken']
    tweet_id = int(request.json['tweetId'])

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
    tweet_id = dbh.run_query(
        "SELECT t.id from takes t WHERE t.id = ?", [tweet_id, ])[0]['id']
  except IndexError:
    return Response("Invalid tweetId", mimetype="text/plain", status=400)
  except:
    return Response("Unknown error with tweetId", mimetype="text/plain", status=400)

  if(type(tweet_id) is str):
    return dbh.exc_handler(tweet_id)

  deleted_tweet = dbh.run_query(
      "DELETE t FROM takes t INNER JOIN `session` s ON t.user_id = s.user_id WHERE t.id = ? AND s.token = ?", [tweet_id, login_token])

  if(type(deleted_tweet) is str):
    return dbh.exc_handler(deleted_tweet)

  if(deleted_tweet == 1):
    return Response("Tweet Deleted Successfully!", mimetype='text/plain', status=201)
  else:
    traceback.print_exc()
    return Response("Error: tweetId or loginToken invalid, Please relog and try again", mimetype='text/plain', status=400)
