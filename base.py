class Base:
    VEL = 5
    
    def __init__(self, y):
        self.y = y
        self.x1 = 0
        
    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 < 0:
            pass
        if self.x2 < 0:
            pass
