from flask import Flask,request,jsonify
from pymongo import MongoClient
from mongoengine_jsonencoder import MongoEngineJSONEncoder
import pandas as pd
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

    json = request.get_json()
    word = json.get('word')
    my_db = client['Project']
    mycol = my_db[word]
    #날짜시작,끝,태그를 뽑고, 워드카운트로 리스트화
    # my_doc = list(mycol.aggregate([{"$match":{"word":json.get('word')}},{"$unwind": "$wordcount"}, {"$project": {"_id": 0, "word": 0}}, {"$replaceWith": "$wordcount"}]))
    # my_doc= mycol.find({"word":word,"$or":[{"data":date1},{"data":date2}]},{"_id":0,"tags":1})
    num = json.get('num')#map에 포함된 갯수

    insta = []
    i=0
    for i in range(int(num)):
        q={"data":json.get('date'+str(i))}
        print("a")
        print(q)
        my_doc = mycol.find(q,{"_id":0,"tags":1})
        
        for i in my_doc:
            for j in range(len(i['tags'])):
                insta.append(i['tags'][j])#태그들을 따로 배열화하여 저장

        df = pd.DataFrame(insta, columns=['tags'])
        tag =df['tags'].value_counts().to_frame()#배열화한 데이터들의 갯수를 세주는 함수
        top10 = tag.head(10)
        q.clear()

    a=[]
    for i in range(len(top10.index)): #Dataframe으로 만들어진 count수를 dict화 해준다.
        b ={"tag":top10.index[i],"count":str(top10['tags'][i])}
        a.append(b)

    print(a)
    client.close()
    return jsonify(a)

@app.route("/yearchui",methods=['POST'])
def yearchui():
    my_db = client['Project']
    mycol = my_db['yearchui2020']
    dong = request.get_json()

    my_doc = list(mycol.find({"행정동명":dong.get("dong")},{"_id":0,"m2019예측":1,"m2020예측":1,"상권_코드_명":1}))

    for i in range(len(my_doc)):
                    print(i)

    print(my_doc)
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

