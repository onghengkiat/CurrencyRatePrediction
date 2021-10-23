from flask import make_response, jsonify, session, request
from app import app
from functools import wraps

def missing_param_handler(func):
    """
    Wrapper to return error messages for key error on unpackaging requests

    Pre:
        None
    Post:
        except TypeError:
            return make_response(jsonify({'message':'Malformed request, missing json'})),400
        except KeyError:
            return make_response(jsonify({'message':'Malformed request, missing parameters'})),400
    """
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TypeError:
            return make_response(jsonify({'message':'Malformed request, missing json'})), 400
        except KeyError:
            return make_response(jsonify({'message':'Malformed request, missing parameters'})), 400
    return inner

def build_preflight_response():
    # to be used in development
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin","*")
    response.headers.add("Access-Control-Allow-Headers","*")
    response.headers.add("Access-Control-Allow-Methods","*")
    return response

def cors_allow(func):
    """
    Wrapper to allows CORS
    """
    @wraps(func)
    def wrapped(*args,**kwargs):
        # to be used in development
        if request.method == 'OPTIONS':
            return build_preflight_response()
        response = func(*args,**kwargs)
        response = make_response(response)
        response.headers.add("Access-Control-Allow-Origin","*")
        return response
    return wrapped


