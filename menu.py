from rgb import RGB
from printmanager import PrintManager, Text
from typing import Callable, Optional
from printmanager import PrintManager
import sys, termios, tty

class MenuItem:
  def __init__(self, Menu: "Menu"):
    self.callback: Optional[Callable] = None
    self.menu: "Menu" = Menu
    self.parent: Optional["MenuItem"] = None
    self.children: list["MenuItem"] = []
    self.text_item: Optional[Text] = None

  def add_child(self, child: "MenuItem"):
    child.parent = self
    self.children.append(child)

  def set_text(self, text: Text):
    if self.text_item is not None:
      for property in vars(self.text_item):
        setattr(self.text_item, property, getattr(self.text_item, property))
    else:
      self.text_item = text
      self.menu.print_manager.add_text(self.text_item)

class Menu:
  def __init__(self, print_manager: PrintManager):
    self.print_manager = print_manager
    self.main_menu = MenuItem(self)
    self.current_menu = self.main_menu

  