from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateField
from wtforms.validators import Optional, Length, DataRequired


class SearchForm(FlaskForm):
    product_name = StringField('Product Name', validators=[
        Optional(strip_whitespace=True),
        Length(min=1, max=50, message=None)])
    purchase_order = IntegerField('Purchase Order Number', validators=[
        Optional(strip_whitespace=True)])
    reference = StringField('Reference', validators=[
        Optional(strip_whitespace=True)])
    best_before_date = DateField('Best Before Date', validators=[
        Optional(strip_whitespace=True)])
    submit = SubmitField('Search')

    def validate(self, extra_validators=None):
        if super().validate(extra_validators):

            # your logic here e.g.
            if not (self.product_name.data or self.purchase_order.data or
                    self.reference.data or self.best_before_date.data):
                self.product_name.errors.append(
                    'At least one field must have a value')
                return False
            else:
                return True

        return False
