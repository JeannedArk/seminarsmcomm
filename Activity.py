class ActionActivity(object):
    def __init__(self, atype, nameaction, object, name):
        self.atype = atype
        self.nameaction = nameaction
        self.object = object
        self.name = name

    def __str__(self):
        return  "ActionActivity(object: " + self.object + " name: " + self.name + " nameaction: " + self.nameaction + ")"

class SpeechActivity(object):
    def __init__(self, atype, object, text):
        self.atype = atype
        self.object = object
        self.text = text

    def __str__(self):
        return "SpeechActivity(object: " + self.object + " text: " + self.text + ")"
