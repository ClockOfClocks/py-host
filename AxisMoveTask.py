class AxisMoveTask:

    def __init__(self,
                 degree: float,
                 speed: float,
                 relative: bool = False
                 ):

        self.degree = degree
        self.speed = speed
        self.relative = relative
