from flask import request, Response
import dbh
import json


def list_trends():
  # optional tagId can be passed to show just 1 hashtag
  arg_scheme = [
      {
          'required': False,
          'name': 'hashtag',
          'type': str
      }
  ]
  parsed_args = dbh.input_handler(request.args, arg_scheme)
  if(parsed_args['success'] == False):
    return parsed_args['error']
  else:
    parsed_args = parsed_args['data']

  # base query for SELECTing hashtags and counting how many times each was used.
  sql = "SELECT h.hashtag, COUNT(h.hashtag) AS times_used FROM hashtags h"

  params = []

  # if user passed a hashtag, change sql statement so it returns a list of all takes and users that used the hashtag. otherwise show trends.
  # ? this could potentially be 2 seperate endpoints, maybe, works for now.
  # we could sort by h.id or by created_at on the front end for sorting in different ways if we want to.
  if(parsed_args.get('hashtag') != None and parsed_args.get('hashtag') != ''):
    sql = "SELECT h.id, h.hashtag, h.user_id, h.take_id, h.created_at FROM hashtags h WHERE h.hashtag = ?"
    params.append(parsed_args['hashtag'])
  else:
    sql += " GROUP BY h.hashtag"

  result = dbh.run_query(sql, params)

  if(result['success'] == False):
    return result['error']

  # if len of data is not 0, return json, otherwise error.
  if(len(result['data']) != 0):
    tags_json = json.dumps(result['data'], default=str)
    return Response(tags_json, mimetype='application/json', status=200)
  else:
    return Response("Hashtag not found!", mimetype="text/plain", status=404)
