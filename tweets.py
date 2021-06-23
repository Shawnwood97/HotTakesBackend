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

  # not sure if this is right, but when testing for errors, IndexError only ever came up when there was a wrong loginToken used, So I used that as the error here!
  try:
    params = [content, user_info[0]["id"]]
  except IndexError:
    traceback.print_exc()
    return Response("Error: Login Token invalid, please relog", mimetype="text/plain", status=404)
  except:
    return Response("Error: Unkown Error", mimetype="text/plain", status=400)

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
    tweet_id = request.json['tweetId']
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

  # tried error catching here, didnt work, on the login_token set below it seems to catch both errors, which is maybe best
  # in order to be more secure and not tell exactly where the issue is?
  # This is how I decided to verify login_token vs the DB, unsure if correct, but works.
  if(login_token != None and login_token != ''):
    # try:
    login_token = dbh.run_query(
        "SELECT s.token FROM `session` s INNER JOIN takes t ON s.user_id = t.user_id WHERE s.token = ? AND t.id = ?", [login_token, tweet_id])
    # except IndexError:
    #   traceback.print_exc()
    #   return Response("Error: Login Token invalid, Please relog", mimetype="text/plain", status=404)
    # except:
    #   traceback.print_exc()
    #   return Response("Error: Unkown Error With Token, Please Relog", mimetype="text/plain", status=400)

  if(type(login_token) is str):
    return dbh.exc_handler(login_token)

  # same as above with login token, except this one has the error handling as well.
  if(tweet_id != None and tweet_id != ''):
    try:
      tweet_id = dbh.run_query(
          "SELECT t.id FROM takes t INNER JOIN `session` s ON t.user_id = s.user_id WHERE t.id = ? AND s.token = ?", [tweet_id, login_token[0]['token']])
    except IndexError:
      traceback.print_exc()
      return Response("Error: tweetId invalid or loginToken invalid, Please relog and try again", mimetype="text/plain", status=404)
    except:
      traceback.print_exc()
      return Response("Error: Unknown Error With tweetId or loginToken, Please relog and try again", mimetype="text/plain", status=400)

  if(type(tweet_id) is str):
    return dbh.exc_handler(tweet_id)

  # update Query, includes setting the was_edited to 1(true) and edit_time to the current time(even though I probably won't use it until I rebuild!)
  sql = "UPDATE takes t INNER JOIN `session` s ON t.user_id = s.user_id SET t.content = ?, t.was_edited = 1, t.edit_time = NOW() WHERE s.token = ? AND t.id = ?"

  # run the update, update variable will equal the rowcount. Should be 1 if successful!
  update = dbh.run_query(
      sql, [content, login_token[0]['token'], tweet_id[0]['id']])

  if(type(update) is str):
    return dbh.exc_handler(update)

  # only happens if update was successful.
  if(update != 0):
    updated_tweet_info = dbh.run_query(
        "SELECT t.id AS tweetId, u.id AS userId, u.username, u.profile_pic_path AS userImageUrl, t.content, t.image_path AS imageUrl, t.created_at AS createdAt FROM takes t INNER JOIN users u ON t.user_id = u.id WHERE t.id = ?", [tweet_id[0]['id'], ])
  else:
    #! this likely does not need to be here
    traceback.print_exc()
    return Response("Failed to update", mimetype="text/plain", status=400)

  # extra error handling, maybe not needed, butttt
  if(type(updated_tweet_info) is str):
    return dbh.exc_handler(updated_tweet_info)

  # even more error handling!
  if(len(updated_tweet_info) != 1):
    traceback.print_exc()
    return Response("Failed to update", mimetype="text/plain", status=400)
  else:
    updated_tweet_json = json.dumps(updated_tweet_info, default=str)
    return Response(updated_tweet_json, mimetype="application/json", status=201)


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

  # error catching, this one seems to catch the login token being incorrect
  # this also verifies that both exist by comparing user_id on the session token to user_id on the tweet_id and comparing with the given data!
  if(tweet_id != None and tweet_id != ''):
    try:
      tweet_id = dbh.run_query(
          "SELECT t.id FROM takes t INNER JOIN `session` s ON t.user_id = s.user_id WHERE t.id = ? AND s.token = ?", [tweet_id, login_token])
    except IndexError:
      traceback.print_exc()
      return Response("Error: tweetId invalid or loginToken invalid, Please relog and try again", mimetype="text/plain", status=404)
    except:
      traceback.print_exc()
      return Response("Error: Unknown Error With tweetId or loginToken, Please relog and try again", mimetype="text/plain", status=400)

  # This var will hold 1 if the delete happened and 0 if it failed, should not be able to be anything else.
  # error catch here seems to catch the tweetId being incorrect.
  try:
    deleted_tweet = dbh.run_query(
        "DELETE t FROM takes t INNER JOIN `session` s ON s.user_id = t.user_id WHERE t.id = ? AND s.token = ?", [tweet_id[0]['id'], login_token])
  except IndexError:
    traceback.print_exc()
    return Response("Error: tweetId invalid or loginToken invalid, Please relog and try again", mimetype="text/plain", status=404)
  except:
    traceback.print_exc()
    return Response("Error: Unknown Error With tweetId or loginToken, Please relog and try again", mimetype="text/plain", status=400)

  if(type(deleted_tweet) is str):
    return dbh.exc_handler(deleted_tweet)

  if(deleted_tweet == 1):
    return Response("Tweet Deleted Successfully!", mimetype='text/plain', status=201)
  else:
    traceback.print_exc()
    return Response("Error deletling tweet!", mimetype='text/plain', status=400)
