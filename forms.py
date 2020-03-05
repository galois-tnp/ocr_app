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
class Financial_RiskForm(FlaskForm):
    tot_debt = DecimalField('Total Debt')
    net_equity = DecimalField('Networth')
    gearing = DecimalField('Gearing')
    pb_it = DecimalField('Profit before interest & tax')
    tot_assets = DecimalField('Total Assets')
    cap_emp = DecimalField('Capital Employed')
    curr_liab = DecimalField('Current Liabilities')
    roce = DecimalField('ROCE')
class Financial_RiskForm1:
    def __init__(self,tot_debt,net_equity,gearing,pb_it,tot_assets,cap_emp,curr_liab,roce):
        self.tot_debt = tot_debt
        self.net_equity = net_equity
        self.gearing = gearing
        self.pb_it = pb_it
        self.tot_assets = tot_assets
        self.cap_emp = cap_emp
        self.curr_liab = curr_liab
        self.roce = roce
