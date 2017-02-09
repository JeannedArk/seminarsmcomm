from abc import ABC, abstractmethod

class Activity(ABC):
    """Represents the super class for all activities"""

    def __init__(self, atype):
        self.atype = atype

    @abstractmethod
    def execute(self):
        """We use a command pattern to execute the activity for seperation of concers reasons,
        to avoid using activity explicit code in other parts
        """
        pass

class ActionActivity(Activity):
    """Represents an ActionActivity

    TODO optional attributes
    TODO start_frame, end_frame
    """
    def __init__(self, atype, nameaction, target, name, speed=1.0, energy=0.0):
        super(self.__class__, self).__init__(atype)
        self.nameaction = nameaction
        self.target = target
        self.name = name
        self.speed = float(speed)

    def execute(self, bge):
        print("execute: " + str(self))

        if self.atype == "lightAction":
            self.executeLightAction()
        else:
            cont = bge.logic.getCurrentController()
            own = cont.owner

            # TODO get from activity?
            start_frame = 0
            end_frame = 30
            own.playAction(self.name, start_frame, end_frame, play_mode=bge.logic.KX_ACTION_MODE_PLAY, speed=self.speed)

    def executeLightAction(self):
        # TODO implement here light action
        pass

    def __str__(self):
        return  "ActionActivity(target: " + self.target + ", name: " + self.name + ", nameaction: " + self.nameaction + ")"

class SpeechActivity(Activity):
    """Represents a SpeechActivity"""

    def __init__(self, atype, target, text):
        super(self.__class__, self).__init__(atype)
        self.target = target
        self.text = text

    def execute(self, bge):
        """Not yet implemented, waiting for MaryTTS module"""
        print("execute: " + str(self))
        pass

    def __str__(self):
        return "SpeechActivity(target: " + self.target + ", text: " + self.text + ")"
