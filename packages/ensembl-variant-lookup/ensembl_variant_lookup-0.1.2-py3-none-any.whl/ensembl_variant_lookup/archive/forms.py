# ensembl_variant_lookup/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class VariantForm(FlaskForm):
    rsid = StringField('RSID', validators=[DataRequired()])
    submit = SubmitField('Fetch Variant')
