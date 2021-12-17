from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateField
from wtforms.validators import DataRequired, Optional


class SearchForm(FlaskForm):
    product_code = IntegerField('Product Code', validators=[
        Optional(strip_whitespace=True)])
    purchase_order = IntegerField('Purchase Order', validators=[
        Optional(strip_whitespace=True)])
    reference = StringField('Reference', validators=[
        Optional(strip_whitespace=True)])
    best_before_date = DateField('Best Before Date', validators=[
        Optional(strip_whitespace=True)])
    submit = SubmitField('Search')

    def validate_on_submit(self, extra_validators=None):
        if super().validate(extra_validators):

            # your logic here e.g.
            if not (self.product_code.data or self.purchase_order.data or
                    self.reference.data or self.best_before_date.data):
                self.product_code.errors.append(
                    'At least one field must have a value')
                return False
            else:
                return True

        return False
