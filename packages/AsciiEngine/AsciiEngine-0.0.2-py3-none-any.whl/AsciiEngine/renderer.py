from os import system
from .mathutils import Vector2

class Renderer:
        def __init__(self, sizex=32, sizey=32):
            self.sizex = sizex
            self.sizey = sizey
        
        def layer2d(self, object, current, pos):
            for char in object:
                current[pos.x][pos.y] = char
                pos.x += 1
            return current
        
        def layer2d(self, object, current, pos):
            for char in object:
                current[pos] = char
                pos += 1
            return current
        
        def pixelsToScanlines(pixels) -> list:
            return [''.join(data) for data in pixels]
        
        def clear(self):
            '''Clear screen on unix and windows'''
            try:
                system("clear")
            except:
                system("cls")
        
        def render(self, data) -> bool:
            '''Render array of scanlines'''
            self.clear()
            if len(data) < 1:
                return False
            del data[:-self.sizey]
            for scanline in data:
                print(scanline)
            return True
