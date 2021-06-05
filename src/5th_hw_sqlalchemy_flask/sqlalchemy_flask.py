from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from flask import Flask, render_template, session
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
def home():
    id_cur = db.session.query(Currencies.id).all()
    return render_template('index.html', name=id_cur)


@app.route('/rate/<int:id_web>')
def rate(id_web):
    try:
        data_for_output = db.session.query(Currencies.id, Currencies.name, Rates.unit_cur, Rates.date, Rates.rate).join(
            Rates).filter(Currencies.id == id_web).first()
        return render_template('rate.html', output=data_for_output)
    except NoResultFound:
        return errors('Нет данных для выбранной валюты.')
    except MultipleResultsFound:
        return errors('Найдено несколько результатов.')


@app.route('/errors')
def errors(string_errors):
    return render_template('errors.html', type=string_errors)


if __name__ == '__main__':
    app.run()
