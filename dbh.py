import mariadb
import dbconn
import traceback
from flask import Response


def loop_items(cursor, rows):
  # Takes column headers from cursor.description, zips them to the rows returned by a query based on index position, into a dictionary for a more
  # readable return.
  headers = [i[0] for i in cursor.description]
  result = []
  for row in rows:
    result.append(dict(zip(headers, row)))
  return result


def run_query(sql, params=[]):
  # This function will run all of the queries, keeping it DRY, params starts as an empty list because we don't always need them.
  # data = None  # Where data that we want to loop through before returning will be stored
  # Where data that we want to return will be stored, post loop or no loop required.
  result = {
      'success': True,
      'error': None,
      'data': None
  }
  conn = dbconn.open_connection()
  cursor = dbconn.create_cursor(conn)
  try:
    cursor.execute(sql, params)
    if(sql.startswith('SELECT')):
      data = cursor.fetchall()
      result['data'] = loop_items(cursor, data)
    elif(sql.startswith('INSERT')):
      conn.commit()
      result['data'] = cursor.lastrowid
    elif(sql.startswith('UPDATE') or sql.startswith('DELETE')):
      conn.commit()
      result['data'] = cursor.rowcount
    else:
      result['success'] = False
      result['error'] = Response(
          "Error: Method Not Allowed!", mimetype="text/plain", status=405)

  except mariadb.InternalError:
    result['success'] = False
    result['error'] = Response(
        "Internal Server Error, Please try again later!", mimetype="text/plain", status=500)
    traceback.print_exc()
  except mariadb.IntegrityError:
    result['success'] = False
    result['error'] = Response(
        "Error: Possible duplicate data or foreign key conflict!", mimetype="text/plain", status=409)
    traceback.print_exc()
  except mariadb.DataError:
    result['success'] = False
    result['error'] = Response(
        "Internal Server Error, Please try again later!", mimetype="text/plain", status=500)
    traceback.print_exc()
  except:
    result['success'] = False
    result['error'] = Response(
        "Internal Server Error, Please try again later!", mimetype="text/plain", status=500)
    traceback.print_exc()

  dbconn.close_all(conn, cursor)

  return result

# !delete lat
# def exc_handler(query):
#   # exception handler function that takes the result of the run_query function and returns the proper response.
#   if(query == "405"):
#     return Response("Error: Method Not Allowed!", mimetype="text/plain", status=int(query))
#   elif(query == "409"):
#     return Response("Error: Possible duplicate data or foreign key conflict!", mimetype="text/plain", status=int(query))
#   else:
#     traceback.print_exc()
#     return Response("Internal Server Error, Please try again later!", mimetype="text/plain", status=500)


def input_handler(data, u_inputs=[]):
  '''?
  u_inputs should be a list of dicts
  ie. 
  [
    {
      required: True,
      name: var_name,
      type: str
    },
    {
      required: True,
      name: var_name,
      type: str
    }
  ]
  '''
  payload = {
      'success': True,
      'error': None,
      'data': {}
  }
  for u_input in u_inputs:
    try:
      if(u_input['required'] == True):
        payload['data'][u_input['name']] = u_input['type'](
            data[u_input['name']])
      else:
        if(data.get(u_input['name']) != None and data.get(u_input['name']) != ''):
          payload['data'][u_input['name']] = u_input['type'](
              data[u_input['name']])
    except ValueError:
      traceback.print_exc()
      payload['success'] = False
      payload['error'] = Response(
          f"Error: {u_input['name']} is invalid!", mimetype="text/plain", status=422)
    except KeyError:
      traceback.print_exc()
      payload['success'] = False
      payload['error'] = Response(
          f"Error: Required field {u_input['name']} is empty!", mimetype="text/plain", status=422)
    except:
      traceback.print_exc()
      payload['success'] = False
      payload['error'] = Response(
          f"Error: Unknown data error with {u_input['name']}", mimetype="text/plain", status=400)

    return payload
