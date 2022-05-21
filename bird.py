class Bird:
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        
    def jump(self):
        self.vel = -10.5
        self.tick_count = 0 
        self.height = self.y
    
    def move(self):
        self.tick_count += 1
