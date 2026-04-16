import sys, termios, tty
import os
import threading

os.set_blocking(sys.stdin.fileno(), False)

class InputManager:
  def __init__(self):
    self.key_press_callbacks = []
    self._thread = None
    self._running = False
    self._old_settings = None
    self._fd = None

  def add_key_press_callback(self, callback):
    self.key_press_callbacks.append(callback)

  def listen_for_input(self):
    self._running = True
    self._thread = threading.Thread(target=self._input_loop, daemon=True)
    self._thread.start()

  def stop(self):
    self._running = False
    if self._fd is not None and self._old_settings is not None:
      termios.tcsetattr(self._fd, termios.TCSADRAIN, self._old_settings)

  def _input_loop(self):
    self._fd = sys.stdin.fileno()
    self._old_settings = termios.tcgetattr(self._fd)
    try:
      tty.setcbreak(self._fd)
      while self._running:
        for line in sys.stdin:
          for callback in self.key_press_callbacks:
            callback(line)
    finally:
      termios.tcsetattr(self._fd, termios.TCSADRAIN, self._old_settings)

  def __del__(self):
    self.stop()