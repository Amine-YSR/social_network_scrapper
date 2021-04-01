from mongoengine import *

class Post_Insta(Document):
    met = {"collection":"Posts"}
    _id = StringField(required=True)
    comments = StringField(max_length=5000)
    image = fields.ImageField(thumbnail=(150,150,False))