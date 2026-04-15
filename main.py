import time
from inputmanager import InputManager
from printmanager import PrintManager, Text
from rgb import RGB
from math import cos, sin

def main():
  print_manager = PrintManager()
  input_manager = InputManager()
  input_manager.listen_for_input()
  input_manager.add_key_press_callback(lambda key: setattr(last_pressed_key_text, "text", f"{last_pressed_key_text.text}{repr(key)}"))

  print_manager.clear()
  normal_text = Text("Normal Text", y=0)
  colored_text = Text("Colored Text", color=RGB(19, 63, 215), y=1)
  black_text = Text("Black Text", color=RGB.black(), y=2)
  background_colored_text = Text("Background Colored Text", background_color=RGB.green(), y=3)
  reversed_text = Text("Reversed Text", color=RGB.blue(), background_color=RGB.green(), reverse=True, y=4)
  gradient_text = Text("Gradient Text", y=5)
  gradient_text.set_gradient(RGB.blue(), RGB.red())
  bold_text = Text("Bold Text", bold=True, y=6)
  italic_text = Text("Italic Text", italic=True, y=7)
  dim_text = Text("Dim Text", dim=True, y=8)
  blink_text = Text("Blinking Text", blink=True, y=9)
  moving_text = Text("Moving Text", y=10, z_index=1)
  underlay_text = Text("----------Underlay Text----------", color=RGB.red(), y=10, z_index=0)
  rainbow_text = Text("Rainbow Text", y=11)
  wave_text = Text("------------Wave Text------------", y=13)
  wave_text.set_gradient(RGB.from_hsl(0, 1, 0.5), RGB.from_hsl(60, 1, 0.5))
  wave_text.is_wave = True
  wave_text.wave_amplitude = 2.0
  wave_text.wave_frequency = 0.25
  wave_text.wave_speed = -10.0
  last_pressed_key_text = Text("", y=15)

  print_manager.add_text(normal_text)
  print_manager.add_text(colored_text)
  print_manager.add_text(black_text)
  print_manager.add_text(background_colored_text)
  print_manager.add_text(reversed_text)
  print_manager.add_text(gradient_text)
  print_manager.add_text(bold_text)
  print_manager.add_text(italic_text)
  print_manager.add_text(dim_text)
  print_manager.add_text(blink_text)
  print_manager.add_text(moving_text)
  print_manager.add_text(underlay_text)
  print_manager.add_text(rainbow_text)
  print_manager.add_text(wave_text)
  print_manager.add_text(last_pressed_key_text)

  print_manager.hide_cursor()

  last_time = time.time()
  while True:
    try:
      delta_time = time.time() - last_time
      last_time = time.time()

      moving_text.x = int((cos(time.time() * 3) / 2 + 0.5) * 23)
      rainbow_text.set_gradient(RGB.from_hsl((time.time() * 250) % 360, 1, 0.5), RGB.from_hsl(((time.time() * 250) - 60) % 360, 1, 0.5))

      print_manager.print(delta_time)
      time.sleep(1/60)
    except KeyboardInterrupt:
      print_manager.show_cursor()
      print_manager.clear()
      input_manager.stop()
      break

if __name__ == "__main__":
  main()