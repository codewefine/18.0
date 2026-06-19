from odoo import models, fields, api, _
import requests
from requests.adapters import HTTPAdapter
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor
import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    
    def action_translate_name(self):
        self.ensure_one()
        if not self.name:
            return

        langs = self.env['res.lang'].search([('active', '=', True)])
        source_text = self.name

        lang_data = []
        for lang in langs:
            odoo_code = lang.code
            
            google_code = {
                'zh_CN': 'zh-CN',
                'zh_TW': 'zh-TW',
            }.get(odoo_code, odoo_code.split('_')[0])
            lang_data.append((odoo_code, google_code))

        if not lang_data:
            return True

        
        session = requests.Session()
        adapter = HTTPAdapter(pool_connections=20, pool_maxsize=20)
        session.mount('https://', adapter)
        encoded_text = quote(source_text)

        def translate_lang(data):
            odoo_code, google_code = data
            try:
                url = (
                    f"https://translate.googleapis.com/translate_a/single"
                    f"?client=gtx&sl=auto&tl={google_code}&dt=t&q={encoded_text}"
                )
                resp = session.get(url, timeout=10)
                if resp.status_code == 200:
                    result = resp.json()
                    translated = ''.join(
                        part[0] for part in result[0] if part and part[0]
                    )
                    return odoo_code, translated
                return odoo_code, None
            except Exception as e:
                _logger.warning("Translation failed for %s: %s", google_code, e)
                return odoo_code, None

        with ThreadPoolExecutor(max_workers=min(len(lang_data), 20)) as executor:
            results = list(executor.map(translate_lang, lang_data))

        session.close()

        translations = {}
        for odoo_code, translated in results:
            if translated:
                translations[odoo_code] = translated

        if translations:
            self.update_field_translations('name', translations)

        return True


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def action_translate_name(self):
        self.ensure_one()
        return self.product_tmpl_id.action_translate_name()
