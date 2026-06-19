/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { TranslationDialog } from "@web/views/fields/translation_dialog";
import { useService } from "@web/core/utils/hooks";
import { loadLanguages } from "@web/core/l10n/translation";
import { useState } from "@odoo/owl";

patch(TranslationDialog.prototype, {
    setup() {
        super.setup(...arguments);
        this.notification = useService("notification");
        this.translateState = useState({ isTranslating: false });
    },

    get canGoogleTranslateProductName() {
        return (
            this.props.fieldName === "name" &&
            (this.props.resModel === "product.template" || this.props.resModel === "product.product")
        );
    },

    async onGoogleTranslateAll() {
        if (!this.props.resId) {
            this.notification.add(
                _t("No product record found."),
                { type: "warning" }
            );
            return;
        }

        this.translateState.isTranslating = true;
        try {
            await this.orm.call(
                this.props.resModel,
                "action_translate_name",
                [[this.props.resId]]
            );

            const languages = await loadLanguages(this.orm);
            const [translations] = await this.loadTranslations(languages);
            let id = 1;
            translations.forEach((t) => (t.id = id++));
            this.terms = translations.map((term) => {
                const relatedLanguage = languages.find((l) => l[0] === term.lang);
                return {
                    ...term,
                    langName: relatedLanguage ? relatedLanguage[1] : term.lang,
                    value: term.value || "",
                };
            });
            this.terms.sort((a, b) => a.langName.localeCompare(b.langName));
            this.updatedTerms = {};
            this.render();

            this.notification.add(
                _t("Translations completed successfully."),
                { type: "success" }
            );
        } catch (error) {
            this.notification.add(
                _t("Translation failed."),
                { type: "danger" }
            );
        } finally {
            this.translateState.isTranslating = false;
        }
    },
});
