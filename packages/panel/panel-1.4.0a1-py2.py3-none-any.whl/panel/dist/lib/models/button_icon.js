var _a;
import { ClickableIcon, ClickableIconView } from "./icon";
export class ButtonIconView extends ClickableIconView {
    *controls() { }
    update_cursor() {
        this.icon_view.el.style.cursor = this.model.disabled ? 'default' : 'pointer';
    }
    click() {
        if (this.model.disabled) {
            return;
        }
        super.click();
        const updateState = (value, disabled) => {
            this.model.value = value;
            this.model.disabled = disabled;
        };
        updateState(true, true);
        new Promise(resolve => setTimeout(resolve, this.model.toggle_duration))
            .then(() => {
            updateState(false, false);
        });
    }
}
ButtonIconView.__name__ = "ButtonIconView";
export class ButtonIcon extends ClickableIcon {
    constructor(attrs) {
        super(attrs);
    }
}
_a = ButtonIcon;
ButtonIcon.__name__ = "ButtonIcon";
ButtonIcon.__module__ = "panel.models.icon";
(() => {
    _a.prototype.default_view = ButtonIconView;
    _a.define(({ Int }) => ({
        toggle_duration: [Int, 75],
    }));
})();
//# sourceMappingURL=button_icon.js.map