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



