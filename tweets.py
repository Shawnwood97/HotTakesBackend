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
    return Response("Input was not a number!", mimetype="text/plain", status=422)
  except:
    traceback.print_exc()
    return Response("Error with id", mimetype="text/plain", status=400)

  # Base for SELECT query for user Id
  sql = "SELECT t.id AS tweetId, u.id AS userId, u.username, t.content, u.profile_pic_path AS userImageUrl, t.image_path AS tweetImageUrl, t.created_at AS createdAt FROM users u INNER JOIN takes t ON u.id = t.user_id"

  # Set params to empty list to use append later
  params = []

  # If user_id does not equal an empty string and doesnt equal None, add to the end of the base query, and append user_id to params list
  # ? I think I really like this check specifically, tweetId one is probably less useful so get an error if no user, but an empty list for users without tweets!
  if(user_id != None and user_id != ''):
    # this try ensures we can error catch in a decent way, as well allowes us to return an empty list if the user exists but has no tweets
    result = dbh.run_query(
        "SELECT u.id from users u WHERE u.id = ?", [user_id, ])

    if(result['success'] == False):
      return result['error']

    try:
      user_id = result['data'][0]['id']
    except:
      return Response("Data not found!", mimetype="text/plain", status=404)

  # add where to qeury if user_id does not equal None or empty string
    sql += " WHERE u.id = ?"
    params.append(user_id)

  elif(tweet_id != None and tweet_id != ''):
    sql += " WHERE t.id = ?"
    params.append(tweet_id)

  result = dbh.run_query(sql, params)

  if(result['success'] == False):
    return result['error']

  # I think all errors are caught by this point.
  tweets_json = json.dumps(result['data'], default=str)
  return Response(tweets_json, mimetype='application/json', status=200)


def create_tweet():
  try:
    # Get all required inputs.
    login_token = request.json['loginToken']
    content = request.json['content']
    # Get optional imageUrl
    image_url = request.json.get('imageUrl')

    #! Thanks Monica 😊
    # if content or login token are empty strings, return an error.
    if(content == '' and login_token == ''):
      return Response("Required fields cannot be empty strings", mimetype="text/plain", status=422)
  except KeyError:
    traceback.print_exc()
    return Response("One or more required fields are empty!", mimetype="text/plain", status=422)
  except:
    traceback.print_exc()
    return Response("Unknown error with an input!", mimetype="text/plain", status=400)

  # set result to the return of run_query from dbh.
  result = dbh.run_query(
      "SELECT user_id FROM `session` WHERE token = ?", [login_token, ])

  # error check on the success key returned by run_query, if False return the response.
  if(result['success'] == False):
    return result['error']

  # try to set the user_id var to the user id from the 0 index inside the data dictionary from result. #! confusing, I know.
  try:
    user_id = result['data'][0]['user_id']
  except:
    traceback.print_exc()
    return Response("Authorization Error!", mimetype="text/plain", status=403)

  # Base for Insert Query
  sql = "INSERT INTO takes"

  # starting point for params to pass to run_query helper function
  # includes content and user id becayse they are mandatory!
  params = [content, user_id]

  # If imageUrl param has a value, insert content, user_id and image_path and append image_url to params, otherwise, just content and user_id, no append needed
  # in else as they are mandatory and already there from default.
  if(image_url != None and image_url != ''):
    sql += " (content, user_id, image_path) VALUES (?,?,?)"
    params.append(image_url)
  else:
    sql += " (content, user_id) VALUES (?,?)"

  # run the query helper function to insert the take
  result = dbh.run_query(sql, params)

  # error check on the success key returned by run_query, if False return the response.
  if(result['success'] == False):
    return result['error']

  # after insertion of tweet was successful, parse content for hashtags.
  # here we pass the user_id, tweet_id, and content, in that order.
  # all errors should be caught in helper function.
  # tweet_id is so we could create a link back to the tweets where each hastag was userd, user_id is so we can attribute the author.
  dbh.parse_insert_hashtags(user_id, result['data'], content)

  # if data key is greater than -1 (lastrowid), run a select statement, else return an error response.
  if(result['data'] > -1):
    new_tweet_info = dbh.run_query(
        "SELECT t.id AS tweetId, u.id AS userId, u.username, u.profile_pic_path AS userImageUrl, t.content, t.image_path AS imageUrl, t.created_at AS createdAt FROM takes t INNER JOIN users u ON t.user_id = u.id WHERE t.id = ?", [result['data'], ])

  # error check on the success key returned by run_query, if False return the response.
    if(new_tweet_info['success'] == False):
      return new_tweet_info['error']
  # if the data dictionary has a length of 1, create the json and return a response
  if(len(new_tweet_info['data']) == 1):
    new_tweet_json = json.dumps(new_tweet_info['data'][0], default=str)
    return Response(new_tweet_json, mimetype="application/json", status=201)
  # otherwise, return error, if this happens, the insert happened but we were unable to get the data afterwards.
  else:
    return Response("Error getting tweet after insert!", mimetype="text/plain", status=404)


