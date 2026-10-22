// Avoid the stale fixed-URL avatar cache without replacing Cinnamon methods.
const Gio=imports.gi.Gio;
const GLib=imports.gi.GLib;
const St=imports.gi.St;
const AppletManager=imports.ui.appletManager;
let started=false, idle=0, settingsId=0, busId=0, record=null;
function queueUpdate() {
    if (!started || idle) return;
    idle=GLib.idle_add(GLib.PRIORITY_DEFAULT_IDLE,()=>{
        idle=0;
        if (started) refresh();
        return GLib.SOURCE_REMOVE;
    });
}
function detach() {
    if (!record) return;
    let r=record;record=null;
    if (r.childSignal) r.avatar.disconnect(r.childSignal);
    if (r.destroySignal) r.avatar.disconnect(r.destroySignal);
    if (r.userSignal) r.user.disconnect(r.userSignal);
    if (r.avatar.child===r.image) r.avatar.child=null;
    if (r.avatar.get_style()==='background-image:none; background-color:transparent;') r.avatar.update();
    r.image.destroy();
}
function attach(avatar,user) {
    if (record && record.avatar===avatar) return;
    detach();
    let r={avatar,user,image:new St.Bin({x_expand:true,y_expand:true}),childSignal:0,destroySignal:0,userSignal:0,lastPath:null};
    record=r;
    r.childSignal=avatar.connect('notify::child',()=>{
        if (avatar.child!==r.image) queueUpdate();
    });
    r.destroySignal=avatar.connect('destroy',()=>{
        if (r.userSignal) r.user.disconnect(r.userSignal);
        r.userSignal=0;
        r.image.destroy();
        if (record===r) record=null;
        queueUpdate();
    });
    r.userSignal=user.connect('changed',queueUpdate);
}
function refresh() {
    let def=AppletManager.definitions.find(d=>d.uuid==='menu@cinnamon.org' && d.applet);
    let widget=def?.applet?.userIcon;
    if (!widget || !widget._avatar || !widget._user) return;
    attach(widget._avatar,widget._user);
    let r=record,path=r.user.get_icon_file();
    if (!path || !GLib.file_test(path,GLib.FileTest.EXISTS)) return;
    try {
        let [ok,contents]=Gio.File.new_for_path(path).load_contents(null);
        if (!ok) return;
        let hash=GLib.compute_checksum_for_bytes(GLib.ChecksumType.SHA256,new GLib.Bytes(contents));
        let dir=GLib.build_filenamev([GLib.get_user_cache_dir(),'gruvbox-profile-photo']);
        GLib.mkdir_with_parents(dir,0o700);
        let cached=GLib.build_filenamev([dir,hash+'.png']);
        if (!GLib.file_test(cached,GLib.FileTest.EXISTS))
            Gio.File.new_for_path(cached).replace_contents(contents,null,false,Gio.FileCreateFlags.REPLACE_DESTINATION,null);
        if (r.lastPath!==cached) {
            r.image.style='background-color:transparent; background-image:url("'+cached+'"); background-size:cover;';
            r.lastPath=cached;
        }
        if (r.avatar.get_style()!=='background-image:none; background-color:transparent;')
            r.avatar.style='background-image:none; background-color:transparent;';
        r.image.set_size(r.avatar.width,r.avatar.height);
        if (r.avatar.child!==r.image) r.avatar.child=r.image;
    } catch (e) {global.logError(e,'Gruvbox profile photo');}
}
function init(metadata) {}
function enable() {
    if (started) return;
    started=true;
    settingsId=global.settings.connect('changed::enabled-applets',queueUpdate);
    busId=Gio.DBus.session.signal_subscribe(null,'org.Cinnamon','XletAddedComplete','/org/Cinnamon',null,Gio.DBusSignalFlags.NONE,queueUpdate);
    queueUpdate();
}
function disable() {
    started=false;
    if (idle) GLib.source_remove(idle);
    if (settingsId) global.settings.disconnect(settingsId);
    if (busId) Gio.DBus.session.signal_unsubscribe(busId);
    idle=settingsId=busId=0;
    detach();
}
