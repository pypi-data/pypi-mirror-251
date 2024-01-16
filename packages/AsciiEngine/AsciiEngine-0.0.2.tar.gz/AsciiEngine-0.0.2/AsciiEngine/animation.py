class InvalidAnimationFile(Exception):
    def __init__(self, message="The provided file for animation is not valid. Did you remember to separate your frames?"):
        pass

class FullScreenAnimation:
        def __init__(self, framesFilename=None):
            if framesFilename:
                framesFile = open(framesFilename)
                if framesFile.read(6) != ":frame":
                    raise InvalidAnimationFile("No starting frame found")
                frames = framesFile.read().split(":frame")
                frames = [temp.split() for temp in frames]
                self.frames = frames
        def render(self, renderer, frame):
            renderer.render(self.frames[frame])