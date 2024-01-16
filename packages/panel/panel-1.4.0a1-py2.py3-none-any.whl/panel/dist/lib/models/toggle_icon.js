var _a;
import { ClickableIcon, ClickableIconView } from "./icon";
export class ToggleIconView extends ClickableIconView {
    *controls() { }
    click() {
        if (this.model.disabled) {
            return;
        }
        super.click();
        this.model.value = !this.model.value;
    }
}
ToggleIconView.__name__ = "ToggleIconView";
export class ToggleIcon extends ClickableIcon {
    constructor(attrs) {
        super(attrs);
    }
}
_a = ToggleIcon;
ToggleIcon.__name__ = "ToggleIcon";
ToggleIcon.__module__ = "panel.models.icon";
(() => {
    _a.prototype.default_view = ToggleIconView;
    _a.define(({}) => ({}));
})();
//# sourceMappingURL=toggle_icon.js.map