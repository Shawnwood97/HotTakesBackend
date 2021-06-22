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
  sql = "SELECT u.id, u.username, u.display_name, u.email, u.birthdate, u.first_name, u.last_name, u.headline, u.website_link, u.location, u.phone_number, u.is_verified, u.profile_pic_path, u.profile_banner_path, u.is_active, u.created_at FROM users u INNER JOIN follows f ON u.id = f.follower_id WHERE f.followed_id = ?"

  followers = dbh.run_query(sql, [user_id, ])

  if(type(followers) is str):
    return dbh.exc_handler(followers)

  # List defined to append each follower into
  followers_list = []
  # loop through all followers and append each dict to the list.
  for follower in followers:
    user_info_json = {
        'userId': follower[0],
        'email': follower[3],
        'username': follower[1],
        'bio': follower[7],
        'birthdate': follower[4],
        'imageUrl': follower[12],
        'bannerUrl': follower[13]
    }
    followers_list.append(user_info_json)

  followers_json = json.dumps(followers_list, default=str)
  return Response(followers_json, mimetype='application/json', status=200)
