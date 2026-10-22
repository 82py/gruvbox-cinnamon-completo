#!/usr/bin/python3
import hashlib
import sys
import threading
from pathlib import Path
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib

class HashWindow(Gtk.Window):
    def __init__(self, path):
        super().__init__(title="Calcular hash")
        self.path = Path(path)
        self.set_default_size(660, 220)
        self.set_border_width(16)
        self.connect("destroy", Gtk.main_quit)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.add(box)
        label = Gtk.Label(label=str(self.path))
        label.set_line_wrap(True)
        label.set_selectable(True)
        box.pack_start(label, False, False, 0)
        row = Gtk.Box(spacing=10)
        box.pack_start(row, False, False, 0)
        row.pack_start(Gtk.Label(label="Algoritmo:"), False, False, 0)
        self.combo = Gtk.ComboBoxText()
        for name in ("MD5", "SHA-1", "SHA-256", "SHA-512"):
            self.combo.append_text(name)
        self.combo.set_active(2)
        row.pack_start(self.combo, False, False, 0)
        self.calculate = Gtk.Button(label="Calcular")
        self.calculate.connect("clicked", self.start)
        row.pack_start(self.calculate, False, False, 0)
        self.result = Gtk.Entry()
        self.result.set_editable(False)
        box.pack_start(self.result, False, False, 0)
        self.status = Gtk.Label(label="Escolha o algoritmo e clique em Calcular.")
        box.pack_start(self.status, False, False, 0)
        self.copy = Gtk.Button(label="Copiar hash")
        self.copy.set_sensitive(False)
        self.copy.connect("clicked", self.copy_hash)
        box.pack_start(self.copy, False, False, 0)
        self.combo.connect("changed", self.reset)
        self.show_all()

    def reset(self, *_):
        self.result.set_text("")
        self.copy.set_sensitive(False)
        self.status.set_text("Clique em Calcular para o algoritmo selecionado.")

    def start(self, *_):
        algorithm = self.combo.get_active_text().lower().replace("-", "")
        self.calculate.set_sensitive(False)
        self.combo.set_sensitive(False)
        self.copy.set_sensitive(False)
        self.result.set_text("")
        self.status.set_text("Calculando…")
        threading.Thread(target=self.compute, args=(algorithm,), daemon=True).start()

    def compute(self, algorithm):
        try:
            digest = hashlib.new(algorithm)
            with self.path.open("rb") as stream:
                while chunk := stream.read(1024 * 1024):
                    digest.update(chunk)
            GLib.idle_add(self.finish, digest.hexdigest(), None)
        except Exception as error:
            GLib.idle_add(self.finish, "", str(error))

    def finish(self, value, error):
        self.calculate.set_sensitive(True)
        self.combo.set_sensitive(True)
        self.result.set_text(value)
        self.copy.set_sensitive(bool(value))
        self.status.set_text("Erro: " + error if error else "Hash pronto. Você pode selecionar o texto ou copiá-lo.")
        return False

    def copy_hash(self, *_):
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(self.result.get_text(), -1)
        clipboard.store()
        self.status.set_text("Hash copiado para a área de transferência.")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        HashWindow(sys.argv[1])
        Gtk.main()
