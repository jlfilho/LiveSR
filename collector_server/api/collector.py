# -*- coding: utf-8 -*-
import json

from flask_restful import Resource, Api
from flask import make_response
from flask_cors import CORS
import logging


def output_json(obj, code, headers=None):

    resp = make_response(json.dumps(obj), code)
    resp.headers.extend(headers or {})
    return resp


def create_api(app):

    DEFAULT_REPRESENTATIONS = {'application/json': output_json}
    
    app.config['CORS_HEADERS'] = "Content-Type"
    CORS(app)
        
    api = Api(app)
    
    api.representations = DEFAULT_REPRESENTATIONS

    logging.getLogger('flask_cors').level = logging.DEBUG
    

    #Registrando os Blueprints
    from api.resources.logs import metrics_blue, LogsResource, Index, GeneralResource
    app.register_blueprint(metrics_blue)

    #Registrando os recursos
    api.add_resource(Index, '/')
    api.add_resource(LogsResource, '/metrics')
    api.add_resource(GeneralResource, '/general')

    return app