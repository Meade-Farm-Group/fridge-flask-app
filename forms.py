from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateField,\
                    ValidationError
from wtforms.validators import Optional, Length, DataRequired


# def no_whitespace_only(form, field):
#     if len(field.data.strip()) == 0:
#         raise ValidationError('No Whitespace only')


class SearchForm(FlaskForm):
    product_name = StringField('Product Name', validators=[
        Optional(strip_whitespace=True),
        Length(min=1, max=50, message=None),
        ])
    purchase_order = IntegerField('Purchase Order Number', validators=[
        Optional(strip_whitespace=True)])
    reference = StringField('Reference', validators=[
        Optional(strip_whitespace=True)])
    best_before_date = DateField('Best Before Date', validators=[
        Optional(strip_whitespace=True)])
    submit = SubmitField('Search')

    def validate(self, extra_validators=None):
        if super().validate(extra_validators):
            product_name = self.product_name.data.strip()
            reference = self.reference.data.strip()
            # your logic here e.g.
            if not (product_name or self.purchase_order.data or
                    reference or self.best_before_date.data):
                self.product_name.errors.append(
                    'At least one field must have a value')
                return False
            else:
                return True

        return False
