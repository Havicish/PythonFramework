from math import sin
import time
from rgb import RGB

class Text:
  def __init__(self, text: str, color: RGB = RGB.white(), background_color: RGB = RGB.none(), end: str = "\n", bold: bool = False, italic: bool = False, dim: bool = False, reverse: bool = False, blink: bool = False, x: int = 0, y: int = 0, z_index: int = 0):
    self.text: str = text
    self.color: RGB = color
    self.background_color: RGB = background_color
    self.end: str = end
    self.bold: bool = bold
    self.italic: bool = italic
    self.dim: bool = dim
    self.reverse: bool = reverse
    self.blink: bool = blink
    self.x: int = x
    self.y: int = y
    self.stored_z_index: int = z_index
    self.is_gradient: bool = False
    self.gradient_start_color: RGB = RGB.white()
    self.gradient_end_color: RGB = RGB.white()
    self.is_visible: bool = True
    self.last_is_visible: bool = True
    self.z_index: int = z_index
    self.last_x: int = x
    self.last_y: int = y
    self.last_text_length: int = len(text)
    self.is_wave: bool = False
    self.last_time: float = 0.0
    self.wave_amplitude: float = 1.0
    self.wave_frequency: float = 1.0
    self.wave_speed: float = 1.0
    self._user_visible: bool = True

  def __eq__(self, other):
    return id(self) == id(other)

  def color_to_ansi_color(self):
    if self.reverse:
      if self.color == RGB.none() and self.background_color == RGB.none():
        return RGB.white().to_ansi_color()
      elif self.color == RGB.none():
        return self.background_color.to_ansi_color()
      elif self.background_color == RGB.none():
        return self.color.to_ansi_background_color()
      else:
        # Swap foreground and background colors for reverse effect
        return self.background_color.to_ansi_color()

    if self.color == RGB.none():
      return RGB.black().to_ansi_color()
    return self.color.to_ansi_color()
  
  def background_color_to_ansi_color(self):
    if self.reverse:
      if self.color == RGB.none() and self.background_color == RGB.none():
        return RGB.white().to_ansi_background_color()
      elif self.color == RGB.none():
        return self.background_color.to_ansi_background_color()
      elif self.background_color == RGB.none():
        return self.color.to_ansi_color()
      else:
        # Swap foreground and background colors for reverse effect
        return self.color.to_ansi_background_color()

    if self.background_color == RGB.none():
      return ""
    return self.background_color.to_ansi_background_color()
  
  def set_gradient(self, start_color: RGB, end_color: RGB):
    self.is_gradient = True
    self.gradient_start_color = start_color
    self.gradient_end_color = end_color
    if start_color == RGB.none() or end_color == RGB.none() or (start_color == end_color):
      self.is_gradient = False

  def set_wave(self, amplitude: float, frequency: float, speed: float):
    self.is_wave = True
    self.wave_amplitude = amplitude
    self.wave_frequency = frequency
    self.wave_speed = speed

  def hide(self):
    self._user_visible = False

  def show(self):
    self._user_visible = True
    
  def style_to_ansicode(self):
    style = ""
    if self.bold:
      style += "\033[1m"
    if self.italic:
      style += "\033[3m"
    if self.dim:
      style += "\033[2m"
    return style
  
  def update_z_index(self):
    if not self.is_visible:
      self.stored_z_index = -1
    else:
      self.stored_z_index = self.z_index

  def update_blink(self):
    if not self._user_visible:
      self.is_visible = False
    elif self.blink:
      self.is_visible = int(time.time() * 2) % 2 == 0
    else:
      self.is_visible = True

  def update_visibility(self):
    current_x = int(round(self.x))
    current_y = int(round(self.y))
    row = max(1, current_y + 1)
    col = max(1, current_x + 1)

    changed_position_or_width = (
      self.last_x != current_x
      or self.last_y != current_y
      or self.last_text_length != len(self.text)
    )

    parts = []
    if changed_position_or_width:
      last_row = max(1, self.last_y + 1)
      last_col = max(1, self.last_x + 1)
      parts.append(f"\033[{last_row};{last_col}H" + (" " * self.last_text_length) + "\033[0m")

    if not self.is_visible and self.last_is_visible:
      # Clear only this text region at its own position to avoid affecting others.
      parts.append(f"\033[{row};{col}H" + (" " * len(self.text)) + "\033[0m")
      self.last_is_visible = self.is_visible
      self.last_x = current_x
      self.last_y = current_y
      self.last_text_length = len(self.text)
      return "".join(parts)
    self.last_is_visible = self.is_visible

  def get_print_string(self, delta_time: float = 0.0):
    self.text = str(self.text)

    # ANSI cursor positioning is 1-based (row;column).
    # Keep `x`/`y` in this framework 0-based for easier use.
    current_x = int(round(self.x))
    current_y = int(round(self.y))
    row = max(1, current_y + 1)
    col = max(1, current_x + 1)

    changed_position_or_width = (
      self.last_x != current_x
      or self.last_y != current_y
      or self.last_text_length != len(self.text)
    )

    parts = []
    if changed_position_or_width:
      last_row = max(1, self.last_y + 1)
      last_col = max(1, self.last_x + 1)
      parts.append(f"\033[{last_row};{last_col}H" + (" " * self.last_text_length) + "\033[0m")

    string = f"\033[{row};{col}H"
    if self.is_gradient:
      if not self.is_wave:
        length = len(self.text)
        for i, char in enumerate(self.text):
          ratio = i / max(length - 1, 1)
          r = int(self.gradient_start_color.r * (1 - ratio) + self.gradient_end_color.r * ratio)
          g = int(self.gradient_start_color.g * (1 - ratio) + self.gradient_end_color.g * ratio)
          b = int(self.gradient_start_color.b * (1 - ratio) + self.gradient_end_color.b * ratio)
          char_color = RGB(r, g, b)
          string += char_color.to_ansi_color() + char
        string += self.end + "\033[0m"
      else:
        length = len(self.text)
        for i, char in enumerate(self.text):
          ratio = i / max(length - 1, 1)
          r = int(self.gradient_start_color.r * (1 - ratio) + self.gradient_end_color.r * ratio)
          g = int(self.gradient_start_color.g * (1 - ratio) + self.gradient_end_color.g * ratio)
          b = int(self.gradient_start_color.b * (1 - ratio) + self.gradient_end_color.b * ratio)
          char_color = RGB(r, g, b)
          last_wave_offset = int(sin((self.last_time * self.wave_speed) + i * self.wave_frequency) * self.wave_amplitude)
          wave_offset = int(sin((time.time() * self.wave_speed) + i * self.wave_frequency) * self.wave_amplitude)
          string += char_color.to_ansi_color()
          string += f"\033[{row + last_wave_offset};{col + i}H" + char_color.to_ansi_color() + " "
          string += f"\033[{row + wave_offset};{col + i}H" + char_color.to_ansi_color() + char
        string += self.end + "\033[0m"
        self.last_time = time.time()
    elif self.is_wave:
      length = len(self.text)
      for i, char in enumerate(self.text):
        last_wave_offset = int(sin((self.last_time * self.wave_speed) + i * self.wave_frequency) * self.wave_amplitude)
        wave_offset = int(sin((time.time() * self.wave_speed) + i * self.wave_frequency) * self.wave_amplitude)
        char_color = self.color
        string += f"\033[{row + last_wave_offset};{col + i}H" + char_color.to_ansi_color() + " "
        string += f"\033[{row + wave_offset};{col + i}H" + char_color.to_ansi_color() + char
      string += self.end + "\033[0m"
      self.last_time = time.time()
    else:
      # Add styles and colors
      string += self.style_to_ansicode() + self.color_to_ansi_color() + self.background_color_to_ansi_color() + self.text + self.end + "\033[0m"

    self.last_x = current_x
    self.last_y = current_y
    self.last_text_length = len(self.text)
    parts.append(string)

    return "".join(parts)

class PrintManager:
  def __init__(self):
    self.screen: list[Text] = []
  
  def add_text(self, text: Text):
    self.screen.append(text)
    return text

  def print(self, delta_time: float = 0.0):
    thing_to_print = ""
    for text in self.screen:
      text.update_z_index()
      text.update_blink()
    for text in sorted(self.screen, key=lambda t: t.stored_z_index):
      thing_to_print += text.update_visibility() or ""
      if not text.is_visible:
        continue
      thing_to_print += text.get_print_string(delta_time)
    print(thing_to_print, end="")

  def clear(self):
    print("\033[2J\033[H\033[2J\033[3J", end="")

  def hide_cursor(self):
    print("\033[?25l", end="")

  def show_cursor(self):
    print("\033[?25h", end="")

  def find_text(self, text: Text):
    for idx, t in enumerate(self.screen):
      if t == text:
        return idx
    return -1