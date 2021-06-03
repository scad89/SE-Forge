from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
db.create_all()


class Currencies(db.Model):
    __tablename__ = 'currencies'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    nbrb_id = db.Column(db.Integer)

    def __repr__(self):
        return '<currencies %r>' % self.id


class Rates(db.Model):
    __tablename__ = 'rates'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    unit_cur = db.Column(db.Integer)
    date = db.Column(db.String, nullable=False)
    rate = db.Column(db.Float)
    currency_id = db.Column(db.Integer, db.ForeignKey('currencies.id'))

    def __repr__(self):
        return '<rates %r>' % self.id


@app.route('/')
@app.route('/home')
@app.route('/index')
def hello_world():
    name = Currencies.query.all()
    return render_template('index.html', name=name)


@app.route('/rate/<int:id>')
def rate(id):
    rate = Rates.query.get(id)
    name = Currencies.query.get(id)
    return render_template('rate.html', unit=rate, name=name, date=rate, rate=rate)


if __name__ == '__main__':
    app.run()
