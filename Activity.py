class ActionActivity(object):
    """Represents an ActionActivity

    TODO optional attributes
    """
    def __init__(self, atype, nameaction, object, name, speed):
        self.atype = atype
        self.nameaction = nameaction
        self.object = object
        self.name = name
        self.speed = speed

    def __str__(self):
        return  "ActionActivity(object: " + self.object + ", name: " + self.name + ", nameaction: " + self.nameaction + ")"

class SpeechActivity(object):
    """Represents a SpeechActivity"""
    def __init__(self, atype, object, text):
        self.atype = atype
        self.object = object
        self.text = text

    def __str__(self):
        return "SpeechActivity(object: " + self.object + ", text: " + self.text + ")"
