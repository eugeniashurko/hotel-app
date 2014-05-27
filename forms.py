from wtforms import Form, TextField, DateField, RadioField, validators
import myvalidators


class AddClientForm(Form):
    name = TextField('Name:', [validators.DataRequired(\
        message="This is required field")])
    surname = TextField('Surname:', [validators.DataRequired(\
        message="This is required field")])
    passport = TextField('Passport (AA123456):', [validators.DataRequired(\
        message="This is required field")])
    address = TextField('Address:', [validators.DataRequired(\
        message="This is required field")])
    sex = RadioField('Sex', choices=[("male", "Male"), ("female", "Female")],\
      validators=[validators.DataRequired(\
        message="This is required field")])


class BookForm(Form):
    date_from = DateField('From (YYYY-MM-DD):', [validators.DataRequired(\
        message="This is required field")])
    date_to = DateField('To (YYYY-MM-DD):', [validators.DataRequired(\
        message="This is required field"), myvalidators.ValidDates(), \
        myvalidators.AvailableDates()])
    room_id = TextField('Room ID:', [validators.DataRequired(\
        message="This is required field"), myvalidators.ValidRoomId()])
    client_id = TextField('Client ID:', [validators.DataRequired(\
        message="This is required field"), myvalidators.ValidClientId()])
    ptype = RadioField('Payment Type:', choices=[("Cash", "Cash"), \
        ("Card", "Card")], validators=[validators.DataRequired(\
        message="This is required field")])
    pdone = RadioField('Payment Done:', choices=[("Yes", "Yes"),\
     ("No", "No")], validators=[validators.DataRequired(\
        message="This is required field")])
