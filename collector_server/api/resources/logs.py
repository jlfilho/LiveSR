
# coding: utf-8
import json
import time
import os
import signal

from flask import Blueprint, request, Response
from flask_restful import Resource, reqparse

from flask_cors import CORS,cross_origin



SUMMARY_DIR = '/usr/src/api/results-collector'

metrics_blue = Blueprint('logging', __name__)

class Index(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        super(Index, self).__init__()

    '''
        Get a log to file   
    '''
    def get(self):

        return {"code": "SUCESS", "message": "Collector Works"}


class LogsResource(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        super(LogsResource, self).__init__()

    '''
        Get a log to file   
    '''
    def get(self):

        return {"code": "SUCESS", "message": "Logs"}

    '''
        Adds a log to file   
    '''
    def post(self):

        sessionId = request.headers.get('sessionId', None)
        abr = request.headers.get('abr', None)

        filename = SUMMARY_DIR + "/" + sessionId + "_" + abr + ".csv"
        print(sessionId)

        postData = json.loads(request.data)
        print(postData)

        log_file = None

        if not os.path.exists(filename):

            log_file = open(filename, 'w')

        else:
            log_file = open(filename, 'a')

        try:

            log_file.write(
                str(time.time()) + '\t' +
                str(postData['throughput']) + '\t' +
                str(postData['bitrate']) + '\t' +
                str(postData['qualityLevel']) + '\t' +
                str(postData['segmentSize']) + '\t' +
                str(postData['segmentDuration']) + '\t' +
                str(postData['segmentDelay']) + '\t' +
                str(postData['bufferLevel']) + '\t' +
                str(postData['rebufferingTime']) + '\t' +
                str(postData['downloadStartTime']) + '\t' +
                str(postData['downloadFinishTime']) + '\t' +
                '\n')
            log_file.flush()

            return {"code": "SUCESS", "message": "Logs Added successful!"}

        except:
            content = {"code": "ERROR", "message": "Try add log failed"}
            return Response(json.dumps(content), status=500, mimetype='application/json')

class GeneralResource(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        super(GeneralResource, self).__init__()

    '''
        Get a log to file   
    '''
    def get(self):

        return {"code": "SUCESS", "message": "Logs"}

    '''
        Adds a log to file   
    '''
    def post(self):

        
        postData = json.loads(request.data.decode("utf-8"))

        print(postData)

        abr = postData['abr']
        sessionId = postData['sessionTime']
        logType = postData['logType']
        log = postData['log']

        filename = SUMMARY_DIR + "/" + str(sessionId) + "_" + abr + "_" + logType + ".json"
        print(sessionId)
       
        log_file = None

        if not os.path.exists(filename):
            log_file = open(filename, 'w')
        else:
            log_file = open(filename, 'a')
        try:
            log_file.write(str(json.dumps(log)) + '\n')
            log_file.flush()

            return {"code": "SUCESS", "message": "Logs Added successful!"}

        except:
            content = {"code": "ERROR", "message": "Try add log failed"}
            return Response(json.dumps(content), status=500, mimetype='application/json')
