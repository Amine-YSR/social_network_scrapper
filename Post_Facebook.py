from mongoengine import *

class Post(Document):
    met = {"collection":"Posts_Facebook"}
    _id = StringField(required=True)
    content = StringField(max_length=5000)
    comments = StringField(max_length=5000)
    image = fields.ImageField(thumbnail=(150,150,False))
