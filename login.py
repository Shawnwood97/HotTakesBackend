from flask import request, Response
import dbh
import json
import traceback
from datetime import datetime
import secrets


def login_user():
  try:
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json['password']
  except ValueError:
    traceback.print_exc()
    return Response("Error: One or more of the inputs is invalid!", mimetype="text/plain", status=422)
  except KeyError:
    traceback.print_exc()
    return Response("Error: One or more required fields are empty!", mimetype="text/plain", status=422)
  except:
    traceback.print_exc()
    return Response("Error: Unknown error with an input!", mimetype="text/plain", status=400)

  # create query depending on condition, this should work decently well as a condition. #? I think?

  sql = "SELECT id FROM users WHERE password = ? AND"

  params = [password]

  if(username != None and username != ''):
    sql += " username = ?"
    params.append(username)
  elif(email != None and email != ''):
    sql += " email = ?"
    params.append(email)

  result = dbh.run_query(sql, params)

  if(result['success'] == False):
    return result['error']

  row_id = -1

  if(len(result['data']) == 1):
    login_token = secrets.token_urlsafe(45)
    # insert query for creating a token
    sql_ins = "INSERT INTO session (token, user_id) VALUES (?,?)"
    # params for insert query
    params_ins = [login_token, result['data'][0]["id"]]
    result = dbh.run_query(sql_ins, params_ins)

    if(result['success'] == False):
      return result['error']

  else:
    return Response("Invalid Authentication", mimetype="text/plain", status=403)

  login_info = dbh.run_query(
      "SELECT u.id AS userId, username, email, headline, birthdate, profile_pic_path, profile_banner_path FROM users u INNER JOIN `session` s ON u.id = s.user_id WHERE s.token = ?", [login_token, ])

  if(login_info['success'] == False):
    return login_info['error']

  # this feels better than using double indexing ie. 'userId': login_info[0][0]
  # Add login token to the dict for returning to user!
  login_info['data'][0].update({'loginToken': login_token})
  updated_login_json = json.dumps(login_info['data'][0], default=str)
  return Response(updated_login_json, mimetype="application/json", status=201)


def logout_user():
  try:
    login_token = request.json['loginToken']
  except KeyError:
    traceback.print_exc()
    return Response("Error: One or more required fields are empty!", mimetype="text/plain", status=422)
  except:
    traceback.print_exc()
    return Response("Error: Unknown error with an input!", mimetype="text/plain", status=400)

  # Inner join seemes apropriate here to validate info rather than using mutiple queries to compare.
  result = dbh.run_query(
      "DELETE s FROM `session` s WHERE s.token = ?", [login_token, ])

  if(result['success'] == False):
    return result['error']

  if(result['data'] == 1):
    # only a status response, no other data!
    return Response(status=204)
  else:
    return Response("Error logging out!", mimetype="text/plain", status=403)
