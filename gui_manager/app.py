"""Interface GTK pessoal. Abrir a janela e revisar planos não aplica mudanças."""
from pathlib import Path
import copy,json,os,shutil,subprocess,threading,time
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk,GLib,Gdk
from .catalog import ROOT,COMPONENTS,closure,units
from .profiles import default_profile,load,export
from .engine import Manager,raw

class Window(Gtk.Window):
 def __init__(self,manager=None,profile=None):
  super().__init__(title='Gruvbox Manager')
  self.manager=manager or Manager();self.profile=profile or default_profile(self.manager.home,self.manager.sandbox)
  if profile is None and self.manager.read_registry()['groups']:self.profile['components']=self.manager.read_registry()['groups']
  self.lang=self.profile.get('language','pt_BR');self.busy=False;self.cancel=threading.Event();self.last_progress=0;self.checks={};self.guard=False;self.snapshot_ids=[]
  self.set_default_size(1100,820);self.set_border_width(18)
  self.connect('delete-event',self.closing);self.connect('destroy',lambda *_:Gtk.main_quit() if Gtk.main_level() else None)
  css=Gtk.CssProvider();css.load_from_data(b'window { background-color:#282828; color:#ebdbb2; } .title {font-size:25px;font-weight:bold;color:#fabd2f;} .muted {color:#bdae93;} .warning {color:#fabd2f;} button.suggested-action {background-image:none;background-color:#458588;color:#fbf1c7;}')
  Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),css,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
  self.build()
 def t(self,pt,en):return en if self.lang=='en' else pt
 def label(self,text,style=None):
  widget=Gtk.Label(label=text,xalign=0);widget.set_line_wrap(True)
  if style:widget.get_style_context().add_class(style)
  return widget
 def tab_label(self,text):return Gtk.Label(label=text)
 def button(self,pt,en,callback):
  b=Gtk.Button(label=self.t(pt,en));b.connect('clicked',callback);return b
 def box(self,vertical=True,spacing=12):return Gtk.Box(orientation=Gtk.Orientation.VERTICAL if vertical else Gtk.Orientation.HORIZONTAL,spacing=spacing)
 def scroll(self,child):
  scroll=Gtk.ScrolledWindow();scroll.set_policy(Gtk.PolicyType.AUTOMATIC,Gtk.PolicyType.AUTOMATIC);scroll.add(child);return scroll
 def build(self):
  old=self.get_child()
  if old:self.remove(old);old.destroy()
  root=self.box();self.add(root)
  head=self.box(False);root.pack_start(head,False,False,0)
  head.pack_start(self.label('Gruvbox Manager','title'),True,True,0)
  languages=Gtk.ComboBoxText();languages.append('pt_BR','Português (Brasil)');languages.append('en','English');languages.set_active_id(self.lang);languages.connect('changed',self.language_changed);head.pack_end(languages,False,False,0)
  self.banner=self.label(self.t('Abrir e revisar não altera seu Cinnamon.','Opening and reviewing does not change Cinnamon.'),'muted');root.pack_start(self.banner,False,False,0)
  actionrow=self.box(False);root.pack_start(actionrow,False,False,0)
  actionrow.pack_start(self.label(self.t('Operação','Operation')),False,False,0)
  self.operation=Gtk.ComboBoxText()
  for key,pt,en in [('apply','Instalar / personalizar','Install / customize'),('uninstall','Desinstalar componentes','Uninstall components'),('restore','Restaurar ponto anterior','Restore a previous point')]:self.operation.append(key,self.t(pt,en))
  self.operation.set_active_id('apply');self.operation.connect('changed',self.mode_changed);actionrow.pack_start(self.operation,False,False,0)
  self.points_combo=Gtk.ComboBoxText();actionrow.pack_start(self.points_combo,True,True,0);self.points_combo.connect('changed',self.point_changed)
  self.notebook=Gtk.Notebook();root.pack_start(self.notebook,True,True,0)
  components=self.box();components.set_border_width(14)
  self.selection_hint=self.label(self.t('Marcado: instalar ou personalizar. Desmarcado: manter como está. Dependências são selecionadas juntas.','Checked: install or customize. Unchecked: leave unchanged. Dependencies are selected together.'))
  components.pack_start(self.selection_hint,False,False,0)
  rows=self.box(spacing=8)
  installed=set(self.manager.read_registry()['groups'])
  for key,(pt,en,deps) in COMPONENTS.items():
   row=self.box(False);check=Gtk.CheckButton(label=self.t(pt,en));check.set_active(key in self.profile['components']);check.connect('toggled',self.component_toggled,key);self.checks[key]=check;row.pack_start(check,True,True,0)
   note=self.t('Gerenciado','Managed') if key in installed else ''
   if deps:note+=(' · ' if note else '')+self.t('Requer: ','Requires: ')+', '.join(COMPONENTS[d][0 if self.lang!='en' else 1] for d in deps)
   row.pack_end(self.label(note,'muted'),False,False,0);rows.pack_start(row,False,False,0)
  components.pack_start(self.scroll(rows),True,True,0)
  tools=self.box(False)
  tools.pack_start(self.button('Selecionar tudo','Select all',lambda *_:self.select_all(True)),False,False,0)
  tools.pack_start(self.button('Manter tudo','Leave all unchanged',lambda *_:self.select_all(False)),False,False,0)
  components.pack_start(tools,False,False,0);self.notebook.append_page(components,self.tab_label(self.t('Componentes','Components')))
  self.custom_page=self.customization();self.notebook.append_page(self.scroll(self.custom_page),self.tab_label(self.t('Aparência e controles','Appearance and controls')))
  self.workspace_page=self.workspace_options();self.notebook.append_page(self.scroll(self.workspace_page),self.tab_label(self.t('Espaços e mídias','Workspaces and media')))
  profiles=self.profile_options();self.notebook.append_page(profiles,self.tab_label(self.t('Perfis e segurança','Profiles and safety')))
  self.log=Gtk.TextView();self.log.set_editable(False);self.log.set_wrap_mode(Gtk.WrapMode.WORD_CHAR);self.notebook.append_page(self.scroll(self.log),self.tab_label(self.t('Registro','Log')))
  self.status=self.label(self.t('Pronto. Nenhuma mudança aplicada.','Ready. No changes applied.'));root.pack_start(self.status,False,False,0)
  bottom=self.box(False);root.pack_start(bottom,False,False,0)
  bottom.pack_start(self.button('Verificar requisitos','Check requirements',self.check_requirements),False,False,0)
  self.deps_button=self.button('Instalar dependências…','Install dependencies…',self.install_dependencies);bottom.pack_start(self.deps_button,False,False,0)
  self.cancel_button=self.button('Cancelar operação','Cancel operation',lambda *_:self.cancel.set());self.cancel_button.set_sensitive(False);bottom.pack_end(self.cancel_button,False,False,0)
  self.review_button=self.button('Revisar alterações…','Review changes…',self.review);self.review_button.get_style_context().add_class('suggested-action');bottom.pack_end(self.review_button,False,False,0)
  self.refresh_points();self.show_all();self.points_combo.set_visible(False)
  if self.manager.sandbox:self.banner.set_text(self.t('MODO DE TESTE · Todas as operações usam uma pasta temporária.','TEST MODE · All operations use a temporary home folder.'))
 def language_changed(self,combo):
  selected=combo.get_active_id()
  if selected!=self.lang:
   self.profile['components']=self.selected();self.lang=selected;self.profile['language']=selected;self.build()
 def selected(self):return [key for key,b in self.checks.items() if b.get_active()]
 def dependencies(self):
  deps={key:set(value[2]) for key,value in COMPONENTS.items()}
  legacy=self.profile['workspaces'].get('legacy_coupled_rain') or self.manager.read_registry().get('legacy_coupled_rain')
  if legacy:deps['workspaces'].add('rain')
  return deps
 def select_all(self,value):
  self.guard=True
  for b in self.checks.values():
   if b.get_sensitive():b.set_active(value)
  self.guard=False;self.profile['components']=self.selected()
 def component_toggled(self,button,key):
  if self.guard:return
  self.guard=True
  try:
   mode=self.operation.get_active_id();selected=set(self.selected());deps=self.dependencies()
   if mode=='apply':
    if button.get_active():
     while True:
      expanded=selected|{d for k in selected for d in deps[k]}
      if expanded==selected:break
      selected=expanded
    else:
     while True:
      reduced={x for x in selected if deps[x]<=selected}
      if reduced==selected:break
      selected=reduced
   elif mode=='uninstall' and button.get_active():
    installed=set(self.manager.read_registry()['groups'])
    while True:
     added={x for x in installed if deps[x]&selected}
     if added<=selected:break
     selected|=added
   for name,b in self.checks.items():b.set_active(name in selected)
   if mode=='apply':self.profile['components']=sorted(selected)
  finally:self.guard=False
 def mode_changed(self,*_):
  mode=self.operation.get_active_id();self.points_combo.set_visible(mode=='restore');self.custom_page.set_sensitive(mode=='apply');self.workspace_page.set_sensitive(mode=='apply')
  if mode=='apply':allowed=set(COMPONENTS);selected=set(self.profile['components'])
  elif mode=='uninstall':allowed=set(self.manager.read_registry()['groups']);selected=allowed
  else:
   pid=self.points_combo.get_active_id();point=next((p for p in self.manager.points() if p['id']==pid),None);allowed=set(point['groups'])&set(COMPONENTS) if point else set();selected=allowed
  self.guard=True
  for key,b in self.checks.items():b.set_sensitive(key in allowed);b.set_active(key in selected)
  self.guard=False
  self.selection_hint.set_text(self.t('Marcado: instalar/personalizar. Desmarcado: manter como está.','Checked: install/customize. Unchecked: leave unchanged.') if mode=='apply' else self.t('Marcado: restaurar/desinstalar. Desmarcado: manter. Seus arquivos e vídeos nunca são apagados.','Checked: restore/uninstall. Unchecked: keep. Your files and videos are never deleted.'))
 def point_changed(self,*_):
  if self.operation.get_active_id()=='restore':self.mode_changed()
 def refresh_points(self):
  self.points_combo.remove_all()
  for point in self.manager.points():self.points_combo.append(point['id'],point['created'][:19].replace('T',' ')+' · '+point['action']+' · '+point['status'])
  self.points_combo.set_active(0)
 def set_pref(self,key,value):self.profile['settings'][key]=raw(value)
 def pref(self,key,default):
  try:return GLib.Variant.parse(None,self.profile['settings'].get(key,raw(default)),None,None).unpack()
  except (GLib.Error,TypeError):return default
 def combo_option(self,container,pt,en,values,current,callback,labels=None):
  row=self.box(False);row.pack_start(self.label(self.t(pt,en)),True,True,0);combo=Gtk.ComboBoxText()
  for value in dict.fromkeys([current,*values]):combo.append(str(value),(labels or {}).get(value,str(value)))
  combo.set_active_id(str(current));combo.connect('changed',lambda c:callback(c.get_active_id()));row.pack_end(combo,False,False,0);container.pack_start(row,False,False,0);return combo
 def switch_option(self,container,pt,en,current,callback):
  row=self.box(False);row.pack_start(self.label(self.t(pt,en)),True,True,0);switch=Gtk.Switch(active=current);switch.connect('notify::active',lambda w,_:callback(w.get_active()));row.pack_end(switch,False,False,0);container.pack_start(row,False,False,0)
 def customization(self):
  box=self.box();box.set_border_width(14)
  box.pack_start(self.label(self.t('Os valores atuais são o padrão. Alterações só são aplicadas aos componentes marcados.','Current values are the default. Changes only apply to checked components.')),False,False,0)
  def themes(base):return [p.name for p in base.iterdir() if p.is_dir()] if base.is_dir() else []
  def icon_changed(value):
   for schema in ('cinnamon','gnome'):self.set_pref('/org/'+schema+'/desktop/interface/icon-theme',value)
  self.combo_option(box,'Tema de ícones','Icon theme',themes(ROOT/'payload/.local/share/icons')+themes(self.manager.home/'.local/share/icons'),self.pref('/org/cinnamon/desktop/interface/icon-theme','Gruvbox-Sistema-Colorido'),icon_changed)
  self.combo_option(box,'Tema do painel e menu','Panel and menu theme',themes(ROOT/'payload/.themes')+themes(self.manager.home/'.themes'),self.pref('/org/cinnamon/theme/name','Gruvbox-Dark-BL-MOD-Sistema-Colorido'),lambda v:self.set_pref('/org/cinnamon/theme/name',v))
  def gtk_changed(value):
   for schema in ('cinnamon','gnome'):self.set_pref('/org/'+schema+'/desktop/interface/gtk-theme',value)
  self.combo_option(box,'Tema dos aplicativos','Application theme',themes(ROOT/'payload/.themes')+themes(self.manager.home/'.themes'),self.pref('/org/cinnamon/desktop/interface/gtk-theme','Mint-L-Dark-Sand'),gtk_changed)
  def cursor_changed(value):
   for schema in ('cinnamon','gnome'):self.set_pref('/org/'+schema+'/desktop/interface/cursor-theme',value)
  self.combo_option(box,'Cursor','Cursor',themes(ROOT/'payload/.icons')+themes(self.manager.home/'.icons'),self.pref('/org/cinnamon/desktop/interface/cursor-theme','Gruvbox_Cursors_Dark'),cursor_changed)
  colors=['keep','black','blue','caramel','citron','firebrick','gold','green','grey','highland','jade','lavender','lime','olive','orange','pistachio','plasma','pumpkin','purple','red','rust','sapphire','tomato','violet','white','yellow']
  self.combo_option(box,'Cor das pastas','Folder color',colors,self.profile.get('folder_color','keep'),lambda v:self.profile.update(folder_color=v),{'keep':self.t('Manter atual','Keep current')})
  for key,pt,en in [('font-name','Fonte da interface','Interface font'),('document-font-name','Fonte dos documentos','Document font'),('monospace-font-name','Fonte monoespaçada','Monospace font')]:
   row=self.box(False);row.pack_start(self.label(self.t(pt,en)),True,True,0);button=Gtk.FontButton();button.set_font(self.pref('/org/cinnamon/desktop/interface/'+key,'Ubuntu 10'));button.connect('font-set',lambda w,k=key:self.font_changed(k,w.get_font()));row.pack_end(button,False,False,0);box.pack_start(row,False,False,0)
  row=self.box(False);row.pack_start(self.label(self.t('Volume inicial do Rain','Rain startup volume')),True,True,0);volume=Gtk.SpinButton.new_with_range(0,100,1);volume.set_value(self.profile['rain_volume']);volume.connect('value-changed',lambda w:self.profile.update(rain_volume=w.get_value()));row.pack_end(volume,False,False,0);box.pack_start(row,False,False,0)
  self.switch_option(box,'Preservar preferências atuais dos applets','Preserve current applet preferences',self.profile.get('preserve_spice_settings',True),lambda v:self.profile.update(preserve_spice_settings=v))
  self.switch_option(box,'Iniciar Rain sem som','Start Rain muted',self.profile['rain_muted'],lambda v:self.profile.update(rain_muted=v))
  self.switch_option(box,'Iniciar espaços ao entrar na sessão','Start workspaces at login',self.profile['autostart_workspaces'],lambda v:self.profile.update(autostart_workspaces=v))
  self.switch_option(box,'Iniciar bandeja Rain ao entrar','Start Rain tray at login',self.profile['autostart_rain'],lambda v:self.profile.update(autostart_rain=v))
  box.pack_start(self.button('Editar outras preferências…','Edit other preferences…',self.preferences_dialog),False,False,0)
  return box
 def font_changed(self,key,value):
  for schema in ('cinnamon','gnome'):self.set_pref('/org/'+schema+'/desktop/interface/'+key,value)
 def choose(self,entry,folder=False,video=False):
  dialog=Gtk.FileChooserDialog(title=self.t('Escolher pasta' if folder else 'Escolher arquivo','Choose folder' if folder else 'Choose file'),transient_for=self,action=Gtk.FileChooserAction.SELECT_FOLDER if folder else Gtk.FileChooserAction.OPEN)
  dialog.add_buttons(self.t('Cancelar','Cancel'),Gtk.ResponseType.CANCEL,self.t('Escolher','Choose'),Gtk.ResponseType.OK)
  if not folder:
   filt=Gtk.FileFilter();filt.set_name(self.t('Vídeos' if video else 'Imagens','Videos' if video else 'Images'))
   for ext in (['mp4','webm','mkv','mov','avi','m4v'] if video else ['png','jpg','jpeg','webp','bmp']):filt.add_pattern('*.'+ext);filt.add_pattern('*.'+ext.upper())
   dialog.add_filter(filt)
  if dialog.run()==Gtk.ResponseType.OK:entry.set_text(dialog.get_filename())
  dialog.destroy()
 def workspace_options(self):
  box=self.box();box.set_border_width(14)
  box.pack_start(self.label(self.t('Quatro áreas independentes. As pastas existentes e os arquivos dentro delas são preservados. Vídeos e imagens são referenciados; não são copiados para o pacote.','Four independent areas. Existing folders and their contents are preserved. Videos and images are referenced, not copied into the package.')),False,False,0)
  self.switch_option(box,'Ativar separação de arquivos e fundos','Enable independent files and backgrounds',self.profile['workspaces'].get('enabled',True),lambda v:self.profile['workspaces'].update(enabled=v))
  from urllib.parse import unquote,urlsplit
  for index,space in enumerate(self.profile['workspaces']['spaces'],1):
   frame=Gtk.Frame(label=self.t('Área ','Workspace ')+str(index));inner=self.box(spacing=8);inner.set_border_width(12);frame.add(inner)
   for key,pt,en in [('folder','Pasta dos arquivos','Files folder'),('image','Imagem de fundo','Background image'),('video','Vídeo para loop','Looping video')]:
    row=self.box(False);row.pack_start(self.label(self.t(pt,en)),False,False,0);entry=Gtk.Entry();value=space[key]
    if key=='image' and value.startswith('file:'):value=unquote(urlsplit(value).path)
    entry.set_text(value);entry.set_hexpand(True)
    def changed(widget,e=space,k=key):
     value=widget.get_text().strip();e[k]=Path(value).expanduser().absolute().as_uri() if k=='image' and value else value
    entry.connect('changed',changed);row.pack_start(entry,True,True,0);row.pack_end(self.button('Escolher…','Choose…',lambda _,w=entry,k=key:self.choose(w,folder=k=='folder',video=k=='video')),False,False,0);inner.pack_start(row,False,False,0)
   row=self.box(False);mode=Gtk.ComboBoxText();mode.append('static',self.t('Imagem estática','Static image'));mode.append('raincarroof',self.t('Rain: vídeo em loop','Rain: looping video'));mode.set_active_id(space['mode']);mode.connect('changed',lambda w,e=space:e.update(mode=w.get_active_id()));row.pack_start(mode,True,True,0)
   fit=Gtk.ComboBoxText()
   for k,pt,en in [('scaled','Ajustar','Fit'),('zoom','Preencher','Fill'),('centered','Centralizar','Center'),('stretched','Esticar','Stretch'),('wallpaper','Repetir','Tile'),('spanned','Estender','Span'),('none','Nenhum','None')]:fit.append(k,self.t(pt,en))
   fit.set_active_id(space['fit']);fit.connect('changed',lambda w,e=space:e.update(fit=w.get_active_id()));row.pack_end(fit,False,False,0);inner.pack_start(row,False,False,0);box.pack_start(frame,False,False,0)
  return box
 def profile_options(self):
  box=self.box();box.set_border_width(14)
  text=self.t('Antes de cada operação, o gerenciador cria um ponto de restauração dos arquivos e preferências envolvidos. Seus documentos, vídeos, imagens e foto pessoal não são apagados nem incorporados ao instalador.','Before each operation, the manager creates a restore point for affected files and preferences. Documents, videos, images and your profile photo are not deleted or embedded in the installer.')
  box.pack_start(self.label(text),False,False,0)
  if self.profile['workspaces'].get('imported_from'):box.pack_start(self.label(self.t('Configuração existente detectada. As quatro pastas e suas mídias foram importadas como padrão.','Existing setup detected. Its four folders and media choices were imported as defaults.')) ,False,False,0)
  box.pack_start(self.label(self.t('A desinstalação desfaz mudanças feitas por este gerenciador. Uma personalização que já existia antes dele será restaurada, não apagada.','Uninstall undoes changes made by this manager. Personalization that existed before it is restored rather than deleted.')) ,False,False,0)
  self.switch_option(box,'Guardar cópia do instalador para manutenção offline','Keep installer copy for offline maintenance',self.profile.get('keep_installer',True),lambda v:self.profile.update(keep_installer=v))
  box.pack_start(self.button('Salvar perfil…','Save profile…',self.save_profile),False,False,0)
  box.pack_start(self.button('Importar perfil…','Import profile…',self.import_profile),False,False,0)
  box.pack_start(self.button('Ler novamente a configuração atual','Read current setup again',self.capture_current),False,False,0)
  box.pack_start(self.button('Usar cores e layout do pacote','Use package colors and layout',self.package_defaults),False,False,0)
  box.pack_start(self.button('Recuperar operação interrompida…','Recover interrupted operation…',self.recover),False,False,0)
  box.pack_start(self.button('Abrir pasta dos pontos de restauração','Open restore-point folder',lambda *_:subprocess.Popen(['xdg-open',str(self.manager.state)])),False,False,0)
  box.pack_start(self.label(self.t('O perfil é um arquivo de configuração com caminhos locais; não contém os vídeos. Trate-o como informação pessoal. Os pontos de restauração ficam na sua pasta de usuário e não são enviados ao GitHub.','A profile is a configuration file with local paths, not the videos themselves. Treat it as personal information. Restore points stay in your home folder and are not uploaded to GitHub.')) ,False,False,0)
  return box
 def save_profile(self,*_):
  d=Gtk.FileChooserDialog(title=self.t('Salvar perfil','Save profile'),transient_for=self,action=Gtk.FileChooserAction.SAVE);d.add_buttons(self.t('Cancelar','Cancel'),Gtk.ResponseType.CANCEL,self.t('Salvar','Save'),Gtk.ResponseType.OK);d.set_current_name('meu-perfil-gruvbox.json');d.set_do_overwrite_confirmation(True)
  if d.run()==Gtk.ResponseType.OK:
   try:self.profile['components']=self.selected();export(d.get_filename(),self.profile);self.status.set_text(self.t('Perfil salvo.','Profile saved.'))
   except Exception as e:self.error(e)
  d.destroy()
 def import_profile(self,*_):
  d=Gtk.FileChooserDialog(title=self.t('Importar perfil','Import profile'),transient_for=self,action=Gtk.FileChooserAction.OPEN);d.add_buttons(self.t('Cancelar','Cancel'),Gtk.ResponseType.CANCEL,self.t('Abrir','Open'),Gtk.ResponseType.OK)
  if d.run()==Gtk.ResponseType.OK:
   try:self.profile=load(d.get_filename());self.lang=self.profile.get('language',self.lang);self.build()
   except Exception as e:self.error(e)
  d.destroy()
 def package_defaults(self,*_):
  self.profile['settings']=json.loads((ROOT/'settings.json').read_text())
  self.profile['components']=list(COMPONENTS);self.profile['rain_volume']=35;self.profile['rain_muted']=True
  # Only appearance/layout defaults change here; folder and media choices stay local.
  self.build()
 def capture_current(self,*_):
  try:self.profile=default_profile(self.manager.home,self.manager.sandbox);self.build()
  except Exception as e:self.error(e)
 def preferences_dialog(self,*_):
  dialog=Gtk.Dialog(title=self.t('Outras preferências','Other preferences'),transient_for=self,modal=True);dialog.set_default_size(860,560);dialog.add_button(self.t('Fechar','Close'),Gtk.ResponseType.CLOSE)
  box=dialog.get_content_area();search=Gtk.SearchEntry();box.pack_start(search,False,False,6);store=Gtk.ListStore(str,str)
  def fill(*_):
   store.clear();term=search.get_text().lower()
   for key,value in sorted(self.profile['settings'].items()):
    if term in key.lower():
     try:v=GLib.Variant.parse(None,value,None,None).unpack();display=json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else str(v)
     except GLib.Error:display=value
     store.append([key,display])
  search.connect('search-changed',fill);fill();tree=Gtk.TreeView(model=store)
  for i,title in enumerate([self.t('Preferência','Preference'),self.t('Valor atual','Current value')]):renderer=Gtk.CellRendererText();tree.append_column(Gtk.TreeViewColumn(title,renderer,text=i))
  def edit(_,path,column):
   key=store[path][0];self.edit_preference(key);fill()
  tree.connect('row-activated',edit);box.pack_start(self.scroll(tree),True,True,0);box.pack_start(self.label(self.t('Clique duas vezes para editar. A prévia final mostra os componentes que serão alterados.','Double-click to edit. The final review shows which components will change.')),False,False,6);dialog.show_all();dialog.run();dialog.destroy()
 def edit_preference(self,key):
  value=GLib.Variant.parse(None,self.profile['settings'][key],None,None);unpacked=value.unpack();dialog=Gtk.Dialog(title=key.rsplit('/',1)[-1],transient_for=self,modal=True);dialog.set_default_size(600,260);dialog.add_buttons(self.t('Cancelar','Cancel'),Gtk.ResponseType.CANCEL,self.t('Guardar escolha','Keep choice'),Gtk.ResponseType.OK);box=dialog.get_content_area();box.pack_start(self.label(key),False,False,8)
  if isinstance(unpacked,bool):widget=Gtk.CheckButton(label=self.t('Ativado','Enabled'));widget.set_active(unpacked);extract=widget.get_active
  elif isinstance(unpacked,(int,float)):
   widget=Gtk.SpinButton.new_with_range(-2147483648,2147483647,1);widget.set_value(unpacked);extract=widget.get_value if isinstance(unpacked,float) else widget.get_value_as_int
  elif isinstance(unpacked,str):widget=Gtk.Entry();widget.set_text(unpacked);extract=widget.get_text
  else:
   widget=Gtk.TextView();widget.set_wrap_mode(Gtk.WrapMode.WORD_CHAR);widget.get_buffer().set_text(json.dumps(unpacked,ensure_ascii=False,indent=2));box.pack_start(self.label(self.t('Lista ou estrutura em JSON','List or structure as JSON')),False,False,6)
   def extract():
    buffer=widget.get_buffer();return json.loads(buffer.get_text(buffer.get_start_iter(),buffer.get_end_iter(),True))
  box.pack_start(widget,True,True,8);dialog.show_all()
  if dialog.run()==Gtk.ResponseType.OK:
   try:self.profile['settings'][key]=GLib.Variant(value.get_type_string(),extract()).print_(True)
   except Exception as e:self.error(e)
  dialog.destroy()
 def check_requirements(self,*_):
  try:self.manager.preflight(closure(self.selected()));self.status.set_text(self.t('Requisitos verificados. Nada foi alterado.','Requirements checked. Nothing changed.'))
  except Exception as e:self.error(e)
 def install_dependencies(self,*_):
  from .dependencies import packages
  selected=closure(self.selected());names=packages(selected);message=self.t('Instalar dependências de sistema? Esta ação usa a autenticação do administrador. O tema continua sendo instalado no seu usuário. Os pacotes de sistema não são removidos pela desinstalação do tema.','Install system dependencies? This uses administrator authentication. The theme itself remains a per-user installation. Theme uninstallation does not remove system packages.')+'\n\n'+', '.join(names)
  if not self.confirm(message,self.t('Instalar dependências','Install dependencies')):return
  self.run_worker(lambda:subprocess.run(['/usr/bin/pkexec','/usr/bin/apt-get','install','-y','--',*names],check=True),dependency=True)
 def review(self,*_):
  try:
   selected=self.selected();mode=self.operation.get_active_id()
   if not selected:raise ValueError(self.t('Selecione pelo menos um componente.','Select at least one component.'))
   if mode=='apply':
    profile=copy.deepcopy(self.profile);profile['components']=selected;plan=self.manager.plan(profile);preview=self.manager.preview(plan)
    message=self.t('Instalar ou personalizar os componentes marcados.','Install or customize checked components.')+'\n\n'+self.t('Componentes: ','Components: ')+str(len(preview['components']))+'\n'+self.t('Arquivos/configurações: ','Files/configuration: ')+str(preview['files'])+'\n'+self.t('Preferências: ','Preferences: ')+str(preview['settings'])+'\n\n'+self.t('Um ponto de restauração será criado antes de qualquer mudança. Nenhum documento ou vídeo será apagado.','A restore point will be created before any change. No document or video will be deleted.')+'\n\n'+self.t('Destinos:','Destinations:')+'\n'+'\n'.join(x['path'] for x in preview['targets'])
    operation=lambda:self.manager.apply(profile)
   elif mode=='uninstall':
    self.manager._validate_remaining(set(self.manager.read_registry()['groups'])-set(selected));message=self.t('Desfazer as alterações gerenciadas nos componentes marcados. Os demais componentes, documentos e mídias serão mantidos.','Undo managed changes to checked components. Other components, documents and media will be kept.')+'\n\n'+'\n'.join(COMPONENTS[k][0 if self.lang!='en' else 1] for k in selected);operation=lambda:self.manager.uninstall(selected)
   else:
    pid=self.points_combo.get_active_id()
    if not pid:raise ValueError(self.t('Nenhum ponto de restauração disponível.','No restore point available.'))
    message=self.t('Restaurar somente os componentes marcados ao estado anterior deste ponto. O estado de agora também será guardado.','Restore only checked components to the state before this point. The current state will also be backed up.')+'\n\n'+pid;operation=lambda:self.manager.restore_point(pid,selected)
   if self.confirm(message,self.t('Aplicar escolhas','Apply choices')):self.run_worker(operation)
  except Exception as e:self.error(e)
 def confirm(self,message,button):
  d=Gtk.Dialog(title=self.t('Revisão final','Final review'),transient_for=self,modal=True);d.set_default_size(800,600);d.add_buttons(self.t('Cancelar','Cancel'),Gtk.ResponseType.CANCEL,button,Gtk.ResponseType.OK);text=Gtk.TextView();text.set_editable(False);text.set_wrap_mode(Gtk.WrapMode.WORD_CHAR);text.get_buffer().set_text(message);d.get_content_area().pack_start(self.scroll(text),True,True,0);d.set_default_response(Gtk.ResponseType.CANCEL);d.show_all();ok=d.run()==Gtk.ResponseType.OK;d.destroy();return ok
 def recover(self,*_):
  pending=[p for p in self.manager.points() if p['status']=='applying']
  if not pending:self.status.set_text(self.t('Nenhuma operação interrompida.','No interrupted operation.'));return
  point=pending[-1]
  if self.confirm(self.t('Voltar ao estado anterior da operação interrompida?','Return to the state before the interrupted operation?')+'\n'+point['id'],self.t('Recuperar','Recover')):self.run_worker(lambda:self.manager.recover(point['id']))
 def run_worker(self,operation,dependency=False):
  if self.busy:return
  self.busy=True;self.cancel.clear();self.notebook.set_sensitive(False);self.operation.set_sensitive(False);self.review_button.set_sensitive(False);self.deps_button.set_sensitive(False);self.cancel_button.set_sensitive(not dependency);self.status.set_text(self.t('Executando…','Working…'))
  def progress(message):
   if self.cancel.is_set():raise RuntimeError(self.t('Operação cancelada.','Operation cancelled.'))
   now=time.monotonic()
   if now-self.last_progress>.08:self.last_progress=now;GLib.idle_add(self.show_progress,message)
  self.manager.progress=progress
  def work():
   try:result=operation();error=None
   except Exception as e:result=None;error=str(e)
   GLib.idle_add(self.done,result,error,dependency)
  threading.Thread(target=work,daemon=False).start()
 def show_progress(self,message):
  self.status.set_text(message);buffer=self.log.get_buffer();buffer.insert(buffer.get_end_iter(),message+'\n');return False
 def done(self,result,error,dependency=False):
  self.busy=False;self.notebook.set_sensitive(True);self.operation.set_sensitive(True);self.review_button.set_sensitive(True);self.deps_button.set_sensitive(True);self.cancel_button.set_sensitive(False);self.refresh_points();self.mode_changed()
  message=(self.t('Dependências instaladas. Verifique os requisitos novamente.','Dependencies installed. Check requirements again.') if dependency else self.t('Concluído. Ponto de restauração: ','Completed. Restore point: ')+str(result)+self.t('\nEncerre a sessão e entre novamente para concluir o carregamento do painel, menus e aplicativos.','\nLog out and back in to finish loading the panel, menus and applications.')) if not error else self.t('A operação não foi concluída: ','The operation did not complete: ')+error
  self.status.set_text(message);buffer=self.log.get_buffer();buffer.insert(buffer.get_end_iter(),message+'\n')
  if error:self.error(error)
  return False
 def error(self,error):
  self.status.set_text(str(error));dialog=Gtk.MessageDialog(transient_for=self,modal=True,message_type=Gtk.MessageType.ERROR,buttons=Gtk.ButtonsType.CLOSE,text=self.t('Não foi possível concluir','Could not complete'));dialog.format_secondary_text(str(error));dialog.run();dialog.destroy()
 def closing(self,*_):
  if self.busy:self.status.set_text(self.t('Aguarde terminar. Cancelar operação pede a restauração segura; não feche o processo à força.','Please wait. Cancel operation requests safe rollback; do not force-close the process.'))
  return self.busy
