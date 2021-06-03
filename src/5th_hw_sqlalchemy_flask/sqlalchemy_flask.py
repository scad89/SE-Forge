from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine, ForeignKey, Float, select
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.sqltypes import Integer
from jinja2 import Template


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///currencies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db = SQLAlchemy(app)
db.create_all()
db.session.commit()


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
def hello_world():
    result = db.session.query(Currencies).all()
    return render_template('index.html', currency_1th=result)


if __name__ == '__main__':
    app.run(debug=True)
    db.create_all()


engine = create_engine('sqlite:///currencies.db', echo=True)
# connection = engine.connect()
meta = MetaData()


def output_all():
    s = select([currencies.c.name, rates.c.unit_cur, rates.c.date,
                rates.c.rate]).where(currencies.c.id == rates.c.id)
    result = conn.execute(s)
    return result.fetchall()


currencies = Table(
    'currencies', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('nbrb_id', Integer),
)

rates = Table(
    'rates', meta,
    Column('id', Integer, primary_key=True),
    Column('unit_cur', Integer),
    Column('date', String),
    Column('rate', Float),
    Column('currency_id', Integer, ForeignKey('currencies.id')))
meta.create_all(engine)
conn = engine.connect()

#s = select([currencies, rates]).where(currencies.c.id == rates.c.id)
# s = select([currencies.c.name, rates.c.unit_cur, rates.c.date,
#             rates.c.rate]).where(currencies.c.id == rates.c.id)
# result = conn.execute(s)
# print(result.fetchall())

print(output_all())


"""
вывод 
(1, 'USD', 12, 1, 31, '2021-05-25', 2.56)
(2, 'EUR', 13, 2, 32, '2021-05-25', 3.06)
"""
