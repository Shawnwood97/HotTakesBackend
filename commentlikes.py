from flask import request, Response
import dbh
import json
import traceback


def add_comment_like():
  try:
    # get required inputs.
    login_token = request.json['loginToken']
    comment_id = int(request.json['commentId'])
    # basic error checking.
    if(comment_id <= 0):
      return Response("Invalid commentId", mimetype="text/plain", status=422)
    if(login_token == ''):
      return Response("Required fields cannot be empty strings", mimetype="text/plain", status=422)
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
  result = dbh.run_query("SELECT s.user_id FROM `session` s WHERE token = ?", [
      login_token, ])

  try:
    user_id = result['data'][0]['user_id']
  except:
    return Response("Authorization error!", mimetype="text/plain", status=403)

  if(result['success'] == False):
    return result['error']

  # SQL statement to create the like
  like_sql = "INSERT INTO comment_hot_cold (comment_id, user_id) VALUES (?,?)"

  # set the like id to a variable, #todo we can refactor this whole function later.
  like_id = dbh.run_query(
      like_sql, [comment_id, user_id])

  if(like_id['success'] == False):
    return like_id['error']

  # if like id is 0 or higher, return status 204 (no content), added else just for safety
  if(like_id['data'] > -1):
    return Response(status=204)
  else:
    # maybe not the right error code. #todo look more into this later.
    return Response("Error liking comment.", mimetype="text/plain", status=403)


def list_comment_likes():
    # set user_id using args because it is a get request
  try:
    comment_id = request.args.get('commentId')
    if(comment_id != None and comment_id != ''):
      comment_id = int(comment_id)
      # basic error checking same as most other functions.
      if(comment_id <= 0):
        return Response("Invalid commentId", mimetype="text/plain", status=422)
  except ValueError:
    return Response("NaN", mimetype="text/plain", status=422)
  except KeyError:
    return Response("No commentId Sent", mimetype="text/plain", status=400)
  except:
    traceback.print_exc()
    return Response("Unknown Error with commentId", mimetype="text/plain", status=400)

  # base sql statement
  sql = "SELECT ch.comment_id AS commentId, ch.user_id AS userId, u.username FROM comment_hot_cold ch INNER JOIN users u ON ch.user_id = u.id"

  # init params as empty list.
  params = []

  # defensive, if comment id is not None and not an empty string append to params and add to sql statement.
  if(comment_id != None and comment_id != ''):
    sql += ' WHERE ch.comment_id = ?'
    params.append(comment_id)

  # run the query, store the result in liked_comments.
  liked_comments = dbh.run_query(sql, params)

  # check if it succeeded.
  if(liked_comments['success'] == False):
    return liked_comments['error']

  liked_comments_json = json.dumps(liked_comments['data'], default=str)
  return Response(liked_comments_json, mimetype='application/json', status=200)


def remove_comment_like():
  try:
    login_token = request.json['loginToken']
    comment_id = int(request.json['commentId'])

    if(comment_id <= 0):
      return Response("Invalid commentId", mimetype="text/plain", status=422)
    if(login_token == ''):
      return Response("Required fields cannot be empty strings", mimetype="text/plain", status=422)
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
  removed_comment_like = dbh.run_query(
      "DELETE ch FROM comment_hot_cold ch INNER JOIN `session` s ON ch.user_id = s.user_id WHERE ch.comment_id = ? AND s.token = ?", [comment_id, login_token])

  if(removed_comment_like['success'] == False):
    return removed_comment_like['error']

  if(removed_comment_like['data'] == 1):
    return Response(status=204)
  else:
    traceback.print_exc()
    return Response("Authorization Error!", mimetype='text/plain', status=403)
