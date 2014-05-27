import xml.sax
from datetime import date
from wtforms import ValidationError


class ClientIdCheckHandler (xml.sax.ContentHandler):
    id = ""
    current_id = ""
    # outside "cl:id" 0
    # inside "cl:id" 1
    state = 0
    # True when client with given id exists
    flag = False

    def __init__(self, client_id):
        xml.sax.ContentHandler.__init__(self)
        ClientIdCheckHandler.id = client_id

    def startElement(self, name, attributes):
        if name == "cl:id":
            ClientIdCheckHandler.state = 1

    def endElement(self, name):
        if name == "cl:id":
            ClientIdCheckHandler.state = 0
            if ClientIdCheckHandler.current_id == ClientIdCheckHandler.id:
                ClientIdCheckHandler.flag = True

    def characters(self, content):
        if (content.strip() != ""):
            if (ClientIdCheckHandler.state == 1):
                ClientIdCheckHandler.current_id = str(content)


class RoomIdCheckHandler (xml.sax.ContentHandler):
    id = ""
    current_id = ""
    # outside "ro:room_id" 0
    # inside "ro:room_id" 1
    state = 0
    # True when room with given id exists
    flag = False

    def __init__(self, room_id):
        xml.sax.ContentHandler.__init__(self)
        RoomIdCheckHandler.id = room_id

    def startElement(self, name, attributes):
        if name == "ro:room_id":
            RoomIdCheckHandler.state = 1

    def endElement(self, name):
        if name == "ro:room_id":
            RoomIdCheckHandler.state = 0
            if RoomIdCheckHandler.current_id == RoomIdCheckHandler.id:
                RoomIdCheckHandler.flag = True

    def characters(self, content):
        if (content.strip() != ""):
            if RoomIdCheckHandler.state == 1:
                RoomIdCheckHandler.current_id = str(content)


class DateHandler (xml.sax.ContentHandler):
    # To avoid enumeration, value of state means :
    # 0 - external state
    # 1 - inside 'book'
    # 2 - inside 'from'
    # 3 - inside 'to'
    # 4 - inside 'room_id'

    room_id = ""
    dates = ["", ""]

    state = 0
    current_room_id = ""

    intersection = False

    def __init__(self, room_id, dates):
        xml.sax.ContentHandler.__init__(self)
        DateHandler.room_id = room_id
        DateHandler.dates = dates

    def startElement(self, name, attributes):
        if name == "hi:book":
            DateHandler.state = 1
        elif name == "hi:from":
            DateHandler.state = 2
        elif name == "hi:to":
            DateHandler.state = 3
        elif name == "hi:room_id":
            DateHandler.state = 4

    def endElement(self, name):
        if name == "hi:room_id":
            DateHandler.state = 0
            if DateHandler.current_room_id == DateHandler.room_id:
                print DateHandler.current_room_id, '=', DateHandler.room_id
                print DateHandler.fbuffer, ', ', DateHandler.tbuffer
                print DateHandler.dates[0], ', ', DateHandler.dates[1]
                print (DateHandler.fbuffer < DateHandler.tbuffer) and \
                    ((DateHandler.tbuffer < DateHandler.dates[0]) or \
                    (DateHandler.dates[1] < DateHandler.fbuffer))
                if not (DateHandler.fbuffer < DateHandler.tbuffer) and \
                    ((DateHandler.tbuffer < DateHandler.dates[0]) or \
                    (DateHandler.dates[1] < DateHandler.fbuffer)):
                    DateHandler.intersection = True
                    print DateHandler.intersection

        elif name == "hi:from":
            DateHandler.state = 0
        elif name == "hi:to":
            DateHandler.state = 0

    def characters(self, content):
        c = content.strip()
        if len(c) != 0:
            if DateHandler.state == 2:
                DateHandler.fbuffer = convert_to_date(content)
            if DateHandler.state == 3:
                DateHandler.tbuffer = convert_to_date(content)
            if DateHandler.state == 4:
                DateHandler.current_room_id = str(content)


def convert_to_date(input_d):
    dtemp = input_d.split("-", 2)
    d = date(int(dtemp[0]), int(dtemp[1]), int(dtemp[2]))
    return d
# Validators respectively to our XMLSchema (whether they're needed)

# def is_valid_passport(passport):
#   result = re.compile("[A-Z]{2}[0-9]{6}").match(passport)
#   return not result is None


class ValidClientId:
    def __init__(self, message=None):
        if not message:
            message = "There is no client with this Id"
        self.message = message

    def __call__(self, form, field):
        c_id = field.data
        xml.sax.parse('static/hotel.xml', ClientIdCheckHandler(c_id))
        if not ClientIdCheckHandler.flag:
            raise ValidationError(self.message)


class ValidRoomId:
    def __init__(self, message=None):
        if not message:
            message = "There is no room with this Id"
        self.message = message

    def __call__(self, form, field):
        r_id = field.data
        xml.sax.parse('static/hotel.xml', RoomIdCheckHandler(r_id))
        if not RoomIdCheckHandler.flag:
            raise ValidationError(self.message)


class ValidDates:
    def __init__(self, message=None):
        if not message:
            message = "These dates are invalid"
        self.message = message

    def __call__(self, form, field):
        if not form.date_from.data < form.date_to.data:
            raise ValidationError(self.message)


class AvailableDates:
    def __init__(self, message=None):
        if not message:
            message = "This date is not available"
        self.message = message

    def __call__(self, form, field):
        xml.sax.parse('static/hotel.xml', DateHandler(form.room_id.data, \
            [form.date_from.data, form.date_to.data]))
        if DateHandler.intersection:
            raise ValidationError(self.message)


class ValidForm:
    def __init__(self, message=None):
        if not message:
            message = "Information is not valid"
        self.message = message

    def __call__(self, form, field):
        xml.sax.parse('static/hotel.xml', DateHandler(form.room_id.data, \
            [form.date_from.data, form.date_to.data]))
        if DateHandler.intersection:
            raise ValidationError(self.message)


# def is_valid_date(doc, room_id, dates):
#     return sooner(dates[0], dates[1]) and is_available(doc, room_id, dates)
