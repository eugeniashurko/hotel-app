import xml.sax
from lxml import etree
from wtforms import ValidationError


# Datastructure representing our client record
class Client:

    nextclientid = 0
    # Empty strings by default

    def __init__(self):
        xml.sax.parse('static/hotel.xml', NextIdHandler())
        self.id = Client.nextclientid + 1
        self.name = ""
        self.surname = ""
        self.passport = ""
        self.address = ""
        self.sex = ""
        Client.nextclientid = 0

    # This method converts object to node
    def convert_to_node(self, inputtree):
        # Create our node "cl:client"
        ns = "{http://www.example.com/clients}"
        clientnode = etree.Element(ns + "client", sex=self.sex)
        # Create and append nodes of client info records
        element = etree.SubElement(clientnode, ns + "id")
        element.text = str(self.id)
        element = etree.SubElement(clientnode, ns + "name")
        element.text = self.name
        element = etree.SubElement(clientnode, ns + "surname")
        element.text = self.surname
        element = etree.SubElement(clientnode, ns + "passport")
        element.text = self.passport
        element = etree.SubElement(clientnode, ns + "address")
        element.text = self.address

        return clientnode


class NextIdHandler(xml.sax.ContentHandler):

    def startElement(self, name, attributes):
        if name == "cl:client":
            Client.nextclientid += 1


# Adding client to database itself
def add_client(client):
    try:
        with open('static/hotel.xml', 'r+') as datasource:
                hoteltree = etree.parse(datasource)
        clientnode = client.convert_to_node(hoteltree)
        ns = "{http://www.example.com/clients}"
        element = hoteltree.find(ns + "clients")
        element.append(clientnode)

        xmlschema_doc = etree.parse('static/schemas/hotel.xsd')
        xmlschema = etree.XMLSchema(xmlschema_doc)
        xmlschema.assertValid(hoteltree)

        # Following is for overwriting the xml file
        with open('static/hotel.xml', 'w') as datasource:
            datasource.write(etree.tostring(hoteltree))

    except etree.DocumentInvalid as e:
        message = e.message
        if message.find("passport") == -1:
            if message.find("sex") == -1:
                if message.find("address") == -1:
                    raise ValidationError("Information is invalid")
                else:
                    raise ValidationError("Invalid address")
            else:
                raise ValidationError("Invalid sex: choose male or female")
        else:
            raise ValidationError("Invalid passport number (valid example AA123456)")
