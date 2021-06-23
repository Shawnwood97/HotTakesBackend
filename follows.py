from flask import request, Response
import dbh
import json
import traceback


def new_follow():
  try:
    login_token = request.json['loginToken']
    follow_id = int(request.json['followId'])

  except ValueError:
    traceback.print_exc()
    return Response("Error: One or more of the inputs is invalid!", mimetype="text/plain", status=422)
  except KeyError:
    traceback.print_exc()
    return Response("Error: One or more required fields are empty!", mimetype="text/plain", status=422)
  except:
    traceback.print_exc()
    return Response("Error: Unknown error with an input!", mimetype="text/plain", status=400)

  # Get current user id using their login token for use in the insert statement.
  user_sql = "SELECT user_id FROM `session` WHERE token = ?"

  user_id = dbh.run_query(user_sql, [login_token, ])

  if(type(user_id) is str):
    return dbh.exc_handler(user_id)

  # SQL statement to create the follow relationship.
  follow_rel_sql = "INSERT INTO follows (follower_id, followed_id) VALUES (?,?)"

  # run_query function will return the id of the row, represented here as the relationship Id. Select statement returns a list of tuples
  # therefor user_id [0][0] is the actual id, and since only 1 relationship can be created at a time, this works.
  if(follow_id != None and follow_id != ''):
    follow_id = dbh.run_query(
        'SELECT u.id from users u WHERE u.id = ?', [follow_id, ])

  try:
    rel_id = dbh.run_query(
        follow_rel_sql, [user_id[0]["user_id"], follow_id[0]["id"]])
  except IndexError:
    return Response("followId does not exist!", mimetype="text/plain", status=404)
  except:
    return Response("Unkown Error with user Id!", mimetype="text/plain", status=400)

  if(type(rel_id) is str):
    return dbh.exc_handler(rel_id)
  else:
    return Response("Follow Success!", mimetype='text/plain', status=201)


def list_follows():
    # set user_id using args because it is a get request
  try:
    user_id = int(request.args['userId'])
  except ValueError:
    return Response("NaN", mimetype="text/plain", status=422)
  except KeyError:
    return Response("No userId Sent", mimetype="text/plain", status=400)
  except:
    traceback.print_exc()
    return Response("Error with id", mimetype="text/plain", status=400)

  # Select query with inner join to create a new temp table to compare params
  if(user_id != None and user_id != ''):
    user_id = dbh.run_query(
        "SELECT u.id FROM users u WHERE u.id = ?", [user_id, ])

    sql = "SELECT u.id AS userId, u.username, u.display_name, u.email, u.birthdate, u.first_name, u.last_name, u.headline AS bio, u.website_link, u.location, u.phone_number, u.is_verified, u.profile_pic_path AS imageUrl, u.profile_banner_path AS bannerUrl, u.is_active, u.created_at FROM users u INNER JOIN follows f ON u.id = f.followed_id WHERE f.follower_id = ?"

  # Check for non mariadb exceptions
  try:
    followed_users = dbh.run_query(sql, [user_id[0]["id"], ])
  except IndexError:
    return Response("userId does not exist!", mimetype="text/plain", status=404)
  except:
    return Response("Unknown error with userId", mimetype="text/plain", status=400)

  if(type(followed_users) is str):
    return dbh.exc_handler(followed_users)

  followed_users_json = json.dumps(followed_users, default=str)
  return Response(followed_users_json, mimetype='application/json', status=200)


def remove_follow():
  try:
    login_token = request.json['loginToken']
    follow_id = int(request.json['followId'])

  except ValueError:
    traceback.print_exc()
    return Response("Error: One or more of the inputs is invalid!", mimetype="text/plain", status=422)
  except KeyError:
    traceback.print_exc()
    return Response("Error: One or more required fields are empty!", mimetype="text/plain", status=422)
  except:
    traceback.print_exc()
    return Response("Error: Unknown error with an input!", mimetype="text/plain", status=400)

  # This var will hold 1 if the unfollow happened and 0 if it failed, should not be able to be anything else.
  rem_follow_rel = dbh.run_query(
      "DELETE f FROM follows f INNER JOIN `session` s ON s.user_id = f.follower_id WHERE f.followed_id = ? AND s.token = ?", [follow_id, login_token])

  if(type(rem_follow_rel) is str):
    return dbh.exc_handler(rem_follow_rel)

  if(rem_follow_rel == 1):
    return Response("Unfollow Success!", mimetype='text/plain', status=201)
  else:
    traceback.print_exc()
    return Response("Error unfollowing user, token or followId invalid!", mimetype='text/plain', status=400)
