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
  rel_id = dbh.run_query(follow_rel_sql, [user_id[0][0], follow_id])

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
  sql = "SELECT u.id, u.username, u.display_name, u.email, u.birthdate, u.first_name, u.last_name, u.headline, u.website_link, u.location, u.phone_number, u.is_verified, u.profile_pic_path, u.profile_banner_path, u.is_active, u.created_at FROM users u INNER JOIN follows f ON u.id = f.followed_id WHERE f.follower_id = ?"

  followed_users = dbh.run_query(sql, [user_id, ])

  if(type(followed_users) is str):
    return dbh.exc_handler(followed_users)

  # List defined to append followed each user into
  users_list = []
  # loop through all users returned by followed_users
  for user in followed_users:
    user_info_json = {
        'userId': user[0],
        'email': user[3],
        'username': user[1],
        'bio': user[7],
        'birthdate': user[4],
        'imageUrl': user[12],
        'bannerUrl': user[13]
    }
    users_list.append(user_info_json)

  users_json = json.dumps(users_list, default=str)
  return Response(users_json, mimetype='application/json', status=200)


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
    return Response("Error unfollowing user!", mimetype='text/plain', status=400)
