import requests
import pymongo
import json

endpoint_thingboard='https://demo.thingsboard.io/api/v1/BIkZtZPHpmGLJU1KEtpZ/telemetry'
client = pymongo.MongoClient("mongodb://dbUser:qazqaz@cluster0-shard-00-00-z0ohv.mongodb.net:27017,cluster0-shard-00-01-z0ohv.mongodb.net:27017,cluster0-shard-00-02-z0ohv.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")

def fungsiThingboard(a):
    pub_string={"Nama":a}
    req=requests.post(endpoint_thingboard, json.dumps(pub_string))
    print("berhasil di upload thingsboard")

def postmongo(a,b,c):
    db = client.test
    posts=db.posts
    #mycol=db.posts
    posts_data={
    'Nama':a,
    'Confidence':b,
    'Waktu':c
    }
    result=posts.insert_one(posts_data)
    print('berhasil di upload ke mongodb:{0}'.format(result.inserted_id))
