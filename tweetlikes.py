from flask import request, Response
import dbh
import json
import traceback


def add_tweet_like():
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

  # Get current user_id using their login token for use in the insert statement.
  user_sql = "SELECT s.user_id FROM `session` s WHERE token = ?"

  user_id = dbh.run_query(user_sql, [login_token, ])

  if(type(user_id) is str):
    return dbh.exc_handler(user_id)

  # SQL statement to create the like
  like_sql = "INSERT INTO take_hot_cold (take_id, user_id) VALUES (?,?)"

  #  check if tweet_id isnt None or empty, then set tweet_id to the tweet id from the db
  # still unsure if this is bad, seems like good verification, but also maybe not needed???
  # return error if theres an index error on the tweet_id or user_id, which will in turn tell us
  # if the loginToken was wrong since it is used to get the user_id
  if(tweet_id != None and tweet_id != ''):
    tweet_id = dbh.run_query(
        'SELECT t.id from takes t WHERE t.id = ?', [tweet_id, ])
  try:
    like_id = dbh.run_query(
        like_sql, [tweet_id[0]['id'], user_id[0]['user_id']])
  except IndexError:
    return Response("tweetId or loginToken does not exist!", mimetype="text/plain", status=404)
  except:
    return Response("Unkown Error with tweetId or loginToken!", mimetype="text/plain", status=400)

  if(type(like_id) is str):
    return dbh.exc_handler(like_id)
  else:
    return Response("Tweet Like Success!", mimetype='text/plain', status=201)


def list_tweet_likes():
    # set user_id using args because it is a get request
  try:
    tweet_id = request.args.get('tweetId')
  except ValueError:
    return Response("NaN", mimetype="text/plain", status=422)
  except KeyError:
    return Response("No tweetId Sent", mimetype="text/plain", status=400)
  except:
    traceback.print_exc()
    return Response("Unknown Error with tweetId", mimetype="text/plain", status=400)

  sql = "SELECT t.id AS tweetId, t.user_id AS userId, u.username FROM take_hot_cold t INNER JOIN users u ON t.user_id = u.id"

  params = []

  if(tweet_id != None and tweet_id != ''):
    sql += ' WHERE t.id = ?'
    params.append(tweet_id)
  # Check for non mariadb exceptions

  liked_tweets = dbh.run_query(sql, params)

  if(type(liked_tweets) is str):
    return dbh.exc_handler(liked_tweets)

  # I know this isnt a perfect error catch, but it works for the time being!
  if(len(liked_tweets) == 0):
    return Response("tweetId does not exist!", mimetype="text/plain", status=404)

  liked_tweets_json = json.dumps(liked_tweets, default=str)
  return Response(liked_tweets_json, mimetype='application/json', status=200)


def remove_tweet_like():
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

  # this makes me feel like I am doing so many things wrong in other places!
  removed_tweet_like = dbh.run_query(
      "DELETE th FROM take_hot_cold th INNER JOIN `session` s ON th.user_id = s.user_id WHERE th.take_id = ? AND s.token = ?", [tweet_id, login_token])

  if(type(removed_tweet_like) is str):
    return dbh.exc_handler(removed_tweet_like)

  if(removed_tweet_like == 1):
    return Response("Unlike Success!", mimetype='text/plain', status=201)
  else:
    traceback.print_exc()
    return Response("Error Unliking tweet, token or tweetId invalid!", mimetype='text/plain', status=400)
