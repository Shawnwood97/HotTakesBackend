import mariadb
import dbconn
import traceback
from flask import Flask, request, Response

#! starting to think building my own responses instread of the loop may be better


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
  result = None
  conn = dbconn.open_connection()
  cursor = dbconn.create_cursor(conn)
  try:
    cursor.execute(sql, params)
    if(sql.startswith('SELECT')):
      data = cursor.fetchall()
      result = loop_items(cursor, data)
    elif(sql.startswith('INSERT')):
      conn.commit()
      result = cursor.lastrowid
    elif(sql.startswith('UPDATE') or sql.startswith('DELETE')):
      conn.commit()
      result = cursor.rowcount
    else:
      result = "405"

  except mariadb.InternalError:
    result = "500"
    traceback.print_exc()
  except mariadb.IntegrityError:
    result = "409"
    traceback.print_exc()
  except mariadb.DataError:
    result = "500"
    traceback.print_exc()
  except:
    result = "500"
    traceback.print_exc()

  dbconn.close_all(conn, cursor)

  return result


def exc_handler(query):
  # exception handler function that takes the result of the run_query function and returns the proper response.
  if(query == "405"):
    return Response("Error: Method Not Allowed!", mimetype="text/plain", status=int(query))
  elif(query == "409"):
    return Response("Error: Possible duplicate data or foreign key conflict!", mimetype="text/plain", status=int(query))
  else:
    traceback.print_exc()
    return Response("Internal Server Error, Please try again later!", mimetype="text/plain", status=500)


# def update_handler(cols, rows, params):
#   sql = "UPDATE " + str(cols) + " SET"
#   for row, col in rows, cols:
#     if(row != None and row != ''):
#       sql += str(col) + "= ?,"
#   return sql
