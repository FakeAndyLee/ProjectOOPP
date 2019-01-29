import shelve
import uuid

class Feedback:
    def __init__(self, id):
        self.id = id
        self.name = ''
        self.comment = ''

feedbacks = shelve.open('feedbacklist')

def get_feedbacks():
    klist = list(feedbacks.keys())
    x = []
    for i in klist:
        x.append(feedbacks[i])
    return x

def generate_feedbackID():
    return str(uuid.uuid4())


