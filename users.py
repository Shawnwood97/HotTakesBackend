from flask import request, Response
import dbh
import json
import traceback
from datetime import datetime
import secrets


def list_users():
  # set user_id using args.get so it's not mandatory.
  try:
    #! USE .args FOR GET!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    user_id = request.args.get('userId')
  except ValueError:
    return Response("NaN", mimetype="text/plain", status=422)
  except:
    traceback.print_exc()
    return Response("Error with id", mimetype="text/plain", status=400)

  # Base for SELECT query
  sql = "SELECT id, username, display_name, email, birthdate, first_name, last_name, headline, website_link, location, phone_number, is_verified, profile_pic_path, profile_banner_path, is_active, created_at FROM users"

  # Set params to empty list to use append later
  params = []

  # If user_id does not equal an empty stright and doesnt equal None, add to the end of the base query, and append user_id to params list
  if(user_id != None and user_id != ''):
    sql += " WHERE id = ?"
    params.append(user_id)

  users = dbh.run_query(sql, params)

  if(type(users) is str):
    return dbh.exc_handler(users)

#! changed this to be more resemble Alex' API now, to make it more plug n play with my tweeter project
  usersList = []
  for user in users:
    user_info = {
        'userId': user[0],
        'email': user[3],
        'username': user[1],
        'bio': user[7],
        'birthdate': user[4],
        'imageUrl': user[12],
        'bannerUrl': user[13]
    }
    usersList.append(user_info)
  users_json = json.dumps(usersList, default=str)
  return Response(users_json, mimetype='application/json', status=200)


def create_user():
  try:
    # Get all required inputs. #? Gotta decide If I want to allow all of the optional fields to be filled out on sign-up
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    bio = request.json['bio']
    # Get birthdate input then set ensure the format matches the database format.
    birthdate = request.json['birthdate']
    birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
  except ValueError:
    traceback.print_exc()
    return Response("Error: One or more of the inputs is invalid!", mimetype="text/plain", status=422)
  except KeyError:
    traceback.print_exc()
    return Response("Error: One or more required fields are empty!", mimetype="text/plain", status=422)
  except:
    traceback.print_exc()
    return Response("Error: Unknown error with an input!", mimetype="text/plain", status=400)

  # Query
  sql = "INSERT INTO users (username, email, password, headline, birthdate) VALUES (?,?,?,?,?)"
  # starting point for params to pass to run_query helper function
  params = [username, email, password, bio, birthdate]
  # params.extend((username, email, password, bio, birthdate))
  new_id = dbh.run_query(sql, params)

  if(type(new_id) is str):
    return dbh.exc_handler(new_id)

  # If newly created row == None, fail.
  if(new_id != None):
    # using 45 bytes, as that is well above the suggested 32 from the docs that says in 2015 was sufficient.
    login_token = secrets.token_urlsafe(45)
    sql = "INSERT INTO session (user_id, token) VALUES (?,?)"
    params = [new_id, login_token]
    ins_token = dbh.run_query(sql, params)

    if(type(ins_token) is str):
      return dbh.exc_handler(ins_token)

    new_user_json = json.dumps(
        {
            "userId": new_id,
            "email": email,
            "username": username,
            "bio": bio,
            "birthdate": birthdate,
            "loginToken": login_token
        }, default=str)
    return Response(new_user_json, mimetype="application/json", status=201)
  else:
    return Response("Failed to create user", mimetype="text/plain", status=400)


def update_user():
  try:
    # Get all required inputs. #? Gotta decide If I want to allow all of the optional fields to be filled out on sign-up
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
  except ValueError:
    traceback.print_exc()
    return Response("Error: One or more of the inputs is invalid!", mimetype="text/plain", status=422)
  except KeyError:
    traceback.print_exc()
    return Response("Error: One or more required fields are empty!", mimetype="text/plain", status=422)
  except:
    traceback.print_exc()
    return Response("Error: Unknown error with an input!", mimetype="text/plain", status=400)

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

  params.append(login_token)
  sql = sql[:-1]
  sql += " WHERE s.token = ?"

  update = dbh.run_query(sql, params)

  if(type(update) is str):
    return dbh.exc_handler(update)

#! Do I need this if block, in what case would the rowcount be 0??? Been trying to make it happen and can't
#! leaving it to be "defensive"
  if(update != 0):
    # ? Maybe I should build this while I build the UPDATE statement?
    updated_info = dbh.run_query(
        "SELECT u.id, username, email, headline, birthdate, profile_pic_path, profile_banner_path FROM users u INNER JOIN `session` s ON u.id = s.user_id WHERE s.token = ?", [login_token, ])
  else:
    traceback.print_exc()
    return Response("Failed to update", mimetype="text/plain", status=400)

  if(type(updated_info) is str):
    return dbh.exc_handler(updated_info)

#! also leaving this to be defensive!
  if(updated_info != None):
    updated_user = {
        "userId": updated_info[0][0],
        "email": updated_info[0][2],
        "username": updated_info[0][1],
        "bio": updated_info[0][3],
        "birthdate": updated_info[0][4],
        "imageUrl": updated_info[0][5],
        "bannerUrl": updated_info[0][6]
    }
    return Response(json.dumps(updated_user, default=str), mimetype="application/json", status=201)
  else:
    traceback.print_exc()
    return Response("Failed to update", mimetype="text/plain", status=400)

#! Would this work?!?!?!?!?
# ? sql = dbh.update_handler('users', ['username', 'email', 'headline', 'birthdate', 'profile_image_url', 'profile_banner_url', 'token'], [
# ?    username, email, bio, birthdate, image_url, banner_url])


def delete_user():
  # Get password and loginToken, both are required, nothing optional!
  try:
    password = request.json['password']
    token = request.json['loginToken']

  except ValueError:
    traceback.print_exc()
    return Response("Error: One or more of the inputs is invalid!", mimetype="text/plain", status=422)
  except KeyError:
    traceback.print_exc()
    return Response("Error: One or more required fields are empty!", mimetype="text/plain", status=422)
  except:
    traceback.print_exc()
    return Response("Error: Unknown error with an input!", mimetype="text/plain", status=400)

  deleted_user = 0

  # Inner join seemes apropriate here to validate info rather than using mutiple queries to compare.
  deleted_user = dbh.run_query(
      "DELETE u FROM users u INNER JOIN `session` s ON u.id = s.user_id WHERE u.password = ? AND s.token = ?", [password, token])

  if(type(deleted_user) is str):
    return dbh.exc_handler(deleted_user)

  #! I used fstring here to display "1 user deleted" doesn't seem particularly useful, will probably change!
  if(deleted_user == 1):
    return Response(f"{deleted_user} User Deleted!", mimetype="text/plain", status=200)
  else:
    return Response("Failed to delete user", mimetype="text/plain", status=400)
