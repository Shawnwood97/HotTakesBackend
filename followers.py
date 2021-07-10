from flask import request, Response
import dbh
import json
import traceback


def list_followers():
    # set user_id using request.args because its a get request
  try:
    user_id = int(request.args['userId'])
    # a user id cannot be 0 or less, so error if so.
    if(user_id <= 0):
      return Response("Invalid userId", mimetype="text/plain", status=422)
  except ValueError:
    return Response("userId must be a number!", mimetype="text/plain", status=422)
  except KeyError:
    return Response("No userId Sent", mimetype="text/plain", status=400)
  except:
    traceback.print_exc()
    return Response("Error with id", mimetype="text/plain", status=400)

  # Select query with inner join to create a new temp table to compare params
  sql = "SELECT u.id AS userId, u.username, u.display_name, u.email, u.birthdate, u.first_name, u.last_name, u.headline AS bio, u.website_link, u.location, u.phone_number, u.is_verified, u.profile_pic_path AS imageUrl, u.profile_banner_path AS bannerUrl, u.is_active, u.created_at FROM users u INNER JOIN follows f ON u.id = f.follower_id WHERE f.followed_id = ?"

  result = dbh.run_query(
      sql, [user_id, ])

  if(result['success'] == False):
    return result['error']
    # our standard error checking to ensure our select returned data.
  # if(len(result['data']) != 0 and result['data'] == []):
  followers_json = json.dumps(result['data'], default=str)
  return Response(followers_json, mimetype='application/json', status=200)
  # else:
  #   return Response("Error getting followers.", mimetype="text/plain", status=404)
