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
    """Represents an ActionActivity"""
    def __init__(self, atype, nameaction, target, name, start_frame=0, end_frame=0, speed=1.0, energy=0.0):
        super(self.__class__, self).__init__(atype)
        self.nameaction = nameaction
        self.target = target
        self.name = name
        self.start_frame = int(start_frame)
        self.end_frame = int(end_frame)
        self.speed = float(speed)
        self.energy = float(energy)

    def execute(self, bge):
        """Execute this activity"""
        print("execute: " + str(self))

        if self.nameaction == "lightAction":
            self.executeLightAction(bge)
        else:
            cont = bge.logic.getCurrentController()
            own = cont.owner
            own.playAction(self.name, self.start_frame, self.end_frame, play_mode=bge.logic.KX_ACTION_MODE_PLAY, speed=self.speed)

    def executeLightAction(self, bge):
        """Execute a light action"""
        print("h: "+ str(bge.logic.getCurrentScene()))
        scene = bge.logic.getCurrentScene()
        light = scene.lights[self.target]
        light.energy = self.energy

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
