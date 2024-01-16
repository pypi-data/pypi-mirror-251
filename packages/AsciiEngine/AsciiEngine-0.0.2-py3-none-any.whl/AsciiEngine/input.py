from pynput import keyboard

class KeyboardInput:
    def __init__(self, framerate=60):
        def on_press(key):
            self.keydown = key
    
        def on_release(key):
            self.keydown = None
        
        
        self.keydown = None
        self.checkKeys = True
        self.defaultCooldown = framerate / 10
        self.cooldown = self.defaultCooldown
        self.listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        self.listener.start()
    
    def getKeydown(self):
        self.checkKeys = False
        return self.keydown
    
    def anyKeyDown(self):
        return True if self.keydown else False
    
    def reset(self):
        self.keydown = None
    
    def update(self):
        if not self.checkKeys:
            self.cooldown -= 1
        if self.cooldown == 0:
            self.cooldown = self.defaultCooldown
            self.checkKeys = True
    