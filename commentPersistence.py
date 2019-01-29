import shelve
import uuid


class Comment:
    def __init__(self, id):
        self.id = id
        self.comment1 = ''
        self.comment2 = ''


routeComment = shelve.open('routeNotes')


def get_comments():
    klist = list(routeComment.keys())
    x = []
    for i in klist:
        x.append(routeComment[i])
    return x

def generate_commentID():
    return str(uuid.uuid4())