def update_tweet():
  try:
    # Get required inputs
    login_token = request.json['loginToken']
    tweet_id = int(request.json['tweetId'])
    content = request.json['content']
    if(tweet_id <= 0):
      return Response("Invalid commentId", mimetype="text/plain", status=422)
    if(login_token == '' and content == ''):
      return Response("Required fields cannot be empty strings", mimetype="text/plain", status=422)
  except ValueError:
    traceback.print_exc()
    return Response("One or more of the inputs is invalid!", mimetype="text/plain", status=422)
  except KeyError:
    traceback.print_exc()
    return Response("One or more required fields are empty!", mimetype="text/plain", status=422)
  except:
    traceback.print_exc()
    return Response("Unknown error with an input!", mimetype="text/plain", status=400)

  # update Query, includes setting the was_edited to 1(true) and edit_time to the current time(even though I probably won't use it until I rebuild!)
  sql = "UPDATE takes t INNER JOIN `session` s ON t.user_id = s.user_id SET t.content = ?, t.was_edited = 1, t.edit_time = NOW() WHERE s.token = ? AND t.id = ?"

  # run the update, update variable will equal the rowcount. Should be 1 if successful!
  result = dbh.run_query(
      sql, [content, login_token, tweet_id])

  if(result['success'] == False):
    return result['error']

  # only happens if update was successful.
  # on update use == 1 instead of != 0
  if(result['data'] == 1):
    updated_tweet_info = dbh.run_query(
        "SELECT t.id AS tweetId, u.id AS userId, u.username, u.profile_pic_path AS userImageUrl, t.content, t.image_path AS imageUrl, t.created_at AS createdAt FROM takes t INNER JOIN users u ON t.user_id = u.id WHERE t.id = ?", [result['data'], ])
  else:
    # this seems better?
    traceback.print_exc()
    return Response("Authorization Error!", mimetype="text/plain", status=403)

  # extra error handling, maybe not needed, butttt
  if(updated_tweet_info['success'] == False):
    return updated_tweet_info['error']

  updated_tweet_json = json.dumps(updated_tweet_info['data'][0], default=str)
  return Response(updated_tweet_json, mimetype="application/json", status=200)


def delete_tweet():
  try:
    # get required info for deleting a tweet
    login_token = request.json['loginToken']
    tweet_id = int(request.json['tweetId'])
    # additional error checking.
    if(tweet_id <= 0):
      return Response("Invalid tweetId", mimetype="text/plain", status=422)
    if(login_token == ''):
      return Response("Required fields cannot be empty strings", mimetype="text/plain", status=422)
  except ValueError:
    traceback.print_exc()
    return Response("One or more of the inputs is invalid!", mimetype="text/plain", status=422)
  except KeyError:
    traceback.print_exc()
    return Response("One or more required fields are empty!", mimetype="text/plain", status=422)
  except:
    traceback.print_exc()
    return Response("Unknown error with an input!", mimetype="text/plain", status=400)

  # delete query, inner joined on session, validated with login token.
  result = dbh.run_query(
      "DELETE t FROM takes t INNER JOIN `session` s ON t.user_id = s.user_id WHERE t.id = ? AND s.token = ?", [tweet_id, login_token])

  if(result['success'] == False):
    return result['error']

  # if result returned 1 for rowcount, return status 204 (no content)
  if(result['data'] == 1):
    return Response(status=204)
  # else auth error return.
  else:
    traceback.print_exc()
    return Response("Authorization Error!", mimetype='text/plain', status=403)
