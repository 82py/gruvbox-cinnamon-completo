#!/usr/bin/env node
'use strict';
// Executes the shipped extension against actor/signal stubs, never a live
// Cinnamon session. Detached texture actors deliberately remain undestroyed.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const sourcePath = process.argv[2] || path.join(__dirname, '..', 'payload', '.local',
    'share', 'cinnamon', 'extensions', 'gruvbox-mintupdate-colors@gruvbox-cinnamon', 'extension.js');
const source = fs.readFileSync(sourcePath, 'utf8');
const TAG = 'gruvbox-mintupdate-color';
class Signals {
    constructor() { this.signals = new Map(); this.nextId = 1; }
    connect(name, callback) { const id = this.nextId++; this.signals.set(id, {name, callback}); return id; }
    disconnect(id) { assert(this.signals.delete(id), 'disconnect must refer to a live signal'); }
    emit(name, ...args) {
        for (const [id, signal] of [...this.signals])
            if (this.signals.has(id) && signal.name === name) signal.callback(this, ...args);
    }
}
class Actor extends Signals {
    constructor() { super(); this.children = []; this.parent = null; this.destroyed = false; }
    get_children() { return [...this.children]; }
    add(child) {
        assert(!child.destroyed);
        if (child.parent) child.parent.remove(child);
        this.children.push(child); child.parent = this; this.emit('actor-added', child);
    }
    remove(child) {
        assert.equal(child.parent, this);
        this.children.splice(this.children.indexOf(child), 1); child.parent = null;
        this.emit('actor-removed', child);
    }
    destroy() {
        this.emit('destroy');
        for (const child of [...this.children]) child.destroy();
        if (this.parent) this.parent.remove(this);
        this.destroyed = true;
    }
}
class Icon extends Actor {
    constructor(name, classes = []) { super(); this.icon_name = name; this.classes = new Set(classes); }
    has_style_class_name(name) { return this.classes.has(name); }
    add_style_class_name(name) { this.classes.add(name); }
    remove_style_class_name(name) { this.classes.delete(name); }
    rename(name) { this.icon_name = name; this.emit('notify::icon-name'); }
}
function setup() {
    const root = new Actor(), settings = new Signals(), bus = new Signals(), pending = new Map();
    let nextIdle = 1;
    const applets = {definitions: [{uuid: 'xapp-status@cinnamon.org', applet: {actor: root}}]};
    bus.signal_subscribe = (...args) => bus.connect('XletAddedComplete', args.at(-1));
    bus.signal_unsubscribe = id => bus.disconnect(id);
    const GLib = {
        PRIORITY_DEFAULT_IDLE: 0, SOURCE_REMOVE: false,
        idle_add(_priority, callback) { const id = nextIdle++; pending.set(id, callback); return id; },
        source_remove(id) { assert(pending.delete(id)); },
    };
    const context = vm.createContext({imports: {gi: {St: {Icon}, GLib, Gio: {DBus: {session: bus}, DBusSignalFlags: {NONE: 0}}},
        ui: {appletManager: applets}}, global: {settings}});
    vm.runInContext(source, context, {filename: sourcePath});
    function flush() {
        for (const [id, callback] of [...pending]) { pending.delete(id); assert.equal(callback(), false); }
    }
    return {root, settings, bus, pending, applets, context, flush, watched: () => vm.runInContext('watched', context)};
}
function subtree() {
    const parent = new Actor(), box = new Actor(), icon = new Icon('mintupdate-up-to-date-symbolic');
    parent.add(box); box.add(icon); return {parent, box, icon, all: [parent, box, icon]};
}
function released(env, actors) {
    for (const actor of actors) {
        assert(!env.watched().has(actor), 'detached actors must leave the tracking map');
        assert.equal(actor.signals.size, 0, 'detached actors must disconnect every observer');
    }
}
const tests = {
    '25 texture replacements keep the watched actor count bounded and color intact'() {
        const env = setup(), icon = new Icon('mintupdate-up-to-date-symbolic');
        env.root.add(icon); env.context.enable(); const baseline = env.watched().size;
        let prior = null;
        for (let cycle = 0; cycle < 25; cycle++) {
            if (prior) {
                icon.remove(prior.parent); released(env, prior.all);
                assert(prior.all.every(a => !a.destroyed), 'replacement must not rely on destruction');
                assert.equal(env.watched().size, baseline);
            }
            const parent = new Actor(), texture = new Actor(); parent.add(texture); icon.add(parent);
            prior = {parent, all: [parent, texture]};
            assert.equal(env.watched().size, baseline + 2); assert(icon.has_style_class_name(TAG));
        }
        env.context.disable(); released(env, [env.root, icon, ...prior.all]);
    },
    'removing and reattaching an indicator releases descendants then restores live coloring'() {
        const env = setup(), tree = subtree(); env.root.add(tree.parent); env.context.enable();
        env.root.remove(tree.parent); released(env, tree.all); assert(!tree.icon.has_style_class_name(TAG));
        env.root.add(tree.parent); assert(tree.icon.has_style_class_name(TAG));
        tree.icon.rename('unrelated-icon'); assert(!tree.icon.has_style_class_name(TAG));
        for (const state of ['checking', 'installing', 'up-to-date', 'updates-available', 'warning', 'error']) {
            tree.icon.rename('mintupdate-' + state + '-symbolic'); assert(tree.icon.has_style_class_name(TAG));
        }
        env.context.disable();
    },
    'preexisting style ownership survives removal and disable'() {
        const env = setup(), icon = new Icon('unrelated-icon', [TAG]); env.root.add(icon); env.context.enable();
        env.root.remove(icon); released(env, [icon]); assert(icon.has_style_class_name(TAG));
        env.root.add(icon); env.context.disable(); assert(icon.has_style_class_name(TAG));
    },
    'only XApp status trees are watched and refresh events are coalesced'() {
        const env = setup(), other = new Icon('mintupdate-error-symbolic');
        env.applets.definitions.push({uuid: 'other@cinnamon.org', applet: {actor: other}});
        env.context.enable(); released(env, [other]); assert(!other.has_style_class_name(TAG));
        const extra = new Actor(), icon = new Icon('mintupdate-warning-symbolic'); extra.add(icon);
        env.applets.definitions.push({uuid: 'xapp-status@cinnamon.org', applet: {actor: extra}});
        env.settings.emit('changed::enabled-applets'); env.bus.emit('XletAddedComplete');
        assert.equal(env.pending.size, 1); env.flush(); assert(icon.has_style_class_name(TAG));
        assert(env.watched().has(extra)); released(env, [other]); env.context.disable();
    },
    'disable cancels pending work, disconnects external events and is idempotent'() {
        const env = setup(), tree = subtree(); env.root.add(tree.parent); env.context.enable();
        env.settings.emit('changed::enabled-applets'); assert.equal(env.pending.size, 1);
        env.context.disable(); env.context.disable();
        assert.equal(env.pending.size, 0); assert.equal(env.settings.signals.size, 0);
        assert.equal(env.bus.signals.size, 0); assert.equal(env.watched().size, 0);
        released(env, [env.root, ...tree.all]); assert(!tree.icon.has_style_class_name(TAG));
        const later = new Icon('mintupdate-error-symbolic'); env.root.add(later); released(env, [later]);
        env.settings.emit('changed::enabled-applets'); env.bus.emit('XletAddedComplete');
        assert.equal(env.pending.size, 0);
    },
    'destroy releases child observers without disrupting surviving indicators'() {
        const env = setup(), tree = subtree(); env.root.add(tree.parent); env.context.enable();
        tree.parent.destroy(); released(env, tree.all);
        const replacement = new Icon('mintupdate-checking-symbolic'); env.root.add(replacement);
        assert(replacement.has_style_class_name(TAG)); env.context.disable();
    },
    'repeated enable and reparent do not multiply signal connections'() {
        const env = setup(), tree = subtree(), second = new Actor();
        env.root.add(second); env.root.add(tree.parent); env.context.enable();
        const baseline = env.watched().size, connections = tree.all.map(a => a.signals.size);
        env.context.enable(); assert.equal(env.settings.signals.size, 1); assert.equal(env.bus.signals.size, 1);
        for (let cycle = 0; cycle < 12; cycle++) {
            (cycle % 2 ? env.root : second).add(tree.parent);
            assert.equal(env.watched().size, baseline); assert.deepEqual(tree.all.map(a => a.signals.size), connections);
        }
        env.context.disable(); env.context.enable(); assert(tree.icon.has_style_class_name(TAG));
        assert.equal(env.settings.signals.size, 1); assert.equal(env.bus.signals.size, 1); env.context.disable();
    },
};
let failures = 0;
for (const [name, run] of Object.entries(tests)) {
    try { run(); console.log('PASS ' + name); }
    catch (error) { failures++; console.error('FAIL ' + name + ': ' + error.message); }
}
console.log(JSON.stringify({tests: Object.keys(tests).length, failures}));
process.exitCode = failures ? 1 : 0;
