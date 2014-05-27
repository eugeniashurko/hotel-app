import xml.sax
from datetime import date
from lxml import etree
from wtforms import ValidationError


class Payment:

    def __init__(self):
        self.type = ""
        self.done = ""
        self.total_summ = str(PriceHandler.total_summ)
        self.currency = "USD"
        PriceHandler.total_summ = 0

    def convert_to_node(self, inputtree):
        ns = "{http://www.example.com/history}"
        paynode = etree.Element(ns + "payment")
        element = etree.SubElement(paynode, ns + "type")
        element.text = self.type
        element = etree.SubElement(paynode, ns + "done")
        element.text = self.done
        element = etree.SubElement(paynode, ns + "total_summ", currency=self.currency)
        element.text = self.total_summ

        return paynode


class Book:

    nextbookid = 0

    def __init__(self):
        xml.sax.parse('static/hotel.xml', NextIdHandler())
        self.id = Book.nextbookid + 1
        self.dates = ["", ""]
        self.room_id = ""
        self.client_id = ""
        self.payment = Payment()
        Book.nextbookid = 0

    def convert_to_node(self, inputtree):
        ns = "{http://www.example.com/history}"
        # Create our node "hi:book"
        booknode = etree.Element(ns + "book")
        # Create and append nodes of book info records
        element = etree.SubElement(booknode, ns + "book_id")
        element.text = str(self.id)
        datenode = etree.SubElement(booknode, ns + "dates")
        element = etree.SubElement(datenode, ns + "from")
        element.text = str(self.dates[0])
        print self.dates
        print str(self.dates[0])
        element = etree.SubElement(datenode, ns + "to")
        print str(self.dates[1])
        element.text = str(self.dates[1])
        element = etree.SubElement(booknode, ns + "room_id")
        element.text = str(self.room_id)
        element = etree.SubElement(booknode, ns + "client_id")
        element.text = str(self.client_id)
        booknode.append(self.payment.convert_to_node(inputtree))

        return booknode


class NextIdHandler(xml.sax.ContentHandler):

    def startElement(self, name, attributes):
        if name == "hi:book":
            Book.nextbookid += 1


class PriceHandler(xml.sax.ContentHandler):
    # 0 - external state
    # 1 - inside room id
    # 2 - inside price
    state = 0

    current_id = ""
    total_summ = 0

    def __init__(self, room_id, dates):
        xml.sax.ContentHandler.__init__(self)
        PriceHandler.room_id = room_id
        PriceHandler.days = count_days(dates)

    def startElement(self, name, attributes):
        if name == "ro:room_id":
            PriceHandler.state = 1
        if name == "ro:price":
            PriceHandler.state = 2

    def endElement(self, name):
        if name == "ro:room_id":
            PriceHandler.state = 0
        elif name == "ro:price":
            PriceHandler.state = 0

    def characters(self, content):
        if (content.strip() != ""):
            if PriceHandler.state == 1:
                PriceHandler.current_id = str(content)
            elif PriceHandler.state == 2:
                if PriceHandler.current_id == PriceHandler.room_id:
                    PriceHandler.total_summ = str(float(content) * PriceHandler.days)


def count_days(d):
    delta = d[1] - d[0]
    return delta.days


def add_book(book):
    try:
        with open('static/hotel.xml', 'r+') as datasource:
                hoteltree = etree.parse(datasource)
        xml.sax.parse('static/hotel.xml', PriceHandler(book.room_id, book.dates))
        print PriceHandler.total_summ
        book.payment.total_summ = PriceHandler.total_summ
        booknode = book.convert_to_node(hoteltree)
        ns = "{http://www.example.com/history}"
        element = hoteltree.find(ns + "history")
        element.append(booknode)

        xmlschema_doc = etree.parse('static/schemas/hotel.xsd')
        xmlschema = etree.XMLSchema(xmlschema_doc)
        xmlschema.assertValid(hoteltree)
        # Following is for overwriting the xml file
        with open('static/hotel.xml', 'w') as datasource:
            datasource.write(etree.tostring(hoteltree))

    except etree.DocumentInvalid as e:
        message = e.message
        if message.find("from") == -1:
            if message.find("to") == -1:
                raise ValidationError("Information is invalid")
            else:
                raise ValidationError("Invalid date (valid example 2011-01-01)")
        else:
            raise ValidationError("Invalid date (valid example 2011-01-01)")
