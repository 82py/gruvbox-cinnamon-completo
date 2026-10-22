#!/usr/bin/env node
'use strict';
// Runs the shipped extension with a small signal/actor model. No live desktop is
// loaded or changed. In particular, removal does NOT imply destruction: this is
// the lifecycle that exposed the retained client-window actors in Cinnamon.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const sourcePath = process.argv[2] || path.join(__dirname, '..', 'payload', '.local',
    'share', 'cinnamon', 'extensions', 'gruvbox-system-colors@gruvbox-cinnamon', 'extension.js');
const source = fs.readFileSync(sourcePath, 'utf8');
const TAG = 'gruvbox-system-color';
class Actor {
    constructor() { this.children = []; this.parent = null; this.signals = new Map(); this.nextId = 1; this.destroyed = false; }
    connect(name, callback) { const id = this.nextId++; this.signals.set(id, {name, callback}); return id; }
    disconnect(id) { assert(this.signals.delete(id), 'disconnect must refer to a live signal'); }
    emit(name, ...args) {
        for (const [id, signal] of [...this.signals])
            if (this.signals.has(id) && signal.name === name) signal.callback(this, ...args);
    }
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
    constructor(name, classes = []) { super(); this.icon_name = name; this.classes = new Set(classes); this.gicon = null; }
    has_style_class_name(name) { return this.classes.has(name); }
    add_style_class_name(name) { this.classes.add(name); }
    remove_style_class_name(name) { this.classes.delete(name); }
    get_gicon() { return this.gicon; }
    rename(name) { this.icon_name = name; this.emit('notify::icon-name'); }
    setNames(names) { this.gicon = {get_names: () => names}; this.emit('notify::gicon'); }
}
function setup() {
    const root = new Actor(), windows = new Actor(), surface = new Actor();
    windows.add(surface); root.add(windows);
    const context = vm.createContext({imports: {gi: {St: {Icon}}, ui: {main: {uiGroup: root}}}, global: {window_group: windows}});
    vm.runInContext(source, context, {filename: sourcePath});
    return {root, windows, surface, context, tracked: () => vm.runInContext('tracked', context)};
}
function subtree() {
    const parent = new Actor(), box = new Actor(), icon = new Icon('xsi-folder-symbolic');
    parent.add(box); box.add(icon); return {parent, box, icon, all: [parent, box, icon]};
}
function released(env, actors) {
    for (const actor of actors) {
        assert(!env.tracked().has(actor), 'removed actors must leave the tracking map');
        assert.equal(actor.signals.size, 0, 'removed actors must disconnect every observer');
    }
}
const tests = {
    'detached subtree releases parent, descendants and signal handlers without destroy'() {
        const env = setup(), tree = subtree(); env.root.add(tree.parent); env.context.enable();
        assert(tree.icon.has_style_class_name(TAG));
        env.root.remove(tree.parent);
        assert(tree.all.every(actor => !actor.destroyed), 'exercise removal, not destruction');
        assert.equal(tree.parent.children[0], tree.box, 'detached subtree remains intact');
        released(env, tree.all);
        assert(!tree.icon.has_style_class_name(TAG), 'restore only the style owned by the extension');
        env.context.disable();
    },
    'reattached subtree is colored again and observes icon-name and GIcon changes'() {
        const env = setup(), tree = subtree(); env.context.enable();
        for (let cycle = 0; cycle < 12; cycle++) {
            tree.icon.rename('xsi-folder-symbolic'); tree.icon.setNames([]);
            env.root.add(tree.parent); assert(tree.icon.has_style_class_name(TAG));
            tree.icon.rename('unrelated-icon'); assert(!tree.icon.has_style_class_name(TAG));
            tree.icon.setNames(['folder-symbolic']); assert(tree.icon.has_style_class_name(TAG));
            env.root.remove(tree.parent); released(env, tree.all);
        }
        env.context.disable();
    },
    'preexisting style class survives removal, reattachment and disable'() {
        const env = setup(), icon = new Icon('unrelated-icon', [TAG]); env.root.add(icon); env.context.enable();
        env.root.remove(icon); released(env, [icon]); assert(icon.has_style_class_name(TAG));
        env.root.add(icon); icon.rename('another-unrelated-icon'); env.context.disable();
        assert(icon.has_style_class_name(TAG)); released(env, [icon]);
    },
    'window group and its existing or future descendants are never observed'() {
        const env = setup(), icon = new Icon('xsi-folder'); env.surface.add(icon); env.context.enable();
        released(env, [env.windows, env.surface, icon]); assert(!icon.has_style_class_name(TAG));
        const later = new Icon('folder'); env.windows.add(later); released(env, [later]);
        env.root.remove(env.windows); env.root.add(env.windows);
        released(env, [env.windows, env.surface, icon, later]); env.context.disable();
    },
    'disable is idempotent and stops observing later children'() {
        const env = setup(), tree = subtree(); env.root.add(tree.parent); env.context.enable();
        env.context.disable(); env.context.disable();
        assert.equal(env.tracked().size, 0); released(env, [env.root, ...tree.all]);
        assert(!tree.icon.has_style_class_name(TAG));
        const later = new Icon('folder'); env.root.add(later); released(env, [later]);
        assert(!later.has_style_class_name(TAG));
    },
    'destroyed subtrees disconnect their observers and leave surviving actors usable'() {
        const env = setup(), tree = subtree(); env.root.add(tree.parent); env.context.enable();
        tree.parent.destroy(); released(env, tree.all);
        const replacement = new Icon('folder'); env.root.add(replacement);
        assert(replacement.has_style_class_name(TAG)); env.context.disable();
    },
    'reparenting between watched containers does not accumulate callbacks'() {
        const env = setup(), left = new Actor(), right = new Actor(), tree = subtree();
        env.root.add(left); env.root.add(right); left.add(tree.parent); env.context.enable();
        const count = env.tracked().size, handlers = tree.all.map(a => a.signals.size);
        env.context.enable();
        for (let cycle = 0; cycle < 12; cycle++) {
            (cycle % 2 ? left : right).add(tree.parent);
            assert.equal(env.tracked().size, count); assert.deepEqual(tree.all.map(a => a.signals.size), handlers);
            assert(tree.icon.has_style_class_name(TAG));
        }
        env.context.disable(); released(env, [env.root, left, right, ...tree.all]);
    },
};
let failures = 0;
for (const [name, run] of Object.entries(tests)) {
    try { run(); console.log('PASS ' + name); }
    catch (error) { failures++; console.error('FAIL ' + name + ': ' + error.message); }
}
console.log(JSON.stringify({tests: Object.keys(tests).length, failures}));
process.exitCode = failures ? 1 : 0;
