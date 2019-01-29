import shelve
import uuid

class Storage:
    def __init__(self, id):
        self.__id = id
        self.__description = ''
        self.__picture = ''

    def get_id(self):
        return self.__id

    def set_description(self, description):
        self.__description = description

    def set_picture(self, picture):
        self.__picture = picture

    def get_description(self):
        return self.__description

    def get_picture(self):
        return self.__picture


class Blog:
    def __init__(self, id):
        self.id = id
        self.description = ''
        self.picture = ''


blogs = shelve.open('blogs')       #blogs is to open shelve


def create_blog(description, picture):
    id = str(uuid.uuid4())
    blog = Blog(id)      #class on top(Blog)
    blog.description = description
    blog.picture = picture
    blogs[id] = blog    #push into dic value

def update_blog(blog):
    blogs[blog.id] = blog

def delete_blog(id):
    if id in blogs:
        del blogs[id]

def get_blogs():
    klist = list(blogs.keys())
    x = []
    for i in klist:
        x.append(blogs[i])
    return x

def get_blog(id):
    if id in blogs:
        return blogs[id]

def update_user(id, blogs):
    blogs[id] = blogs
    return blogs[id]

def clear_user():
    klist = list(blogs.keys())
    for key in klist:
        del blogs[key]

def clear_blog():
    klist = list(blogs.keys())
    for key in klist:
        del blogs[key]

def add_user(blog):
    blogs[blog.get_id()] = blog
