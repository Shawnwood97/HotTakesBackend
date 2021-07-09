from flask import request, Response
import dbh
import json
import traceback
import secrets
import hashlib


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
  # SQL base statement
  sql = "SELECT id FROM users"

  # empty list starting point for params.
  params = []

  # if username or email is not None or an empty string, add it to the end of the sql string, elif because only one should be true.
  # also append it to params for prepared statement.
  if(username != None and username != ''):
    sql += " WHERE username = ? AND"
    params.append(username)
    identity = username
  elif(email != None and email != ''):
    sql += " WHERE email = ? AND"
    params.append(email)
    identity = email

  # add password to the where clause in our sql statement
  sql += " password = ?"

  # get salt from DB, add it before password and hash it
  salt = dbh.get_salt(identity)
  password = salt + password
  password = hashlib.sha512(password.encode()).hexdigest()

  # append salted, hashed password to params for prepared statement
  params.append(password)

  # run sql query
  result = dbh.run_query(sql, params)

  if(result['success'] == False):
    return result['error']

  # if the length of the data list in result is equal to 1, create the login token and insert it
  if(len(result['data']) == 1):
    login_token = secrets.token_urlsafe(45)
    # insert query for creating a token
    sql_ins = "INSERT INTO session (token, user_id) VALUES (?,?)"
    # params for insert query
    params_ins = [login_token, result['data'][0]["id"]]
    result = dbh.run_query(sql_ins, params_ins)

    if(result['success'] == False):
      return result['error']
  # auth error if the data dictionary as no, or too many objects inside. Should never be more, most likely will be 1 or 0.
  else:
    return Response("Invalid Authentication", mimetype="text/plain", status=403)

  # Select statement for returning data.
  login_info = dbh.run_query(
      "SELECT u.id AS userId, username, email, headline, birthdate, profile_pic_path, profile_banner_path FROM users u INNER JOIN `session` s ON u.id = s.user_id WHERE s.token = ?", [login_token, ])

  if(login_info['success'] == False):
    return login_info['error']

  # if login info data list has a length of 1, create the json return, else error.
  if(len(login_info['data']) == 1):
    # add login token into the first index in the data dict for API return purposes.
    login_info['data'][0].update({'loginToken': login_token})
    updated_login_json = json.dumps(login_info['data'][0], default=str)
    return Response(updated_login_json, mimetype="application/json", status=201)
  else:
    return Response("Error getting user info after insert!", mimetype="text/plain", status=404)


def logout_user():
  try:
    login_token = request.json['loginToken']
    if(login_token == ''):
      return Response("Required fields cannot be empty strings", mimetype="text/plain", status=422)
  except KeyError:
    traceback.print_exc()
    return Response("Error: One or more required fields are empty!", mimetype="text/plain", status=422)
  except:
    traceback.print_exc()
    return Response("Error: Unknown error with an input!", mimetype="text/plain", status=400)

  # result will be the rowcount = the number of rows deleted, should only ever be 1 when successful
  result = dbh.run_query(
      "DELETE s FROM `session` s WHERE s.token = ?", [login_token, ])

  if(result['success'] == False):
    return result['error']

  # if the data (rowcount) is equal to 1, return 204 response (no content), else error.
  if(result['data'] == 1):
    # only a status response, no other data!
    return Response(status=204)
  else:
    return Response("Error logging out!", mimetype="text/plain", status=403)
