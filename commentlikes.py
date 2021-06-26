from flask import request, Response
import dbh
import json
import traceback


def add_comment_like():
  try:
    login_token = request.json['loginToken']
    comment_id = int(request.json['commentId'])
    if(comment_id <= 0):
      return Response("Invalid commentId", mimetype="text/plain", status=422)
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
  # need this later so doesnt feel like overkill here!
  try:
    user_id = dbh.run_query("SELECT s.user_id FROM `session` s WHERE token = ?", [
                            login_token, ])[0]['user_id']
  except:
    return Response("Authorization error!", mimetype="text/plain", status=403)

  if(type(user_id) is str):
    return dbh.exc_handler(user_id)

  # SQL statement to create the like
  like_sql = "INSERT INTO comment_hot_cold (comment_id, user_id) VALUES (?,?)"

  #  check if comment_id isnt None or empty, then set comment_id to the comment id from the db
  # still unsure if this is bad, seems like good verification, but also maybe not needed???
  # return error if theres an index error on the comment_id or user_id, which will in turn tell us
  # if the loginToken was wrong since it is used to get the user_id

# ? overkill?????????????????
  # try:
  #   comment_id = dbh.run_query(
  #       'SELECT c.id from comments c WHERE c.id = ?', [comment_id, ])[0]['id']
  # except IndexError:
  #   return Response("commentId does not exist!", mimetype="text/plain", status=404)
  # except:
  #   return Response("Unkown error with commentId", mimetype="text/plain", status=404)

  # if(type(comment_id) is str):
  #   return dbh.exc_handler(comment_id)

  like_id = dbh.run_query(
      like_sql, [comment_id, user_id])

  if(type(like_id) is str):
    return dbh.exc_handler(like_id)
  #! does this else make more sense than the if below it??
  # else:
  #   return Response(status=204)

  # ? maybe I add an else to the above helper catch that responds success?
  if(like_id > -1):
    return Response(status=204)


def list_comment_likes():
    # set user_id using args because it is a get request
  try:
    comment_id = request.args.get('commentId')
    if(comment_id != None or comment_id != ''):
      comment_id = int(comment_id)
      # ? this seems like an okay error check?
    if(comment_id <= 0):
      return Response("Invalid commentId", mimetype="text/plain", status=422)
  except ValueError:
    return Response("NaN", mimetype="text/plain", status=422)
  except KeyError:
    return Response("No commentId Sent", mimetype="text/plain", status=400)
  except:
    traceback.print_exc()
    return Response("Unknown Error with commentId", mimetype="text/plain", status=400)

  sql = "SELECT ch.comment_id AS commentId, ch.user_id AS userId, u.username FROM comment_hot_cold ch INNER JOIN users u ON ch.user_id = u.id"

  params = []

  if(comment_id != None and comment_id != ''):

    sql += ' WHERE ch.comment_id = ?'
    params.append(comment_id)
  # Check for non mariadb exceptions

  liked_comments = dbh.run_query(sql, params)

  if(type(liked_comments) is str):
    return dbh.exc_handler(liked_comments)

  liked_comments_json = json.dumps(liked_comments, default=str)
  return Response(liked_comments_json, mimetype='application/json', status=200)


def remove_comment_like():
  try:
    login_token = request.json['loginToken']
    comment_id = int(request.json['commentId'])

    if(comment_id <= 0):
      return Response("Invalid commentId", mimetype="text/plain", status=422)
  except ValueError:
    traceback.print_exc()
    return Response("Error: One or more of the inputs is invalid!", mimetype="text/plain", status=422)
  except KeyError:
    traceback.print_exc()
    return Response("Error: One or more required fields are empty!", mimetype="text/plain", status=422)
  except:
    traceback.print_exc()
    return Response("Error: Unknown error with an input!", mimetype="text/plain", status=400)
# ? more overkill!?!?
# # using this type of error checking in lots of places, I like it, but don't know if good. mostly all uses PK's so indexing should make it fast.
#   try:
#     comment_id = dbh.run_query(
#         'SELECT c.id from comments c WHERE c.id = ?', [comment_id, ])[0]['id']
#   except IndexError:
#     return Response("commentId does not exist!", mimetype="text/plain", status=404)
#   except:
#     return Response("Unkown error with commentId", mimetype="text/plain", status=404)

#   if(type(comment_id) is str):
#     return dbh.exc_handler(comment_id)

#   try:
#     login_token = dbh.run_query(
#         'SELECT s.token FROM `session` s WHERE s.token = ?', [login_token, ])[0]['token']
#   except IndexError:
#     return Response("Invalid loginToken, relog and try again!", mimetype="text/plain", status=404)
#   except:
#     return Response("Unkown error with loginToken!", mimetype="text/plain", status=404)

  # if(type(list(login_token)) is str):
  #   return dbh.exc_handler(login_token)

  # this makes me feel like I am doing so many things wrong in other places!
  removed_comment_like = dbh.run_query(
      "DELETE ch FROM comment_hot_cold ch INNER JOIN `session` s ON ch.user_id = s.user_id WHERE ch.comment_id = ? AND s.token = ?", [comment_id, login_token])

  if(type(removed_comment_like) is str):
    return dbh.exc_handler(removed_comment_like)

  if(removed_comment_like == 1):
    return Response(status=204)
  else:
    traceback.print_exc()
    return Response("Authorization Error!", mimetype='text/plain', status=403)
