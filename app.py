from apiclient.discovery import build
from flask import Flask, request, json
from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask_cors import CORS

client = MongoClient()

api_key = "AIzaSyAm2QfYBhP7iGuYdVpdJS21l_Mt00UQRt4"
youtube = build('youtube', 'v3', developerKey=api_key)
app = Flask(__name__)

CORS(app)
cors = CORS(app, resources={
    r"/*": {
        "origins": "*"
    }
})

client = MongoClient("mongodb+srv://brajesh:1234@cluster0.uhrit.mongodb.net/inter_iit?retryWrites=true&w=majority")
db = client['inter_iit']
coll = db['test']


@app.route("/")
def home():
    return "done"

def empty_collection():
    coll.delete_many({})

@app.route("/search", methods=['POST', 'GET'])
def search():
    
    if request.method == "POST":
        empty_collection()
        json_data = request.json
        body = json_data['body']
        #a_value = json_data["name"]
        data = body["name"]
        print(data)
        req = youtube.search().list(part='snippet',
                                    q=data,
                                    type='video',
                                    maxResults=50)
        type(req)
        res = req.execute()
        l = []
        for i in res['items']:
            temp = i['id']['videoId']
            date = i['snippet']['publishTime']
            coll.insert_one({
                'body': temp,
                'date': date[0:9]
            })
            l.append(temp)
        data = json.dumps(l)
    else:
        return "get working"
    return data


if __name__ == "__main__":
    app.run()
