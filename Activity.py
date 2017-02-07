class ActionActivity(object):
    """Represents an ActionActivity

    TODO optional attributes
    TODO start_frame, end_frame
    """
    def __init__(self, atype, nameaction, target, name, speed=1.0):
        self.atype = atype
        self.nameaction = nameaction
        self.target = target
        self.name = name
        self.speed = float(speed)

    def __str__(self):
        return  "ActionActivity(target: " + self.target + ", name: " + self.name + ", nameaction: " + self.nameaction + ")"

class SpeechActivity(object):
    """Represents a SpeechActivity"""
    def __init__(self, atype, target, text):
        self.atype = atype
        self.target = target
        self.text = text

    def __str__(self):
        return "SpeechActivity(target: " + self.target + ", text: " + self.text + ")"
