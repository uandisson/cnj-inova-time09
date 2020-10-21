from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine
from json import dumps
import xmltodict

#Class
from Util import Util
from db import Connect


db = Connect()
db.__init__

app = Flask(__name__)
api = Api(app)

class XMLRead(Resource):
    def post(self):
        print('post')
        xml_data = request.form['xmlTribunal']
        print(xml_data)
        util = Util()
        util.readXML(xml_data, db)

        return {"status": "success"}

    def get(self):
       
        return {"status" : "ok get"}

api.add_resource(XMLRead, '/xml') 

if __name__ == '__main__':
    app.run()

