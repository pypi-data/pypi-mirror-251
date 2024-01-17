import time


class GameLoop:
    def loop(self, targetFps, func):
        '''Main loop'''
        while True:
            starttime = time.perf_counter()
            func ()
            endtime = time.perf_counter()
            time.sleep(abs(1 / (targetFps) - (endtime - starttime)))