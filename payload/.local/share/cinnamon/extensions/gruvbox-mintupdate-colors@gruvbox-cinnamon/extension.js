// Adds a scoped style class; no applet or application methods are replaced.
const Gio = imports.gi.Gio;
const GLib = imports.gi.GLib;
const St = imports.gi.St;
const AppletManager = imports.ui.appletManager;
const TAG = 'gruvbox-mintupdate-color';
const NAMES = new Set(['checking','installing','up-to-date','updates-available','warning','error'].map(s => 'mintupdate-'+s+'-symbolic'));
let watched = new Map();
let started = false;
let idleId = 0;
let settingsId = 0;
let busId = 0;
function synchronize(actor, record) {
    if (!(actor instanceof St.Icon) || !record.owned) return;
    if (NAMES.has(actor.icon_name || '')) actor.add_style_class_name(TAG);
    else actor.remove_style_class_name(TAG);
}
function watch(actor) {
    if (watched.has(actor)) return;
    let r = {owned: !(actor instanceof St.Icon) || !actor.has_style_class_name(TAG), added: 0, destroyed: 0, changed: 0};
    watched.set(actor,r);
    r.added = actor.connect('actor-added', (_parent, child) => watch(child));
    r.destroyed = actor.connect('destroy', () => watched.delete(actor));
    if (actor instanceof St.Icon) {
        r.changed = actor.connect('notify::icon-name', () => synchronize(actor,r));
        synchronize(actor,r);
    }
    for (let child of actor.get_children()) watch(child);
}
function refresh() {
    for (let d of AppletManager.definitions) {
        if (d.uuid === 'xapp-status@cinnamon.org' && d.applet) watch(d.applet.actor);
    }
}
function queueRefresh() {
    if (!started || idleId) return;
    idleId = GLib.idle_add(GLib.PRIORITY_DEFAULT_IDLE, () => {
        idleId=0;
        if (started) refresh();
        return GLib.SOURCE_REMOVE;
    });
}
function init(metadata) {}
function enable() {
    if (started) return;
    started=true;
    settingsId=global.settings.connect('changed::enabled-applets',queueRefresh);
    busId=Gio.DBus.session.signal_subscribe(null,'org.Cinnamon','XletAddedComplete','/org/Cinnamon',null,Gio.DBusSignalFlags.NONE,queueRefresh);
    refresh();
}
function disable() {
    started=false;
    if (idleId) GLib.source_remove(idleId);
    if (settingsId) global.settings.disconnect(settingsId);
    if (busId) Gio.DBus.session.signal_unsubscribe(busId);
    idleId=settingsId=busId=0;
    for (let [a,r] of watched) {
        if (r.added) a.disconnect(r.added);
        if (r.destroyed) a.disconnect(r.destroyed);
        if (r.changed) a.disconnect(r.changed);
        if (a instanceof St.Icon && r.owned) a.remove_style_class_name(TAG);
    }
    watched.clear();
}
