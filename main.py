import time
from printmanager import PrintManager, Text
from rgb import RGB

def main():
  print_manager = PrintManager()

  print_manager.clear()
  text0 = Text("Hello, World!", color=RGB.red(), bold=True)
  text1 = Text("Test text", color=RGB.white(), x=0, y=1)
  print_manager.add_text(text0)
  print_manager.add_text(text1)
  print_manager.print()

  text1.color = RGB.blue()
  print_manager.print()

  while True:
    text0.set_gradient(RGB.from_hsl(((time.time() + 1) * 60) % 360, 1, 0.5), RGB.from_hsl((time.time() * 60) % 360, 1, 0.5))
    print_manager.print()
    time.sleep(1/60)

if __name__ == "__main__":
  main()