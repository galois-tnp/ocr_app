from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,SelectField,DateField,DecimalField,FieldList,FormField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

# User Based Imports
class ImageForm(FlaskForm):
    pageNum = StringField('Page Number', validators=[DataRequired()])
    submit = SubmitField('Convert')
class ConfigurationForm(FlaskForm):
    bal_sheet = StringField('Balance Sheet')
    profit_loss = StringField('Profit & Loss')
    submit = SubmitField('Submit')
