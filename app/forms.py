from flask.ext.wtf import Form
from wtforms import HiddenField
from wtforms.fields.html5 import TelField
from wtforms.validators import Required

class EditMileageForm(Form):
    miles    = TelField('miles', validators = [Required()],  default = 0.0)
    price    = TelField('price', validators = [Required()], default = 0.000) 
    gallons  = TelField('gallons', validators = [Required()], default = 0.000) 
    date = HiddenField("date")

class MileageForm(EditMileageForm):
    latitude = HiddenField('latitude')
    longitude = HiddenField('longitude')
