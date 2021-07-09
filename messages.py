from flask import request, Response
import dbh
import json
import traceback

# ? do I need a conversations endpoint???!?!?


def list_sent_messages():
  arg_scheme = [
      {
          'required': True,
          'name': 'loginToken',
          'type': str
      }
  ]
  parsed_args = dbh.input_handler(request.args, arg_scheme)
  if(parsed_args['success'] == False):
    return parsed_args['error']
  else:
    parsed_args = parsed_args['data']

  #! I want usernames and profile images here as well, but we can get them per conversation rather than per message to make more efficient.
  # todo make a seperate endpoints for listing sent and recieved so we can have seperate inboxes on front end and make querys nicer.
  sql = "SELECT m.from_user_id, m.to_user_id, m.content, m.created_at FROM messages m INNER JOIN `session` s ON m.from_user_id = s.user_id WHERE s.token = ?"

  result = dbh.run_query(sql, [parsed_args['loginToken'], ])

  if(result['success'] == False):
    return result['error']

  if(len(result['data']) != 0):
    messages_json = json.dumps(result['data'], default=str)
    return Response(messages_json, mimetype='application/json', status=200)
  else:
    return Response("Messages not found!", mimetype="text/plain", status=404)


def list_recieved_messages():
  arg_scheme = [
      {
          'required': True,
          'name': 'loginToken',
          'type': str
      }
  ]
  parsed_args = dbh.input_handler(request.args, arg_scheme)
  if(parsed_args['success'] == False):
    return parsed_args['error']
  else:
    parsed_args = parsed_args['data']

  #! I want usernames and profile images here as well, but we can get them per conversation rather than per message to make more efficient.
  sql = "SELECT m.from_user_id, m.to_user_id, m.content, m.created_at FROM messages m INNER JOIN `session` s ON m.to_user_id = s.user_id WHERE s.token = ?"

  result = dbh.run_query(sql, [parsed_args['loginToken'], ])

  if(result['success'] == False):
    return result['error']

  if(len(result['data']) != 0):
    messages_json = json.dumps(result['data'], default=str)
    return Response(messages_json, mimetype='application/json', status=200)
  else:
    return Response("Messages not found!", mimetype="text/plain", status=404)


def send_message():
  arg_scheme = [
      {
          'required': True,
          'name': 'loginToken',
          'type': str
      },
      {
          'required': True,
          'name': 'userId',
          'type': int
      },
      {
          'required': True,
          'name': 'content',
          'type': str
      }
  ]
  parsed_args = dbh.input_handler(request.json, arg_scheme)
  if(parsed_args['success'] == False):
    return parsed_args['error']
  else:
    parsed_args = parsed_args['data']

  user_sql = "SELECT user_id FROM `session` WHERE token = ?"

  result = dbh.run_query(user_sql, [parsed_args['loginToken'], ])

  if(result['success'] == False):
    return result['error']

  from_user_id = result['data'][0]['user_id']

  message_sql = "INSERT INTO messages (from_user_id, to_user_id, content) VALUES (?,?,?)"

  # todo append a created to this to save the select statement at the end.
  message_result = dbh.run_query(
      message_sql, [from_user_id, parsed_args['userId'], parsed_args['content']])

  if(message_result['success'] == False):
    return message_result['error']
  else:
    # todo, we can probably make this a little better since we have all the info except for the created_at from previous queries, but this gets the job done for now!
    message_data = dbh.run_query(
        "SELECT m.id, m.from_user_id, m.to_user_id, m.content, m.created_at FROM messages m WHERE m.id = ?", [message_result['data'], ])
    if(message_data['success'] == False):
      return message_result['error']
    new_message_json = json.dumps(message_data['data'][0], default=str)
    return Response(new_message_json, mimetype="application/json", status=201)

#! I personally don't think I would want the ability to edit messages, so I'm leaving that functionality out for now, this should be good for general messaging functionality!

# todo add a column called is_read later in order to have read/unread functionality!


def delete_message():
  arg_scheme = [
      {
          'required': True,
          'name': 'loginToken',
          'type': str
      },
      {
          'required': True,
          'name': 'messageId',
          'type': int
      }
  ]
  parsed_args = dbh.input_handler(request.json, arg_scheme)
  if(parsed_args['success'] == False):
    return parsed_args['error']
  else:
    parsed_args = parsed_args['data']

  result = dbh.run_query(
      "DELETE m FROM messages m INNER JOIN `session` s ON m.from_user_id = s.user_id WHERE m.id = ? AND s.token = ?", [parsed_args['messageId'], parsed_args['loginToken']])

  if(result['success'] == False):
    return result['error']

  if(result['data'] == 1):
    return Response(status=204)
  else:
    traceback.print_exc()
    return Response("Authorization Error", mimetype='text/plain', status=403)
