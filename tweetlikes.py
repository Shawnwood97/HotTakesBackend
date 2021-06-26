from flask import request, Response
import dbh
import json
import traceback


def add_tweet_like():
  try:
    login_token = request.json['loginToken']
    tweet_id = int(request.json['tweetId'])
    if(tweet_id <= 0):
      return Response("Invalid tweetId", mimetype="text/plain", status=422)
  except ValueError:
    traceback.print_exc()
    return Response("One or more of the inputs is invalid!", mimetype="text/plain", status=422)
  except KeyError:
    traceback.print_exc()
    return Response("One or more required fields are empty!", mimetype="text/plain", status=422)
  except:
    traceback.print_exc()
    return Response("Unknown error with an input!", mimetype="text/plain", status=400)

  # Get current user_id using their login token for use in the insert statement.
  # I need the userId later, so I think this extra query is ok for validation
  user_sql = "SELECT s.user_id FROM `session` s WHERE token = ?"
  try:
    user_id = dbh.run_query(user_sql, [login_token, ])[0]['user_id']
    # general except should be fine here, if it fails we assume it's an auth error.
  except:
    return Response("Authorization Error", mimetype="text/plain", status=403)

  if(type(user_id) is str):
    return dbh.exc_handler(user_id)

  # SQL statement to create the like
  like_sql = "INSERT INTO take_hot_cold (take_id, user_id) VALUES (?,?)"

  #  check if tweet_id isnt None or empty, then set tweet_id to the tweet id from the db
  # still unsure if this is bad, seems like good verification, but also maybe not needed???
  # return error if theres an index error on the tweet_id or user_id, which will in turn tell us
  # if the loginToken was wrong since it is used to get the user_id
  # ? removing this, seems like something we don't really need. Semantically it feels okay, but realistically, not needed?
  # if(tweet_id != None and tweet_id != ''):
  #   try:
  #     tweet_id = dbh.run_query(
  #         'SELECT t.id from takes t WHERE t.id = ?', [tweet_id, ])[0]['id']
  #   except IndexError:
  #     return Response("tweetId does not exist!", mimetype="text/plain", status=404)
  #   except:
  #     return Response("Unkown error with tweetId", mimetype="text/plain", status=404)

  # if(type(tweet_id) is str):
  #   return dbh.exc_handler(tweet_id)

# tweetId has to be a number due to Value error above, this should all be good
  like_id = dbh.run_query(
      like_sql, [tweet_id, user_id])

  if(type(like_id) is str):
    return dbh.exc_handler(like_id)
  #! does this else make more sense than the if below it??
  # else:
  #   return Response(status=204)

  # ?Dont think there's any need for an else here, which means probably not much use for an if here.
  # ? maybe I add an else to the above helper catch that responds success?
  if(like_id > -1):
    return Response(status=204)


def list_tweet_likes():
    # set user_id using args because it is a get request
    #! for future I probably want the ability to send userId and get all likes by a specific user
    #! useful for a "liked tweets tab, should make front end easier!??"
  try:
    tweet_id = request.args.get('tweetId')
    if(tweet_id != None or tweet_id != ''):
      tweet_id = int(tweet_id)
      # ? this seems like an okay error check?
    if(tweet_id <= 0):
      return Response("Invalid tweetId", mimetype="text/plain", status=422)
  except ValueError:
    return Response("tweetId must be a number!", mimetype="text/plain", status=422)
  except KeyError:
    return Response("No tweetId Sent", mimetype="text/plain", status=400)
  except:
    traceback.print_exc()
    return Response("Unknown Error with tweetId", mimetype="text/plain", status=400)

  sql = "SELECT t.take_id AS tweetId, t.user_id AS userId, u.username FROM take_hot_cold t INNER JOIN users u ON t.user_id = u.id"

  params = []

  if(tweet_id != None and tweet_id != ''):
      # ? probably overkill
    #   try:
    #     tweet_id = dbh.run_query(
    #         'SELECT t.id from takes t WHERE t.id = ?', [tweet_id, ])[0]['id']
    #   except IndexError:
    #     return Response("tweetId does not exist!", mimetype="text/plain", status=404)
    #   except:
    #     return Response("Unkown error with tweetId", mimetype="text/plain", status=404)

    sql += ' WHERE t.take_id = ?'
    params.append(tweet_id)
  # Check for non mariadb exceptions

  liked_tweets = dbh.run_query(sql, params)

  if(type(liked_tweets) is str):
    return dbh.exc_handler(liked_tweets)

  # cant think of any other errors to catch at this point, should all be caught elsewhere?
  liked_tweets_json = json.dumps(liked_tweets, default=str)
  return Response(liked_tweets_json, mimetype='application/json', status=200)


def remove_tweet_like():
  try:
    login_token = request.json['loginToken']
    tweet_id = int(request.json['tweetId'])
    if(tweet_id <= 0):
      return Response("Invalid tweetId", mimetype="text/plain", status=422)
  except ValueError:
    traceback.print_exc()
    return Response("One or more of the inputs is invalid!", mimetype="text/plain", status=422)
  except KeyError:
    traceback.print_exc()
    return Response("One or more required fields are empty!", mimetype="text/plain", status=422)
  except:
    traceback.print_exc()
    return Response("Unknown error with an input!", mimetype="text/plain", status=400)

# using this type of error checking in lots of places, I like it, but don't know if good. mostly all uses PK's so indexing should make it fast.
  # ? overkill?
  # try:
  #   tweet_id = dbh.run_query(
  #       'SELECT t.id from takes t WHERE t.id = ?', [tweet_id, ])[0]['id']
  # except IndexError:
  #   return Response("tweetId does not exist!", mimetype="text/plain", status=404)
  # except:
  #   return Response("Unkown error with tweetId", mimetype="text/plain", status=404)

  # if(type(tweet_id) is str):
  #   return dbh.exc_handler(tweet_id)
# ? overkill again?
  # try:
  #   login_token = dbh.run_query(
  #       'SELECT s.token FROM `session` s WHERE s.token = ?', [login_token, ])[0]['token']
  # except IndexError:
  #   return Response("Invalid loginToken, relog and try again!", mimetype="text/plain", status=404)
  # except:
  #   return Response("Unkown error with loginToken!", mimetype="text/plain", status=404)

  # if(type(list(login_token)) is str):
  #   return dbh.exc_handler(login_token)

  # this makes me feel like I am doing so many things wrong in other places!
  removed_tweet_like = dbh.run_query(
      "DELETE th FROM take_hot_cold th INNER JOIN `session` s ON th.user_id = s.user_id WHERE th.take_id = ? AND s.token = ?", [tweet_id, login_token])

  if(type(removed_tweet_like) is str):
    return dbh.exc_handler(removed_tweet_like)

  if(removed_tweet_like == 1):
    return Response(status=204)
  else:
    traceback.print_exc()
    return Response("Authorization Error!", mimetype='text/plain', status=403)
