from flask import request, Response
import dbh
import json
import traceback
from datetime import datetime
import secrets


def login_user():
  try:
    username_email = request.json['usernameEmail']
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
  if("@" in username_email and "." in username_email):
    sql = "SELECT id FROM users WHERE email = ? AND password = ?"
  else:
    sql = "SELECT id FROM users WHERE username = ? AND password = ?"

  params = [username_email, password]

  user = dbh.run_query(sql, params)

  if(type(user) is str):
    return dbh.exc_handler(user)

  if(len(user) == 1):
    login_token = secrets.token_urlsafe(45)
    # insert query for creating a token
    sql_ins = "INSERT INTO session (token, user_id) VALUES (?,?)"
    # params for insert query
    params_ins = [login_token, user[0][0]]
    row_id = dbh.run_query(sql_ins, params_ins)

  if(row_id != -1):
    login_info = dbh.run_query(
        "SELECT u.id, username, email, headline, birthdate, profile_pic_path, profile_banner_path FROM users u INNER JOIN `session` s ON u.id = s.user_id WHERE s.token = ?", [login_token, ])
    print(login_info)
  else:
    traceback.print_exc()
    return Response("Failed to update", mimetype="text/plain", status=400)

  if(type(login_info) is str):
    return dbh.exc_handler(login_info)

  if(login_info != None):
    # this feels better than using double indexing ie. 'userId': login_info[0][0]
    for col in login_info:
      updated_login_json = json.dumps(
          {
              'userId': col[0],
              'email': col[2],
              'username': col[1],
              'bio': col[3],
              'birthdate': col[4],
              'imageUrl': col[5],
              'bannerUrl': col[6],
              'loginToken': login_token
          }, default=str)
    return Response(updated_login_json, mimetype="application/json", status=201)
  else:
    traceback.print_exc()
    return Response("Failed to update", mimetype="text/plain", status=400)


def logout_user():
  try:
    login_token = request.json['loginToken']
  except ValueError:
    traceback.print_exc()
    return Response("Error: One or more of the inputs is invalid!", mimetype="text/plain", status=422)
  except KeyError:
    traceback.print_exc()
    return Response("Error: One or more required fields are empty!", mimetype="text/plain", status=422)
  except:
    traceback.print_exc()
    return Response("Error: Unknown error with an input!", mimetype="text/plain", status=400)

  deleted_token = 0

  # Inner join seemes apropriate here to validate info rather than using mutiple queries to compare.
  deleted_token = dbh.run_query(
      "DELETE s FROM `session` s WHERE s.token = ?", [login_token, ])

  if(type(deleted_token) is str):
    return dbh.exc_handler(deleted_token)

  #! Same thing with the token as the deleted user from before!
  if(deleted_token == 1):
    return Response(f"{deleted_token} Token Deleted!", mimetype="text/plain", status=200)
  else:
    return Response("Failed to logout user, likely invalid token", mimetype="text/plain", status=400)
