# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djangocms_dag_jetcode',
 'djangocms_dag_jetcode.conf',
 'djangocms_dag_jetcode.migrations']

package_data = \
{'': ['*'],
 'djangocms_dag_jetcode': ['locale/fr/LC_MESSAGES/*',
                           'static/djangocms_dag_jetcode/css/*',
                           'static/djangocms_dag_jetcode/img/*',
                           'templates/djangocms_dag_jetcode/*']}

install_requires = \
['Django>2',
 'django-cms>=3.0.0,<4.0.0',
 'django-multiselectfield>=0.1.12,<0.2.0',
 'djangocms-attributes-field>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'djangocms-dag-jetcode',
    'version': '1.2.1',
    'description': "Django CMS DAG Jetcode is a plugin for Django CMS that allows you to add DAG System's Jetcodes on your site.",
    'long_description': '# djangocms-dag-jetcode\n\n**Django CMS DAG Jetcode** is a plugin for [Django CMS](http://django-cms.org/) that allows you to add [DAG System](https://dag-system.com/)\'s Jetcodes on your site.\n\n![preview djangocms-dag-jetcode](https://gitlab.com/kapt/open-source/djangocms-dag-jetcode/-/raw/main/preview.png)\n\n# Requirements\n\n- Python 3.8+\n- Django 2.0+\n- Django CMS 3.8.0+\n\n# Installation\n\n- run `pip install djangocms-dag-jetcode`\n- add `djangocms_dag_jetcode` to your `INSTALLED_APPS`\n- include in your `urls.py`\n  ```py\n  path(\n      "djangocms-dag-jetcode/",\n      include("djangocms_dag_jetcode.urls", namespace="djangocms-dag-jetcode"),\n  ),\n  ```\n- run `python manage.py migrate djangocms_dag_jetcode`\n- import DAG\'s scripts before the closing `</body>` tag\n  ```html\n  <script src="https://jetcode.dag-system.com/jetcodes/fr?customerID=<your customer id>" defer></script>\n  ```\n- add required `<div>` for the basket\n  ```html\n  <div class="basket-jetcode" data-basket-id="0" css-jetcode-href="https://absolute.path/to/custom.css"></div>\n  ```\n- add required `<div>` for the popups\n  ```html\n  <div class="rate-jetcode-def" css-jetcode-href="https://absolute.path/to/custom.css"></div>\n  <div class="cart-jetcode-def" css-jetcode-href="https://absolute.path/to/custom.css"></div>\n  <div class="checkout-jetcode-def" css-jetcode-href="https://absolute.path/to/custom.css"></div>\n  <div class="payinresult-jetcode-def" css-jetcode-href="https://absolute.path/to/custom.css"></div>\n  <div class="shippinginfo-jetcode-def" css-jetcode-href="https://absolute.path/to/custom.css"></div>\n  <div class="productinfo-jetcode-def" css-jetcode-href="https://absolute.path/to/custom.css"></div>\n  ```\n\nYou can override some files to customize the style:\n- `static/djangocms_dag_jetcode/css/base.css` base style for all Jetcodes\n- `static/djangocms_dag_jetcode/css/product.css` product Jetcodes\n- `static/djangocms_dag_jetcode/css/productselector.css` product selector Jetcodes\n- `static/djangocms_dag_jetcode/css/package.css` package Jetcodes\n- `static/djangocms_dag_jetcode/css/container.css` container Jetcodes\n- `static/djangocms_dag_jetcode/img/calendar-icon.png` the calendar icon\n- `templates/djangocms_dag_jetcode/default.html` the template used to render the Jetcodes\n\n# Settings\n\n## Styles choices\n\n```python\nDJANGOCMS_DAG_JETCODE_STYLE_CHOICES = [\n  ("my-style", "My custom style"),\n]\n```\ndefaults to `[]`\n\nEach style defined in this setting must have a corresponding CSS file in `{STATIC_ROOT}/djangocms_dag_jetcode/css/` (for example: `my-style.css`).\n\n## Cache timeout\n\nSet the cache timeout for the `get_css` view.\n```python\nDJANGOCMS_DAG_JETCODE_CACHE_TIMEOUT = 15 * 60\n```\ndefaults to `15 * 60` (15 minutes)\n\nWhen `DEBUG=True`, you can set this setting to `0` to disable the cache.\n\n# Reload Jetcode after CMS plugin edit\n\nWhen you add or edit a plugin, the CMS does not reload the entire page. You should re-instantiate the Jetcodes to display them without a page refresh. Add this code to your pages:\n```js\nif (window.hasOwnProperty(\'CMS\') === true) {\n  CMS.$(window).on(\'cms-content-refresh\', function () {\n    initJetcode()\n  })\n}\n```\n',
    'author': 'Kapt dev team',
    'author_email': 'dev@kapt.mobi',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/kapt/open-source/djangocms-dag-jetcode',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.0.0,<4.0.0',
}


setup(**setup_kwargs)
