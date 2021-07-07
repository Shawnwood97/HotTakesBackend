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

  result = dbh.run_query(user_sql, [login_token, ])
  if(result['success'] == False):
    return result['error']
  try:
    user_id = result['data'][0]['user_id']
    # general except should be fine here, if it fails we assume it's an auth error.
  except:
    return Response("Authorization Error", mimetype="text/plain", status=403)

  # SQL statement to create the like
  like_sql = "INSERT INTO take_hot_cold (take_id, user_id) VALUES (?,?)"


# tweetId has to be a number due to Value error above, this should all be good
  like_id = dbh.run_query(
      like_sql, [tweet_id, user_id])

  if(like_id['success'] == False):
    return like_id['error']

  # ?Dont think there's any need for an else here, which means probably not much use for an if here.
  # ? maybe I add an else to the above helper catch that responds success?
  if(like_id['data'] > -1):
    return Response(status=204)


def list_tweet_likes():
    # set user_id using args because it is a get request
    #! for future I probably want the ability to send userId and get all likes by a specific user
    #! useful for a "liked tweets tab, should make front end easier!??"
  try:
    tweet_id = request.args.get('tweetId')
    if(tweet_id != None and tweet_id != ''):
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

    sql += ' WHERE t.take_id = ?'
    params.append(tweet_id)

  liked_tweets = dbh.run_query(sql, params)

  if(liked_tweets['success'] == False):
    return liked_tweets['error']

  # cant think of any other errors to catch at this point, should all be caught elsewhere?
  liked_tweets_json = json.dumps(liked_tweets['data'], default=str)
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

  # this makes me feel like I am doing so many things wrong in other places!
  result = dbh.run_query(
      "DELETE th FROM take_hot_cold th INNER JOIN `session` s ON th.user_id = s.user_id WHERE th.take_id = ? AND s.token = ?", [tweet_id, login_token])

  if(result['success'] == False):
    return result['error']

  if(result['data'] == 1):
    return Response(status=204)
  else:
    traceback.print_exc()
    return Response("Authorization Error!", mimetype='text/plain', status=403)
