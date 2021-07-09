from flask import request, Response
import dbh
import json
import traceback
from datetime import datetime
import secrets
import hashlib


def list_users():
  # set user_id using args.get so it's not mandatory.
  arg_scheme = [
      {
          'required': False,
          'name': 'userId',
          'type': int
      }
  ]
  parsed_args = dbh.input_handler(request.args, arg_scheme)
  if(parsed_args['success'] == False):
    return parsed_args['error']
  else:
    parsed_args = parsed_args['data']

  # Base for SELECT query
  sql = "SELECT id AS userId, username, display_name, email, birthdate, first_name, last_name, headline AS bio, website_link, location, phone_number, is_verified, profile_pic_path AS imageUrl, profile_banner_path AS bannerUrl, is_active, created_at FROM users"

  # Set params to empty list to use append later
  params = []

  if(parsed_args.get('userId') != None and parsed_args.get('userId') != ''):
    sql += " WHERE id = ?"
    params.append(parsed_args['userId'])

  result = dbh.run_query(sql, params)

  if(result['success'] == False):
    return result['error']

  if(len(result['data']) != 0):
    users_json = json.dumps(result['data'], default=str)
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

  # create salt, add it before the password, hash it, and add both to the sql query later to be added to db.
  salt = dbh.create_salt()
  password = salt + password
  password = hashlib.sha512(password.encode()).hexdigest()

  # Query
  sql = "INSERT INTO users (username, email, password, headline, birthdate, salt) VALUES (?,?,?,?,?,?)"
  # starting point for params to pass to run_query helper function
  params = [username, email, password, bio, birthdate, salt]

  for item in params:
    # this is speicifically to catch "", as it gets passed the KeyError from above
    if(item == ""):
      return Response("Missing required information!", mimetype="text/plain", status=422)

  result = dbh.run_query(sql, params)

  if(result['success'] == False):
    return result['error']

  # using 45 bytes, as that is well above the suggested 32 from the docs that says in 2015 was sufficient.
  login_token = secrets.token_urlsafe(45)
  sql = "INSERT INTO session (user_id, token) VALUES (?,?)"
  params = [result['data'], login_token]
  result_token = dbh.run_query(sql, params)

  if(result_token['success'] == False):
    return result_token['error']

# todo dont need this select, I have all data from above! refactor
  new_user_result = dbh.run_query(
      "SELECT u.id AS userId, u.email, u.username, u.headline AS bio, u.birthdate, s.token AS loginToken FROM users u INNER JOIN `session` s ON u.id = s.user_id WHERE u.id = ?", [result['data'], ])

  if(new_user_result['success'] == False):
    return new_user_result['error']

  new_user_json = json.dumps(new_user_result['data'][0], default=str)
  return Response(new_user_json, mimetype="application/json", status=201)


def update_user():
  # inputs to be passed to helper function, we can probably move these into their own file and make them more reusable rather than creating all these lines here.
  # see dbh => input_handler for explanation
  arg_scheme = [
      {
          'required': True,
          'name': 'loginToken',
          'type': str
      },
      {
          'required': False,
          'name': 'username',
          'type': str
      },
      {
          'required': False,
          'name': 'email',
          'type': str
      },
      {
          'required': False,
          'name': 'bio',
          'type': str
      },
      {
          'required': False,
          'name': 'birthdate',
          'type': str
      },
      {
          'required': False,
          'name': 'imageUrl',
          'type': str
      },
      {
          'required': False,
          'name': 'bannerUrl',
          'type': str
      },
  ]
  # setting parsed_args as the return of the input_handler function, passing request.json as out endpoint_arg, and the scheme from above as u_inputs.
  # parsed args will be a dictionary
  parsed_args = dbh.input_handler(request.json, arg_scheme)
  # if the key success has a False value, rerutn the error from the error key.
  if(parsed_args['success'] == False):
    return parsed_args['error']
  else:
    # else set parsed args to the data dictionary that is within the input handler returned dictionary.
    parsed_args = parsed_args['data']

  # if birthdate exists, set it to the proper date format for the database using datetime library
  if(parsed_args.get('birthdate') != None):
    parsed_args['birthdate'] = datetime.strptime(
        parsed_args['birthdate'], "%Y-%m-%d")

  # Base for update query
  sql = "UPDATE users u INNER JOIN `session` s ON u.id = s.user_id SET"
  # Starting point for params
  params = []

  # TODO I should be able to make a loop function for this.
  # check each of the inputs and if they are not None or empty strings, append them to params list from above.
  if(parsed_args.get('username') != None and parsed_args.get('username') != ''):
    sql += " u.username = ?,"
    params.append(parsed_args['username'])
  if(parsed_args.get('email') != None and parsed_args.get('email') != ''):
    sql += " u.email = ?,"
    params.append(parsed_args['email'])
  if(parsed_args.get('bio') != None and parsed_args.get('bio') != ''):
    sql += " u.headline = ?,"
    params.append(parsed_args['bio'])
  if(parsed_args.get('birthdate') != None and parsed_args.get('birthdate') != ''):
    sql += " u.birthdate = ?,"
    params.append(parsed_args['birthdate'])
  if(parsed_args.get('imageUrl') != None and parsed_args.get('imageUrl') != ''):
    sql += " u.profile_pic_path = ?,"
    params.append(parsed_args['imageUrl'])
  if(parsed_args.get('bannerUrl') != None and parsed_args.get('bannerUrl') != ''):
    sql += " u.profile_banner_path = ?,"
    params.append(parsed_args['bannerUrl'])

  # check to see if any optional data was passed, if it was, remove the comma using slice, append the loginToken to the params and add the WHERE clause to
  # the sql statement, else return no data passed response.
  if(len(params) != 0):
    params.append(parsed_args['loginToken'])
    sql = sql[:-1]
    sql += " WHERE s.token = ?"
  else:
    return Response("No data passed!", mimetype="text/plain", status=400)

  # set the result of the run_query function to the result variable.
  result = dbh.run_query(sql, params)

  # if the success key is False, return the error keys value which is a Response.
  if(result['success'] == False):
    return result['error']

  # if the data key is has a value of 0 or lower, return an authentication error, seems appropriate since we are returning rowcount with updates.
  if(result['data'] <= 0):
    return Response("Authentication Error!", mimetype="text/plain", status=403)

  # Select query to get all the info after updating.
  updated_user_info = dbh.run_query(
      "SELECT u.id AS userId, u.username, u.email, u.headline AS bio, u.birthdate, u.website_link, u.created_at, u.profile_pic_path AS imageUrl, u.profile_banner_path AS bannerUrl FROM users u INNER JOIN `session` s ON u.id = s.user_id WHERE s.token = ?", [parsed_args['loginToken'], ])

  # if the success key is False, return the error keys value which is a Response.
  if(updated_user_info['success'] == False):
    return updated_user_info['error']

  # if the length of the data key equals 1, set user_info_json to the data key at the 0 index, which will be the dict of key value pairs returned from the loop_items function
  # in dbh, else, error.
  if(len(updated_user_info['data']) == 1):
    user_info_json = json.dumps(updated_user_info['data'][0], default=str)
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
  result = dbh.run_query(
      "DELETE u FROM users u INNER JOIN `session` s ON u.id = s.user_id WHERE u.password = ? AND s.token = ?", [password, token])

  if(result['success'] == False):
    return result['error']

  # just return status if true, 403 if false
  if(result['data'] == 1):
    return Response(status=204)
  else:
    return Response("Authentication Error!", mimetype="text/plain", status=403)
