BASE=['python3','python3-gi','python3-gi-cairo','python3-pil','gir1.2-gtk-3.0','libnotify-bin','dconf-cli']
BY_GROUP={
 'workspaces':['python3-xlib','xdg-user-dirs','zenity'],
 'rain':['mpv','ffmpeg','socat','wmctrl','xterm','build-essential','libx11-dev','libxext-dev','libxrender-dev'],
 'themes':['gtk2-engines-murrine','gnome-themes-extra'],
 'preferences':['fonts-ubuntu','fonts-dejavu'],
 'terminal':['cool-retro-term','xterm'],
 'relax':['mpv','celluloid','zenity'],
}
def packages(groups):return sorted(set(BASE)|{p for g in groups for p in BY_GROUP.get(g,[])})
