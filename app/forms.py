from flask.ext.wtf import Form
from wtforms import HiddenField
from flask.ext.wtf.html5 import DecimalField
from wtforms.validators import Required

class EditMileageForm(Form):
    miles =    DecimalField('miles', validators = [Required()], places = 1)
    price    = DecimalField('price', validators = [Required()], places = 3) 
    gallons  = DecimalField('gallons', validators = [Required()], places = 3) 
    date = HiddenField("date")

class MileageForm(EditMileageForm):
    latitude = HiddenField('latitude')
    longitude = HiddenField('longitude')
