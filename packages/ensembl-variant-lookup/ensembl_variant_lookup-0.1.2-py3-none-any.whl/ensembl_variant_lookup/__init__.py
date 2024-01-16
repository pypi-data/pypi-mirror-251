# ensembl_variant_lookup/__init__.py

from flask import Flask

app = Flask(__name__)

from ensembl_variant_lookup import fetch_variants
