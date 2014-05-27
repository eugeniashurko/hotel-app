from flask import Flask, render_template, request, send_file, redirect, url_for
from werkzeug import DebuggedApplication
from lxml import etree
from clientadd import Client, add_client
from bookadd import Book, Payment, add_book
from forms import AddClientForm, BookForm
from wtforms import ValidationError

app = Flask(__name__)
app.wsgi_app = DebuggedApplication(app.wsgi_app, True)


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/rooms')
def list_of_rooms():
    xml_input = etree.XML(open('static/hotel.xml', 'r').read())
    xslt_root = etree.XML(open('static/roomsinfo.xsl', 'r').read())
    transform = etree.XSLT(xslt_root)
    output = transform(xml_input)
    with open('static/roomsinfo.html', 'w') as datasource:
            datasource.write(etree.tostring(output))
    return send_file('static/roomsinfo.html')


@app.route('/history')
def history():
    xml_input = etree.XML(open('static/hotel.xml', 'r').read())
    xslt_root = etree.XML(open('static/history.xsl', 'r').read())
    transform = etree.XSLT(xslt_root)
    output = transform(xml_input)
    with open('static/history.html', 'w') as datasource:
            datasource.write(etree.tostring(output))
    return send_file('static/history.html')


@app.route('/view/<int:room_id>')
def room_view(room_id):
    return 'Room view page'


# Forms will be here
@app.route('/newclient', methods=['GET', 'POST'])
def new_client():
    form = AddClientForm(request.form)
    if request.method == 'POST' and form.validate():
        client = Client()
        client.name = form.name.data
        client.surname = form.surname.data
        client.passport = form.passport.data
        client.address = form.address.data
        client.sex = form.sex.data
        try:
            add_client(client)
        except ValidationError as e:
            return render_template('clientform.html', form=form, ermes=e.message)
        return redirect(url_for('home_page'))
    return render_template('clientform.html', form=form)


@app.route('/book', methods=['GET', 'POST'])
def new_book():
    form = BookForm(request.form)
    if request.method == 'POST' and form.validate():
        book = Book()
        book.room_id = form.room_id.data
        book.dates = [form.date_from.data, form.date_to.data]
        book.client_id = form.client_id.data
        payment = Payment()
        payment.type = form.ptype.data
        payment.done = form.pdone.data
        book.payment = payment
        try:
            add_book(book)
        except ValidationError as e:
            return render_template('bookform.html', form=form, ermes=e.message)
        return redirect(url_for('history'))
    return render_template('bookform.html', form=form)


@app.route('/edit/<int:book_id>')
def edit_book(request):
    form = BookForm(request.POST)
    if request.method == 'POST' and form.validate():
        form.populate_obj(user)
        user.save()
        redirect('edit_profile')
    return render_response('edit_profile.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
