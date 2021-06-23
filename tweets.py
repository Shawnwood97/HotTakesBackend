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

  if(user_id != None and user_id != ''):
    user_id = dbh.run_query(
        "SELECT u.id FROM users u WHERE u.id = ?", [user_id, ])

    sql = "SELECT t.id AS tweetId, u.id AS userId, u.username, t.content, u.profile_pic_path AS userImageUrl, t.image_path AS tweetImageUrl, t.created_at AS createdAt FROM users u INNER JOIN takes t ON u.id = t.user_id"
  if(type(user_id) is str):
    return dbh.exc_handler(user_id)
  else:
    sql = "SELECT t.id AS tweetId, u.id AS userId, u.username, t.content, u.profile_pic_path AS userImageUrl, t.image_path AS tweetImageUrl, t.created_at AS createdAt FROM users u INNER JOIN takes t ON u.id = t.user_id"

  # Set params to empty list to use append later
  params = []

  # If user_id does not equal an empty string and doesnt equal None, add to the end of the base query, and append user_id to params list
  if(user_id != None and user_id != ''):
    sql += " WHERE u.id = ?"
    # Don't know if this is the right spot for this try/except, doesn't feel great, but works for now!
    try:
      params.append(user_id[0]["id"])
    except IndexError:
      return Response("userId does not exist!", mimetype="text/plain", status=404)
    except:
      return Response("Unkown Error with user Id!", mimetype="text/plain", status=400)

  elif(tweet_id != None and tweet_id != ''):
    sql += " WHERE t.id = ?"
    params.append(tweet_id)

  tweets = dbh.run_query(sql, params)

  if(type(tweets) is str):
    return dbh.exc_handler(tweets)

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

  # # Statement to get user id from the session table for verification
  # user_id_sql = "SELECT user_id FROM `session` s WHERE s.token = ?"

  # # SELECT query will return the user id. #! removed to save an additional query
  # user_id = dbh.run_query(user_id_sql, [login_token, ])

  user_info = dbh.run_query(
      "SELECT u.id FROM users u INNER JOIN `session` s ON u.id = s.user_id WHERE s.token = ?", [login_token, ])

  if(type(user_info) is str):
    return dbh.exc_handler(user_info)

  # Insert Query
  sql = "INSERT INTO takes"
  # starting point for params to pass to run_query helper function
  # includes content because content is mandatory.
  params = [content, user_info[0]["id"]]

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
        "SELECT t.id, u.id, u.username, u.profile_pic_path AS userImageUrl, t.content, t.image_path AS imageUrl, t.created_at AS createdAt FROM takes t INNER JOIN users u ON t.user_id = u.id WHERE t.id = ?", [new_tweet_id, ])

    new_tweet_json = json.dumps(new_tweet_info, default=str)
    return Response(new_tweet_json, mimetype="application/json", status=201)
  else:
    return Response("Failed to create tweet", mimetype="text/plain", status=400)
