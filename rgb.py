class RGB:
  def __init__(self, r: int, g: int, b: int):
    self.r = r
    self.g = g
    self.b = b

  def __eq__(self, other):
    if not isinstance(other, RGB):
      return False
    return self.r == other.r and self.g == other.g and self.b == other.b
  
  def __str__(self):
    return f"RGB({self.r}, {self.g}, {self.b})"
  
  def __repr__(self):
    return self.__str__()
  
  def __add__(self, other):
    if not isinstance(other, (int, RGB)):
      raise ValueError("Can only add RGB by a number, or another RGB")
    if isinstance(other, RGB):
      return RGB(min(self.r + other.r, 255), min(self.g + other.g, 255), min(self.b + other.b, 255))
    return RGB(min(self.r + other, 255), min(self.g + other, 255), min(self.b + other, 255))
  
  def __mul__(self, other):
    if not isinstance(other, (int, RGB)):
      raise ValueError("Can only multiply RGB by a number, or another RGB")
    if isinstance(other, RGB):
      return RGB(min(int(self.r * other.r / 255), 255), min(int(self.g * other.g / 255), 255), min(int(self.b * other.b / 255), 255))
    return RGB(min(int(self.r * other), 255), min(int(self.g * other), 255), min(int(self.b * other), 255))
  
  def __rmul__(self, other):
    return self.__mul__(other)
  
  def __truediv__(self, other):
    if not isinstance(other, (int, RGB)):
      raise ValueError("Can only divide RGB by a number, or another RGB")
    if isinstance(other, RGB):
      return RGB(min(int(self.r / other.r * 255), 255), min(int(self.g / other.g * 255), 255), min(int(self.b / other.b * 255), 255))
    return RGB(min(int(self.r / other), 255), min(int(self.g / other), 255), min(int(self.b / other), 255))
  
  def __rtruediv__(self, other):
    if not isinstance(other, (int, RGB)):
      raise ValueError("Can only divide RGB by a number, or another RGB")
    if isinstance(other, RGB):
      return RGB(min(int(other.r / self.r * 255), 255), min(int(other.g / self.g * 255), 255), min(int(other.b / self.b * 255), 255))
    return RGB(min(int(other / self.r * 255), 255), min(int(other / self.g * 255), 255), min(int(other / self.b * 255), 255))

  def to_ansi_color(self):
    return f"\033[38;2;{self.r};{self.g};{self.b}m"

  def to_ansi_background_color(self):
    return f"\033[48;2;{self.r};{self.g};{self.b}m"

  @staticmethod
  def white():
    return RGB(255, 255, 255)
  
  @staticmethod
  def red():
    return RGB(255, 0, 0)
  
  @staticmethod
  def green():
    return RGB(0, 255, 0)
  
  @staticmethod
  def blue():
    return RGB(0, 0, 255)

  @staticmethod
  def yellow():
    return RGB(255, 255, 0)
  
  @staticmethod
  def pink():
    return RGB(255, 0, 255)
  
  @staticmethod
  def cyan():
    return RGB(0, 255, 255)
  
  @staticmethod
  def orange():
    return RGB(255, 128, 0)
  
  @staticmethod
  def purple():
    return RGB(128, 0, 255)

  @staticmethod
  def gray():
    return RGB(128, 128, 128)
  
  @staticmethod
  def black():
    return RGB(0, 0, 0)
  
  @staticmethod
  def none():
    return RGB(-1, -1, -1)
  
  @staticmethod
  def from_hsl(h, s, l):
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2
    if h < 60:
      r, g, b = c, x, 0
    elif h < 120:
      r, g, b = x, c, 0
    elif h < 180:
      r, g, b = 0, c, x
    elif h < 240:
      r, g, b = 0, x, c
    elif h < 300:
      r, g, b = x, 0, c
    else:
      r, g, b = c, 0, x
    return RGB(int((r + m) * 255), int((g + m) * 255), int((b + m) * 255))