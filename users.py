from threading import current_thread
from flask import Flask, request, Response
import dbh
import json
import traceback
import sys
import mariadb
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

  users_json = json.dumps(users, default=str)
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

  # If newly created row == -1, fail.
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
