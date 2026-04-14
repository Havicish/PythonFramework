import time
from printmanager import PrintManager, Text
from rgb import RGB
from menu import Menu

def main():
  print_manager = PrintManager()
  main_menu = Menu(print_manager)

  print_manager.clear()
  text0 = Text("Hello, World!", color=RGB.red(), bold=True)
  text1 = Text("Test text", color=RGB.white(), x=0, y=1)
  print_manager.add_text(text0)
  print_manager.add_text(text1)

  text1.color = RGB.blue()

  while True:
    text0.set_gradient(RGB.from_hsl(((time.time() + 1) * 60) % 360, 1, 0.5), RGB.from_hsl((time.time() * 60) % 360, 1, 0.5))
    print_manager.print()
    if time.time() % 5 < 2.5:
      text1.hide()
    else:
      text1.show()
    time.sleep(1/60)

if __name__ == "__main__":
  main()