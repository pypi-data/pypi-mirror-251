var _a;
import { Tooltip } from "@bokehjs/models/ui/tooltip";
import { TablerIcon } from "@bokehjs/models/ui/icons/tabler_icon";
import { SVGIcon } from "@bokehjs/models/ui/icons/svg_icon";
import { Control, ControlView } from '@bokehjs/models/widgets/control';
import { build_view } from '@bokehjs/core/build_views';
import { ButtonClick } from "@bokehjs/core/bokeh_events";
export class ClickableIconView extends ControlView {
    *controls() { }
    remove() {
        this.tooltip?.remove();
        this.icon_view?.remove();
        super.remove();
    }
    async lazy_initialize() {
        await super.lazy_initialize();
        this.was_svg_icon = this.is_svg_icon(this.model.icon);
        this.icon_view = await this.build_icon_model(this.model.icon, this.was_svg_icon);
        const { tooltip } = this.model;
        if (tooltip != null)
            this.tooltip = await build_view(tooltip, { parent: this });
    }
    *children() {
        yield* super.children();
        yield this.icon_view;
        if (this.tooltip != null)
            yield this.tooltip;
    }
    is_svg_icon(icon) {
        return icon.trim().startsWith('<svg');
    }
    connect_signals() {
        super.connect_signals();
        const { icon, active_icon, disabled, value, size } = this.model.properties;
        this.on_change([active_icon, icon, value], () => this.update_icon());
        this.on_change(disabled, () => this.update_cursor());
        this.on_change(size, () => this.update_size());
    }
    render() {
        super.render();
        this.icon_view.render();
        this.update_icon();
        this.update_cursor();
        this.shadow_el.appendChild(this.icon_view.el);
        const toggle_tooltip = (visible) => {
            this.tooltip?.model.setv({
                visible,
            });
        };
        let timer;
        this.el.addEventListener("mouseenter", () => {
            timer = setTimeout(() => toggle_tooltip(true), this.model.tooltip_delay);
        });
        this.el.addEventListener("mouseleave", () => {
            clearTimeout(timer);
            toggle_tooltip(false);
        });
    }
    update_cursor() {
        this.icon_view.el.style.cursor = this.model.disabled ? 'not-allowed' : 'pointer';
    }
    update_size() {
        this.icon_view.model.size = this.calculate_size();
    }
    async build_icon_model(icon, is_svg_icon) {
        const size = this.calculate_size();
        let icon_model;
        if (is_svg_icon) {
            icon_model = new SVGIcon({ svg: icon, size: size });
        }
        else {
            icon_model = new TablerIcon({ icon_name: icon, size: size });
        }
        const icon_view = await build_view(icon_model, { parent: this });
        icon_view.el.addEventListener('click', () => this.click());
        return icon_view;
    }
    async update_icon() {
        const icon = this.model.value ? this.get_active_icon() : this.model.icon;
        const is_svg_icon = this.is_svg_icon(icon);
        if (this.was_svg_icon !== is_svg_icon) {
            // If the icon type has changed, we need to rebuild the icon view
            // and invalidate the old one.
            const icon_view = await this.build_icon_model(icon, is_svg_icon);
            icon_view.render();
            this.icon_view.remove();
            this.icon_view = icon_view;
            this.was_svg_icon = is_svg_icon;
            this.update_cursor();
            this.shadow_el.appendChild(this.icon_view.el);
        }
        else if (is_svg_icon) {
            this.icon_view.model.svg = icon;
        }
        else {
            this.icon_view.model.icon_name = icon;
        }
        this.icon_view.el.style.lineHeight = '0';
    }
    get_active_icon() {
        return this.model.active_icon !== '' ? this.model.active_icon : `${this.model.icon}-filled`;
    }
    calculate_size() {
        if (this.model.size !== null)
            return this.model.size;
        const maxWidth = this.model.width ?? 15;
        const maxHeight = this.model.height ?? 15;
        const size = Math.max(maxWidth, maxHeight);
        return `${size}px`;
    }
    click() {
        this.model.trigger_event(new ButtonClick());
    }
}
ClickableIconView.__name__ = "ClickableIconView";
export class ClickableIcon extends Control {
    constructor(attrs) {
        super(attrs);
    }
    on_click(callback) {
        this.on_event(ButtonClick, callback);
    }
}
_a = ClickableIcon;
ClickableIcon.__name__ = "ClickableIcon";
ClickableIcon.__module__ = "panel.models.icon";
(() => {
    _a.prototype.default_view = ClickableIconView;
    _a.define(({ Nullable, Ref, Number, String, Boolean }) => ({
        active_icon: [String, ""],
        icon: [String, "heart"],
        size: [Nullable(String), null],
        value: [Boolean, false],
        tooltip: [Nullable(Ref(Tooltip)), null],
        tooltip_delay: [Number, 500],
    }));
})();
//# sourceMappingURL=icon.js.map