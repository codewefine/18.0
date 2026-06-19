{
    "name": "Product Name Google Translate",
    "version": "18.0.1.0.0",
    "category": "Sales",
    "summary": "Auto translate product names in the translation dialog using Google Translate",
    "description": """
Product Name Google Translate
=============================
This module integrates Google Translate directly into the Odoo product translation dialog. 
It allows you to automatically translate product names into any target language with a single click.

Features:
- One-click Google Translate integration inside Odoo's translation dialog.
- Supports translating product names to multiple languages.
- Simple, fast, and improves productivity.
    """,
    "author": "codewefine",
    "maintainer": "codewefine",
    "website": "",
    "images": ["static/description/images.png"],
    "depends": ["web", "product"],
    "data": [],
    "assets": {
        "web.assets_backend": [
            "product_name_translate/static/src/js/translation_dialog_patch.js",
            "product_name_translate/static/src/xml/translation_dialog_patch.xml",
        ],
    },
    "installable": True,
    "application": False,
    "license": "LGPL-3",
    "price": 10.00,
    "currency": "USD",
}
