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
