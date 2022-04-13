import time
class PD:
    def __init__(self, k):
        self._kp, self._kd = k
        self._prev_error = 0
        self.prev_output = 0
        self.restart()
    def keep(self, error):
        timestamp = time.time()
        if self.restarted:
            self._prev_error = error
            self._timestamp = time.time()-0.001
            self.restarted  = False
        if not (timestamp-self._timestamp):
            return self.prev_output
        output = self._kp*error + self._kd/(timestamp-self._timestamp)*(error-self._prev_error)
        self._timestamp = timestamp-0.001
        self._prev_error = error
        self.prev_output = output
        return output
    def restart(self):
        self.restarted = True