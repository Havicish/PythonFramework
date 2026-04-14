from typing import Callable, Optional
from printmanager import PrintManager
import sys, termios, tty

class MenuItem:
  def __init__(self):
    self.name: str = ""
    self.callback: Optional[Callable] = None
    self.parent: Optional["MenuItem"] = None
    self.children: list["MenuItem"] = []

  def add_child(self, child: "MenuItem"):
    child.parent = self
    self.children.append(child)

class Menu:
  def __init__(self, print_manager: PrintManager):
    self.print_manager = print_manager
    self.main_menu = MenuItem()
    self.current_menu = self.main_menu

  def display_menu(self):
    self.print_manager.clear()
    self.print_manager.print("Menu:")
    for idx, item in enumerate(self.current_menu.children):
      self.print_manager.print(f"{idx + 1}. {item.name}")
    if self.current_menu.parent:
      self.print_manager.print("0. Back")