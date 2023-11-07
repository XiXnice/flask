import flask
from flask import jsonify, request, Response
from flask.views import MethodView
from models import Advertisements, Session
from sqlalchemy.exc import IntegrityError

app = flask.Flask('app')


class HttpError(Exception):

    def __init__(self, status_code: int, description: str):
        self.status_code = status_code
        self.description = description


@app.errorhandler(HttpError)
def error_handler(error):
    response = jsonify({'error': error.description})
    response.status_code = error.status_code
    return response


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response: Response):
    request.session.close()
    return response


def get_adv(adv_id: int):
    adv = request.session.get(Advertisements, adv_id)
    if adv is None:
        raise HttpError(404, 'user not found')
    return adv


def add_adv(adv: Advertisements):
    try:
        request.session.add(adv)
        request.session.commit()
    except IntegrityError as err:
        raise HttpError(409, 'user already exists')
    return adv


class AdvView(MethodView):

    @property
    def session(self) -> Session:
        return request.session

    def get(self, adv_id: int):
        adv = get_adv(adv_id)
        return jsonify({'id': adv.id, 'title': adv.title, 'description': adv.description, 'registration_time': adv.registration_time.isoformat(), 'owner': adv.owner})

    def post(self):
        adv_data = request.json
        new_adv = Advertisements(**adv_data)
        new_adv = add_adv(new_adv)
        return jsonify({'id': new_adv.id})

    def delete(self, adv_id: int):
        adv = get_adv(adv_id)
        self.session.delete(adv)
        self.session.commit()
        return jsonify({'status': 'ok'})


adv_view = AdvView.as_view('adv_view')

app.add_url_rule('/adv/<int:adv_id>', view_func=adv_view, methods=['GET', 'DELETE'])
app.add_url_rule('/adv', view_func=adv_view, methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True)
