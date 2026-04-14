from rgb import RGB

class Text:
  def __init__(self, text: str, color: RGB = RGB.white(), background_color: RGB = RGB.none(), end: str = "\n", bold: bool = False, italic: bool = False, dim: bool = False, reverse: bool = False, x: int = 0, y: int = 0, z_index: int = 0):
    self.text: str = text
    self.color: RGB = color
    self.background_color: RGB = background_color
    self.end: str = end
    self.bold: bool = bold
    self.italic: bool = italic
    self.dim: bool = dim
    self.reverse: bool = reverse
    self.x: int = x
    self.y: int = y
    self.stored_z_index: int = z_index
    self.is_gradient: bool = False
    self.gradient_start_color: RGB = RGB.white()
    self.gradient_end_color: RGB = RGB.white()
    self.is_visible: bool = True
    self.z_index: int = z_index

  def __eq__(self, other):
    return id(self) == id(other)

  def color_to_ansi_color(self):
    return self.color.to_ansi_color() if not self.reverse else self.background_color.to_ansi_color()
  
  def background_color_to_ansi_color(self):
    if self.background_color == RGB.none():
      return ""
    return self.background_color.to_ansi_background_color() if not self.reverse else self.color.to_ansi_background_color()
  
  def set_gradient(self, start_color: RGB, end_color: RGB):
    self.is_gradient = True
    self.gradient_start_color = start_color
    self.gradient_end_color = end_color

  def hide(self):
    self.is_visible = False

  def show(self):
    self.is_visible = True
    
  def style_to_ansicode(self):
    style = ""
    if self.bold:
      style += "\033[1m"
    if self.italic:
      style += "\033[3m"
    if self.dim:
      style += "\033[2m"
    return style

  def get_print_string(self):
    # ANSI cursor positioning is 1-based (row;column).
    # Keep `x`/`y` in this framework 0-based for easier use.
    row = max(1, self.y + 1)
    col = max(1, self.x + 1)
    string = f"\033[{row};{col}H"
    if self.is_gradient:
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
      # Add styles and colors
      string += self.style_to_ansicode() + self.color_to_ansi_color() + self.background_color_to_ansi_color() + self.text + self.end + "\033[0m"
    return string

class PrintManager:
  def __init__(self):
    self.screen: list[Text] = []
  
  def add_text(self, text: Text):
    self.screen.append(text)
    return text

  def print(self):
    thing_to_print = ""
    for text in sorted(self.screen, key=lambda t: t.z_index):
      if text.is_visible:
        thing_to_print += text.get_print_string()
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