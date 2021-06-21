from flask import Flask, request, Response
import dbh
import json
import traceback
import sys
import mariadb
import users
import login

app = Flask(__name__)


# ? --------------------------------------------------------
# ? --------------------- GET REQUESTS ---------------------
# ? --------------------------------------------------------


@app.get('/api/users')
def call_list_users():
  return users.list_users()


# * --------------------------------------------------------
# * -------------------- POST REQUESTS ---------------------
# * --------------------------------------------------------

@app.post('/api/users')
def call_create_user():
  return users.create_user()


@app.post('/api/login')
def call_login_user():
  return login.login_user()

# ? --------------------------------------------------------
# ? -------------------- PATCH REQUESTS --------------------
# ? --------------------------------------------------------


@app.patch('/api/users')
def call_update_user():
  return users.update_user()

# ! --------------------------------------------------------
# ! -------------------- DELETE REQUESTS -------------------
# ! --------------------------------------------------------


@app.delete('/api/users')
def call_delete_user():
  return users.delete_user()


if(len(sys.argv) > 1):
  mode = sys.argv[1]
else:
  print("No mode argument, please pass a mode argument when invoking the file!")
  exit()

if(mode == "prod"):
  import bjoern  # type: ignore
  bjoern.run(app, "0.0.0.0", 5015)
elif(mode == "test"):
  from flask_cors import CORS
  CORS(app)
  app.run(debug=True)
else:
  print("Invalid mode, please select either 'prod' or 'test'")
  exit()
