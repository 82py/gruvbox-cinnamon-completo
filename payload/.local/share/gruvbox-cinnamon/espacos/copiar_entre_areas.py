#!/usr/bin/python3
"""Cópia entre pastas fixas, sem remover nem sobrescrever arquivos."""
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import threading
from urllib.parse import unquote, urlsplit

BASE = Path(__file__).resolve().parent


def freeze_sources(values):
    result = []
    for value in values:
        if value.startswith('file:'):
            uri = urlsplit(value)
            if uri.netloc not in ('', 'localhost'):
                raise ValueError('Somente arquivos locais podem ser copiados.')
            value = unquote(uri.path)
        elif '://' in value:
            raise ValueError('Somente arquivos locais podem ser copiados.')
        path = Path(value)
        # Resolve o ponteiro da área agora, sem seguir o próprio atalho selecionado.
        path = path.parent.resolve(strict=True) / path.name
        path.lstat()
        if path not in result:
            result.append(path)
    return result


def candidate(parent, name, number, directory):
    if not number:
        return parent / name
    p = Path(name)
    stem, suffix = (name, '') if directory else (p.stem, p.suffix)
    return parent / f'{stem} (cópia {number}){suffix}'


def copy_one(source, parent, progress=lambda text: None):
    info = source.lstat()
    directory = stat.S_ISDIR(info.st_mode)
    if not (directory or stat.S_ISREG(info.st_mode) or stat.S_ISLNK(info.st_mode)):
        raise ValueError(f'Item especial não copiado: {source}')
    if directory and (parent == source or source in parent.parents):
        raise ValueError('Não é possível copiar uma pasta para dentro dela mesma.')
    number = 0
    while True:
        dest = candidate(parent, source.name, number, directory)
        try:
            if directory:
                dest.mkdir(mode=0o700)
                fd = None
            elif stat.S_ISLNK(info.st_mode):
                link = os.readlink(source)
                # Um atalho relativo continua apontando para o mesmo lugar.
                if not os.path.isabs(link):
                    link = os.path.normpath(str(source.parent / link))
                dest.symlink_to(link)
                fd = None
            else:
                fd = os.open(dest, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            break
        except FileExistsError:
            number += 1
    progress(source.name)
    try:
        if directory:
            for item in source.iterdir():
                copy_one(item, dest, progress)
            shutil.copystat(source, dest, follow_symlinks=False)
        elif fd is not None:
            with os.fdopen(fd, 'wb') as output:
                source_fd = os.open(source, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
                with os.fdopen(source_fd, 'rb') as input_file:
                    if not stat.S_ISREG(os.fstat(input_file.fileno()).st_mode):
                        raise ValueError('O arquivo de origem mudou durante a cópia.')
                    shutil.copyfileobj(input_file, output, 1024 * 1024)
                output.flush()
                os.fsync(output.fileno())
            shutil.copystat(source, dest, follow_symlinks=False)
        return dest
    except Exception as exc:
        raise RuntimeError(f'{exc}\nCópia incompleta preservada em: {dest}') from exc


def copy_batch(sources, destination, progress=lambda text: None):
    destination = Path(destination).resolve(strict=True)
    if not destination.is_dir():
        raise ValueError('A pasta de destino não está disponível.')
    # Valida todas as seleções antes de começar a escrever.
    for source in sources:
        if source.parent == destination:
            raise ValueError('Este item já está nessa área. Escolha outra área.')
        if source.is_dir() and not source.is_symlink():
            if destination == source or source in destination.parents:
                raise ValueError('O destino fica dentro de uma das pastas selecionadas.')
    done, errors = [], []
    for source in sources:
        try:
            done.append(str(copy_one(source, destination, progress)))
        except Exception as exc:
            errors.append(f'{source.name}: {exc}')
    return done, errors


def main():
    import gi
    gi.require_version('Gtk', '3.0')
    gi.require_version('PangoCairo', '1.0')
    from gi.repository import Gtk, Gdk, GLib, GdkPixbuf, Pango, PangoCairo

    class Preview(Gtk.DrawingArea):
        """Wallpaper e amostra dos ícones; não troca áreas nem captura janelas."""
        def __init__(self, owner, folder, number):
            super().__init__()
            self.owner, self.folder, self.number = owner, folder, number
            self.set_size_request(304, 190)
            self.connect('draw', self.paint)
            self.background = None
            self.key = None
            self.items = []
            self.entry = {}
            self.refresh()

        def refresh(self):
            try:
                data = json.loads((BASE / 'fundos.json').read_text())
                self.entry = data.get('spaces', {}).get(str(self.number), {})
            except (OSError, ValueError):
                self.entry = {}
            try:
                files = sorted((p for p in self.folder.iterdir() if not p.name.startswith('.')), key=lambda p: p.name.casefold())
                self.items = [(p.name, 'folder' if stat.S_ISDIR(p.lstat().st_mode) else 'emblem-symbolic-link' if p.is_symlink() else 'text-x-generic') for p in files[:6]]
            except OSError:
                self.items = []
            path = Path(unquote(urlsplit(self.entry.get('image', '')).path))
            try:
                key = (str(path), path.stat().st_mtime_ns)
                if key != self.key:
                    self.background = GdkPixbuf.Pixbuf.new_from_file_at_scale(str(path), 608, 380, True)
                    self.key = key
            except (OSError, GLib.Error):
                self.background = None
                self.key = None
            self.queue_draw()

        def paint(self, widget, cr):
            width, height = self.get_allocated_width(), self.get_allocated_height()
            cr.set_source_rgb(.025, .075, .08); cr.paint()
            video = self.entry.get('mode') == 'raincarroof'
            pix = self.owner.video_preview if video and self.owner.video_preview and self.entry.get('video', '') == str(getattr(self.owner, 'preview_video', '')) else self.background
            if pix:
                pw, ph = pix.get_width(), pix.get_height()
                fit = 'zoom' if video else self.entry.get('fit', 'zoom')
                scale = min(width / pw, height / ph) if fit == 'scaled' else max(width / pw, height / ph)
                cr.save()
                cr.rectangle(0, 0, width, height); cr.clip()
                cr.translate((width - pw * scale) / 2, (height - ph * scale) / 2)
                cr.scale(scale, scale)
                Gdk.cairo_set_source_pixbuf(cr, pix, 0, 0); cr.paint()
                cr.restore()
            theme = Gtk.IconTheme.get_default()
            for index, (name, icon_name) in enumerate(self.items):
                x, y = 8 + (index // 3) * 72, 12 + (index % 3) * 53
                try:
                    icon = theme.load_icon(icon_name, 22, Gtk.IconLookupFlags.FORCE_SIZE)
                    Gdk.cairo_set_source_pixbuf(cr, icon, x + 22, y); cr.paint()
                except GLib.Error:
                    pass
                layout = PangoCairo.create_layout(cr)
                layout.set_font_description(Pango.FontDescription('Sans 7'))
                layout.set_width(66 * Pango.SCALE)
                layout.set_ellipsize(Pango.EllipsizeMode.END)
                layout.set_alignment(Pango.Alignment.CENTER)
                layout.set_text(name, -1)
                cr.move_to(x + 1, y + 25); cr.set_source_rgba(0, 0, 0, .9); PangoCairo.show_layout(cr, layout)
                cr.move_to(x, y + 24); cr.set_source_rgb(1, 1, 1); PangoCairo.show_layout(cr, layout)
            if video:
                cr.set_source_rgba(0, 0, 0, .7); cr.rectangle(width - 115, height - 26, 115, 26); cr.fill()
                layout = PangoCairo.create_layout(cr)
                layout.set_font_description(Pango.FontDescription('Sans 9'))
                layout.set_text('▶ Rain', -1)
                cr.move_to(width - 106, height - 21); cr.set_source_rgb(1, 1, 1); PangoCairo.show_layout(cr, layout)
            return False

    class Window(Gtk.Window):
        def __init__(self):
            super().__init__(title='Copiar entre áreas')
            self.set_default_size(680, 570)
            self.set_border_width(20)
            self.stick()
            self.busy = False
            self.sources = []
            self.previews = []
            self.video_preview = None
            self.video_loading = False
            self.video_attempted = False
            self.connect('delete-event', self.closing)
            self.connect('destroy', self.destroyed)
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
            self.add(box)
            intro = Gtk.Label(label='Arraste arquivos ou pastas para a área de destino.\nOs originais ficam onde estão. Nomes repetidos ganham “cópia”.')
            intro.set_line_wrap(True)
            box.pack_start(intro, False, False, 0)
            self.grid = Gtk.Grid(column_spacing=12, row_spacing=12)
            box.pack_start(self.grid, True, True, 0)
            self.status = Gtk.Label(label='Pronto para copiar.')
            self.status.set_line_wrap(True)
            self.status.set_max_width_chars(68)
            box.pack_start(self.status, False, False, 0)
            try:
                config = json.loads((BASE / 'configuracao.json').read_text())
                if not config.get('enabled'):
                    raise ValueError('As áreas independentes estão desativadas.')
                self.folders = [Path(p).resolve(strict=True) for p in config['folders']]
                args = sys.argv[1:]
                if args and args[0] == '--':
                    args = args[1:]
                self.sources = freeze_sources(args)
                if self.sources:
                    self.status.set_text(f'{len(self.sources)} item(ns) selecionado(s). Clique na área de destino.')
                for i, folder in enumerate(self.folders):
                    button = Gtk.Button()
                    card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
                    card.set_border_width(6)
                    preview = Preview(self, folder, i + 1)
                    self.previews.append(preview)
                    card.pack_start(preview, True, True, 0)
                    caption = Gtk.Label(label=f'Área {i + 1}')
                    card.pack_start(caption, False, False, 0)
                    button.add(card)
                    button.get_accessible().set_name(f'Copiar para a área {i + 1}')
                    button.set_hexpand(True)
                    button.set_vexpand(True)
                    button.set_tooltip_text(str(folder))
                    button.connect('clicked', self.clicked, folder, i + 1)
                    button.drag_dest_set(Gtk.DestDefaults.ALL, [Gtk.TargetEntry.new('text/uri-list', 0, 0)], Gdk.DragAction.COPY)
                    button.connect('drag-data-received', self.dropped, folder, i + 1)
                    self.grid.attach(button, i % 2, i // 2, 1, 1)
                self.refresh_previews()
                self.refresh_timer = GLib.timeout_add_seconds(2, self.refresh_previews)
            except Exception as exc:
                self.status.set_text(str(exc))
                self.grid.set_sensitive(False)

        def destroyed(self, *args):
            if getattr(self, 'refresh_timer', None):
                GLib.source_remove(self.refresh_timer)
                self.refresh_timer = None
            if Gtk.main_level():
                Gtk.main_quit()

        def refresh_previews(self):
            for preview in self.previews:
                preview.refresh()
            if any(p.entry.get('mode') == 'raincarroof' for p in self.previews) and not self.video_attempted:
                self.video_attempted = True
                self.load_video_preview()
            return True

        def load_video_preview(self):
            import subprocess
            if not shutil.which('ffmpeg'):
                return
            data = json.loads((BASE / 'fundos.json').read_text())
            choices = [e.get('video','') for e in data['spaces'].values() if e.get('mode') == 'raincarroof']
            video = next((Path(v) for v in choices if Path(v).is_file()), Path('/nonexistent-video'))
            self.preview_video = video
            if not video.is_file():
                return
            def work():
                try:
                    result = subprocess.run(['ffmpeg', '-v', 'error', '-ss', '2', '-i', str(video), '-frames:v', '1', '-vf', 'scale=608:380:force_original_aspect_ratio=increase,crop=608:380', '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True, timeout=15)
                    if result.returncode == 0:
                        GLib.idle_add(self.video_ready, result.stdout)
                except (OSError, subprocess.TimeoutExpired):
                    pass
            threading.Thread(target=work, daemon=True).start()

        def video_ready(self, data):
            try:
                loader = GdkPixbuf.PixbufLoader.new_with_type('png')
                loader.write(data); loader.close()
                self.video_preview = loader.get_pixbuf()
                for preview in self.previews:
                    preview.queue_draw()
            except GLib.Error:
                pass
            return False

        def closing(self, *args):
            if self.busy:
                self.status.set_text('Aguarde a cópia terminar antes de fechar esta janela.')
            return self.busy

        def clicked(self, button, folder, number):
            if self.sources:
                self.start_copy(self.sources, folder, number)
            else:
                self.status.set_text('Arraste um arquivo ou pasta para o botão da área desejada.')

        def dropped(self, button, context, x, y, selection, info, timestamp, folder, number):
            try:
                sources = freeze_sources(selection.get_uris() or [])
                if not sources:
                    raise ValueError('Nenhum arquivo local foi recebido.')
                accepted = self.start_copy(sources, folder, number)
                Gtk.drag_finish(context, accepted, False, timestamp)
            except Exception as exc:
                Gtk.drag_finish(context, False, False, timestamp)
                self.status.set_text(str(exc))

        def start_copy(self, sources, folder, number):
            if self.busy:
                return False
            try:
                config = json.loads((BASE / 'configuracao.json').read_text())
                if not config.get('enabled'):
                    raise ValueError('As áreas independentes estão desativadas. Nenhuma cópia foi iniciada.')
            except Exception as exc:
                self.status.set_text(str(exc))
                return False
            self.busy = True
            self.grid.set_sensitive(False)
            self.status.set_text(f'Copiando para a área {number}…')
            def progress(name):
                GLib.idle_add(self.status.set_text, f'Área {number}: copiando {name}')
            def work():
                try:
                    done, errors = copy_batch(sources, folder, progress)
                except Exception as exc:
                    done, errors = [], [str(exc)]
                GLib.idle_add(self.finished, number, done, errors)
            threading.Thread(target=work, daemon=False).start()
            return True

        def finished(self, number, done, errors):
            self.busy = False
            self.grid.set_sensitive(True)
            if errors:
                self.status.set_text(f'{len(done)} item(ns) copiado(s). Houve um problema; os originais foram mantidos.')
                dialog = Gtk.MessageDialog(transient_for=self, modal=True, message_type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.CLOSE, text='A cópia não foi concluída para todos os itens.')
                dialog.format_secondary_text('\n\n'.join(errors))
                dialog.run()
                dialog.destroy()
            else:
                self.status.set_text(f'{len(done)} item(ns) copiado(s) para a área {number}. Originais preservados.')
            return False

    window = Window()
    window.show_all()
    Gtk.main()


if __name__ == '__main__':
    main()
