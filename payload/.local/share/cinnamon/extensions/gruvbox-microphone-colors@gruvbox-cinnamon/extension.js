/* Draft only: not installed or enabled. Adds a CSS class, never replaces applet methods. */
const Gio = imports.gi.Gio;
const GLib = imports.gi.GLib;
const St = imports.gi.St;
const AppletManager = imports.ui.appletManager;
const TAG = 'gruvbox-microphone-color';
let tracked = new Map();
let started = false;
let idleId = 0;
let settingsId = 0;
let busId = 0;

function isMicrophone(icon) {
    return (icon.icon_name || '').startsWith('xsi-microphone-sensitivity-');
}
function synchronize(icon, record) {
    if (!record.owned) return;
    if (isMicrophone(icon)) icon.add_style_class_name(TAG);
    else icon.remove_style_class_name(TAG);
}
function track(icon) {
    if (tracked.has(icon)) return;
    let record = { owned: !icon.has_style_class_name(TAG), changed: 0, destroyed: 0 };
    tracked.set(icon, record);
    synchronize(icon, record);
    record.changed = icon.connect('notify::icon-name', () => synchronize(icon, record));
    record.destroyed = icon.connect('destroy', () => tracked.delete(icon));
}
function refresh() {
    for (let definition of AppletManager.definitions) {
        if (definition.uuid !== 'sound@cinnamon.org' || !definition.applet) continue;
        let sound = definition.applet;
        function walk(actor) {
            if (actor instanceof St.Icon && isMicrophone(actor)) track(actor);
            for (let child of actor.get_children()) walk(child);
        }
        // Popup actors are outside the panel applet's actor tree.
        for (let menu of [sound.menu, sound._applet_context_menu]) {
            if (menu && menu.actor) walk(menu.actor);
        }
    }
}
function queueRefresh() {
    if (!started || idleId) return;
    idleId = GLib.idle_add(GLib.PRIORITY_DEFAULT_IDLE, () => {
        idleId = 0;
        if (started) refresh();
        return GLib.SOURCE_REMOVE;
    });
}
function init(metadata) {}
function enable() {
    if (started) return;
    started = true;
    settingsId = global.settings.connect('changed::enabled-applets', queueRefresh);
    busId = Gio.DBus.session.signal_subscribe(null, 'org.Cinnamon', 'XletAddedComplete',
        '/org/Cinnamon', null, Gio.DBusSignalFlags.NONE, queueRefresh);
    refresh();
}
function disable() {
    started = false;
    if (idleId) GLib.source_remove(idleId);
    if (settingsId) global.settings.disconnect(settingsId);
    if (busId) Gio.DBus.session.signal_unsubscribe(busId);
    idleId = settingsId = busId = 0;
    for (let [icon, record] of tracked) {
        if (record.changed) icon.disconnect(record.changed);
        if (record.destroyed) icon.disconnect(record.destroyed);
        if (record.owned) icon.remove_style_class_name(TAG);
    }
    tracked.clear();
}
