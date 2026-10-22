#!/usr/bin/python3
"""Abre o gerenciador sem instalar ou alterar preferências automaticamente."""
import argparse
from pathlib import Path

def main():
 parser=argparse.ArgumentParser(description='Gerenciador pessoal Gruvbox')
 parser.add_argument('--sandbox-home',type=Path,help='Conta temporária para testes, nunca sua pasta pessoal')
 parser.add_argument('--profile',type=Path)
 parser.add_argument('--operation',choices=['apply','uninstall','restore'],default='apply')
 args=parser.parse_args()
 import gi
 gi.require_version('Gtk','3.0')
 from gi.repository import Gtk
 from gui_manager.engine import Manager
 from gui_manager.profiles import load
 from gui_manager.app import Window
 manager=Manager(args.sandbox_home,True) if args.sandbox_home else Manager()
 profile=load(args.profile) if args.profile else None
 window=Window(manager,profile);window.show_all();window.operation.set_active_id(args.operation);window.points_combo.set_visible(args.operation=='restore');Gtk.main()
if __name__=='__main__':main()
