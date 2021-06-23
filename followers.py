from flask import request, Response
import dbh
import json
import traceback


def list_followers():
    # set user_id using args because its a get request
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
  sql = "SELECT u.id AS userId, u.username, u.display_name, u.email, u.birthdate, u.first_name, u.last_name, u.headline AS bio, u.website_link, u.location, u.phone_number, u.is_verified, u.profile_pic_path AS imageUrl, u.profile_banner_path AS bannerUrl, u.is_active, u.created_at FROM users u INNER JOIN follows f ON u.id = f.follower_id WHERE f.followed_id = ?"

  if(user_id != None and user_id != ''):
    user_id = dbh.run_query(
        "SELECT u.id from users u WHERE u.id = ?", [user_id, ])

  if(type(user_id) is str):
    return dbh.exc_handler(user_id)

  try:
    followers_list = dbh.run_query(
        sql, [user_id[0]["id"]])
  except IndexError:
    return Response("userId does not exist!", mimetype="text/plain", status=404)
  except:
    return Response("Unkown Error with user Id!", mimetype="text/plain", status=400)

  if(type(followers_list) is str):
    return dbh.exc_handler(followers_list)

  followers_json = json.dumps(followers_list, default=str)
  return Response(followers_json, mimetype='application/json', status=200)
