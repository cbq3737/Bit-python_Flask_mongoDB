from flask import Flask,request,jsonify
from pymongo import MongoClient
from mongoengine_jsonencoder import MongoEngineJSONEncoder

app = Flask(__name__) #플라스크 객체 생성
app.json_encoder = MongoEngineJSONEncoder
app.config['JSON_AS_ASCII'] = False #인코딩


#client = MongoClient("mongodb://14.32.18.97:27017/")
client = MongoClient("14.32.18.97",27017,username='Project',password='bit')
print(client)

@app.route('/environments/<language>')
def environments(language):
    return jsonify({"language":language})

@app.route('/message/<int:message_id>')
def get_message(message_id):
    return "message id: " + message_id

@app.route("/upjong",methods=['POST'])
def upjong():
    my_db = client['Project']
    mycol = my_db['allSang']
    value = request.get_json()

    my_doc = list(mycol.find({"class":value.get('classes')},{"_id":0}))
    print(my_doc)

    client.close()#mongoDB닫는것.

    return jsonify(my_doc)

@app.route("/instar",methods=['POST'])
def instar():
    my_db = client['test']
    mycol = my_db['test']
    name = request.get_json()

    my_doc = list(mycol.find({},{"_id":0}))

    client.close()
    return jsonify(my_doc)

@app.route("/mongoTest",methods=['POST'])
def mongoTest():
    my_db = client['test']
    mycol = my_db['test']
    name = request.get_json()

    my_doc = list(mycol.find({},{"_id":0}))

    client.close()
    return jsonify(my_doc)

@app.route("/server_info")
def server_json():

    data ={"server_name":"0.0.0.0","server_port":"8000"}

    return jsonify(data)

