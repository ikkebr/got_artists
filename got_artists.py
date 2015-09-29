from flask import Flask, render_template
from flask.ext.mongoengine import MongoEngine
from flask.views import View
from flask.json import JSONEncoder
from flask_wtf import Form
from wtforms import fields, validators

import json

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = 'as_w3g0tp0_pia' * 5
app.config["MONGODB_SETTINGS"] = {'DB': 'got_artists'}
app.config["WTF_CSRF_ENABLED"] = False


db = MongoEngine(app)


class Artists(db.Document):
    age = db.IntField(required=True)
    uuid = db.UUIDField(required=True)

    def __unicode__(self):
        return self.uuid

    def to_json(self):
        return {'uuid': self.uuid, 'age': self.age}

    meta = {
        'collection': 'artists',
        'strict': False
    }


class MongoEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Artists):
            return obj.to_json()
        return JSONEncoder.default(self, obj)


class SearchForm(Form):
    min_age = fields.IntegerField('Minimum age: ', validators=[
        validators.InputRequired(),
        validators.NumberRange(0, 150),
    ])

    max_age = fields.IntegerField('Maximum age: ', validators=[
        validators.InputRequired(),
        validators.NumberRange(0, 150)
    ])


class Search(View):
    methods = ['GET', 'POST']

    # sorting by distance to average value
    def search_fitness(self, x):
        return abs(x.age - abs(self.max_age + self.min_age) / 2.)

    def dispatch_request(self):
        form = SearchForm()

        if form.validate_on_submit():
            # lets assume our user wants to use both ages
            self.min_age, self.max_age = sorted(
                [form.min_age.data, form.max_age.data])

            artists = Artists.objects.filter(
                age__gte=self.min_age, age__lte=self.max_age)

            artists_list = sorted(artists, key=self.search_fitness)

            return json.dumps(artists_list, cls=MongoEncoder)

        # if we don't have a valid form on submit or if we are getting
        # we should redirect to another page instead of doing this
        return render_template('index.html', form=form)


app.add_url_rule('/', view_func=Search.as_view('artists'))

if __name__ == '__main__':
    app.run()
