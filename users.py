from flask import request, Response
import dbh
import json
import traceback
from datetime import datetime
import secrets


def list_users():
  # set user_id using args.get so it's not mandatory.

  parsed_args = dbh.input_handler(request.args,
                                  [
                                      {
                                          'required': False,
                                          'name': 'userId',
                                          'type': int
                                      }
                                  ]
                                  )
  if(parsed_args['success'] == False):
    return parsed_args['error']
  else:
    parsed_args = parsed_args['data']

  # Base for SELECT query
  sql = "SELECT id AS userId, username, display_name, email, birthdate, first_name, last_name, headline AS bio, website_link, location, phone_number, is_verified, profile_pic_path AS imageUrl, profile_banner_path AS bannerUrl, is_active, created_at FROM users"

  # Set params to empty list to use append later
  params = []

  if(parsed_args['userId'] != None and parsed_args['userId'] != ''):
    sql += " WHERE id = ?"
    params.append(parsed_args['userId'])

  users = dbh.run_query(sql, params)

  if(type(users) is str):
    return dbh.exc_handler(users)

  if(len(users) != 0):
    users_json = json.dumps(users, default=str)
    return Response(users_json, mimetype='application/json', status=200)
  else:
    return Response("User not found!", mimetype="text/plain", status=404)


def create_user():
  try:
    # Get all required inputs. #? Gotta decide If I want to allow all of the optional fields to be filled out on sign-up
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    bio = request.json['bio']
    # Get birthdate input then set ensure the format matches the database format.
    birthdate = request.json['birthdate']
    # set birthdate to proper format using datetime library
    birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
  except KeyError:
    traceback.print_exc()
    return Response("Missing required information!", mimetype="text/plain", status=422)
  except:
    traceback.print_exc()
    return Response("Unknown error with an input!", mimetype="text/plain", status=400)

  # Query
  sql = "INSERT INTO users (username, email, password, headline, birthdate) VALUES (?,?,?,?,?)"
  # starting point for params to pass to run_query helper function
  params = [username, email, password, bio, birthdate]

  for item in params:
    # this is speicifically to catch "", as it gets passed the KeyError from above
    if(item == ""):
      return Response("Missing required information!", mimetype="text/plain", status=422)

  new_id = dbh.run_query(sql, params)

  if(type(new_id) is str):
    return dbh.exc_handler(new_id)

  # using 45 bytes, as that is well above the suggested 32 from the docs that says in 2015 was sufficient.
  login_token = secrets.token_urlsafe(45)
  sql = "INSERT INTO session (user_id, token) VALUES (?,?)"
  params = [new_id, login_token]
  ins_token = dbh.run_query(sql, params)

  if(type(ins_token) is str):
    return dbh.exc_handler(ins_token)

  new_user_info = dbh.run_query(
      "SELECT u.id AS userId, u.email, u.username, u.headline AS bio, u.birthdate, s.token AS loginToken FROM users u INNER JOIN `session` s ON u.id = s.user_id WHERE u.id = ?", [new_id, ])
  new_user_json = json.dumps(new_user_info[0], default=str)
  return Response(new_user_json, mimetype="application/json", status=201)


def update_user():
  try:
    # Get any inputs to be updated
    username = request.json.get('username')
    email = request.json.get('email')
    bio = request.json.get('bio')
    # Get birthdate input then set ensure the format matches the database format.
    birthdate = request.json.get('birthdate')
    if(birthdate != None):
      birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
    image_url = request.json.get('imageUrl')
    banner_url = request.json.get('bannerUrl')
    login_token = request.json['loginToken']
  except KeyError:
    traceback.print_exc()
    return Response("One or more required fields are empty!", mimetype="text/plain", status=422)
  except:
    traceback.print_exc()
    return Response("Unknown error with an input!", mimetype="text/plain", status=400)

  # Base for update query
  # sql_s = "SELECT "
  sql = "UPDATE users u INNER JOIN `session` s ON u.id = s.user_id SET"
  # Starting point for valid params
  params = []

  # TODO I should be able to make a loop function for this.
  if(username != None and username != ''):
    sql += " u.username = ?,"
    params.append(username)
  if(email != None and email != ''):
    sql += " u.email = ?,"
    params.append(email)
  if(bio != None and bio != ''):
    sql += " u.headline = ?,"
    params.append(bio)
  if(birthdate != None and birthdate != ''):
    sql += " u.birthdate = ?,"
    params.append(birthdate)
  if(image_url != None and image_url != ''):
    sql += " u.profile_pic_path = ?,"
    params.append(image_url)
  if(banner_url != None and banner_url != ''):
    sql += " u.profile_banner_path = ?,"
    params.append(banner_url)

  # check to see if params were passed, mainly for good error catching!
  if(len(params) != 0):
    params.append(login_token)
    sql = sql[:-1]
    sql += " WHERE s.token = ?"
  else:
    return Response("No data passed!", mimetype="text/plain", status=400)

  updated_rows = dbh.run_query(sql, params)

  if(type(updated_rows) is str):
    return dbh.exc_handler(updated_rows)

  updated_user_info = dbh.run_query(
      "SELECT u.id AS userId, u.username, u.email, u.headline AS bio, u.birthdate, u.profile_pic_path AS imageUrl, u.profile_banner_path AS bannerUrl FROM users u INNER JOIN `session` s ON u.id = s.user_id WHERE s.token = ?", [login_token, ])

  if(type(updated_user_info) is str):
    return dbh.exc_handler(updated_user_info)

  # if the length of updated info does not = 1, error, else return data.
  # UPDATEs return rowcount
  if(len(updated_user_info) == 1):
    user_info_json = json.dumps(updated_user_info[0], default=str)
    return Response(user_info_json, mimetype="application/json", status=201)
  else:
    traceback.print_exc()
    return Response("Error getting user after update!", mimetype="text/plain", status=404)


def delete_user():
  # Get password and loginToken, both are required, nothing optional!
  try:
    password = request.json['password']
    token = request.json['loginToken']

  except KeyError:
    traceback.print_exc()
    return Response("Error: One or more required fields are empty!", mimetype="text/plain", status=422)
  except:
    traceback.print_exc()
    return Response("Error: Unknown error with an input!", mimetype="text/plain", status=400)

  # Inner join seemes apropriate here to validate info rather than using mutiple queries to compare.
  deleted_user = dbh.run_query(
      "DELETE u FROM users u INNER JOIN `session` s ON u.id = s.user_id WHERE u.password = ? AND s.token = ?", [password, token])

  if(type(deleted_user) is str):
    return dbh.exc_handler(deleted_user)

  # just return status if true, 403 if false
  if(deleted_user == 1):
    return Response(status=204)
  else:
    return Response("Authorization Error!", mimetype="text/plain", status=403)
