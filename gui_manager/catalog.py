from pathlib import Path
import ast,json
ROOT=Path(__file__).resolve().parents[1]
# id: Portuguese, English, required components
COMPONENTS={
 'icons':('Ícones de aplicativos','Application icons',()),
 'system':('Ícones e indicadores do sistema','System icons and indicators',('icons','themes')),
 'themes':('Temas de janelas e aplicativos','Desktop and application themes',()),
 'cursor':('Cursor','Cursor',()),
 'panel':('Painel, menu e favoritos','Panel, menu and favorites',()),
 'photo':('Atualização da foto de perfil','Profile photo refresh',()),
 'workspaces':('Espaços, arquivos e fundos independentes','Independent workspaces, files and backgrounds',()),
 'rain':('Rain e fundos em vídeo','Rain and video wallpapers',('workspaces',)),
 'folder_colors':('Seletor de cores das pastas','Folder color picker',('icons','system')),
 'nemo':('Nemo e ações de arquivos','Nemo and file actions',()),
 'terminal':('Perfil visual do terminal','Terminal appearance',()),
 'relax':('Vídeo em tela cheia e atalho Relax','Fullscreen video and Relax shortcut',()),
 'flatpak':('Correções de fontes Flatpak','Flatpak font fixes',()),
 'autostart':('Inicialização opcional de aplicativos','Optional application autostart',()),
 'preferences':('Fontes, atalhos, gestos e outras preferências','Fonts, shortcuts, gestures and other preferences',()),
}
EXTENSIONS={'photo':['gruvbox-profile-photo@gruvbox-cinnamon'], 'system':['gruvbox-microphone-colors@gruvbox-cinnamon','gruvbox-mintupdate-colors@gruvbox-cinnamon','gruvbox-system-colors@gruvbox-cinnamon']}
AGGREGATE='/org/cinnamon/enabled-extensions'
def array(raw):
 if raw is None:return []
 raw=raw.strip()
 if raw.startswith('@as '):raw=raw[4:]
 value=ast.literal_eval(raw)
 if not isinstance(value,list) or not all(isinstance(x,str) for x in value):raise ValueError('Lista inválida')
 return value

def closure(selected):
 result=set(selected)
 if result-set(COMPONENTS):raise ValueError('Componente desconhecido')
 while True:
  added={d for c in result for d in COMPONENTS[c][2]}
  if added<=result:return result
  result|=added

def unit_group(target):
 if target=='.local/bin/xwinwrap':return 'rain'
 if target in ('.local/share/gruvbox-cinnamon/manage.py','.local/bin/gruvbox-desinstalar'):return 'legacy_core'
 if 'Gruvbox-Pastas-Coloridas-' in target or 'folder_colors.py' in target or 'cor-pastas' in target or target in ('escolher-cor-pastas.sh','folders-color-chooser.sh'):return 'folder_colors'
 if 'Gruvbox-Sistema-Colorido' in target or any(x in target for x in ['gruvbox-microphone-colors@','gruvbox-mintupdate-colors@','gruvbox-system-colors@']):return 'system'
 if 'Gruvbox-Plus-Dark' in target:return 'icons'
 if '.icons/' in target:return 'cursor'
 if '.themes/' in target or target in ('.gtkrc-2.0','.config/gtk-3.0/gtk.css','.config/gtk-2.0/gtkfilechooser.ini'):return 'themes'
 if 'profile-photo@' in target:return 'photo'
 if '.var/app/' in target or '/flatpak/overrides/' in target:return 'flatpak'
 if 'terminal' in target or target.endswith('/cool-retro-term.desktop'):return 'terminal'
 if target.endswith('/Relax.desktop') or 'gruvbox-video-tela-cheia' in target:return 'relax'
 if target.startswith('.config/autostart/') and not any(x in target for x in ('espacos-de-trabalho','video-wallpaper')):return 'autostart'
 if any(x in target for x in ('raincarroof','video-wallpaper','/rain/','/rain.desktop')):return 'rain'
 if any(x in target for x in ('/espacos/','espacos-de-trabalho','wallpapers-por-espaco','copiar-entre-areas')):return 'workspaces'
 if '/nemo/' in target:return 'nemo'
 if '/spices/' in target or '/menus/' in target or '/desktop-directories/' in target:return 'panel'
 raise ValueError('Unidade sem grupo: '+target)

def setting_group(key):
 name=key.rsplit('/',1)[-1]
 if key==AGGREGATE:return 'aggregate'
 if 'icon-theme' in name:return 'icons'
 if 'cursor-' in name:return 'cursor'
 if name in ('gtk-theme','gtk-theme-backup') or key=='/org/cinnamon/theme/name' or key.endswith('/wm/preferences/theme'):return 'themes'
 if '/applications/terminal/' in key or name=='terminal':return 'terminal'
 if '/custom-keybindings/custom0/' in key:return 'relax'
 if '/custom-keybindings/custom1/' in key:return 'rain'
 if name in ('num-workspaces','number-workspaces','workspace-names','workspace-name-overrides') or '/desktop/background/' in key or '/org/cinnamon/background/' in key or '/org/nemo/desktop/' in key:return 'workspaces'
 if name in ('enabled-applets','next-applet-id','favorite-apps') or name.startswith(('panel','app-menu','system-icon')):return 'panel'
 if key.startswith('/org/blueman/'):return 'system'
 if key.startswith('/org/nemo/'):return 'nemo'
 return 'preferences'

def units(root=ROOT):
 return [(u,unit_group(u['target'])) for u in json.loads((root/'manifest.json').read_text())['units']]
