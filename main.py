import logging
from bottle import Bottle, request, response
from Models import Score
logging.getLogger().setLevel(logging.DEBUG)
import json


bottle = Bottle()
version = "v0.0.3"


@bottle.route('/')
def hello():
    return "Running " + version


@bottle.route('/crossdomain.xml')
def crossdomain_xml():
    crossdomain =  '<?xml version="1.0"?>'
    crossdomain =  crossdomain + '<!DOCTYPE cross-domain-policy SYSTEM "/xml/dtds/cross-domain-policy.dtd">'
    crossdomain =  crossdomain + '<cross-domain-policy>'
    crossdomain =  crossdomain + '<site-control permitted-cross-domain-policies="all"/>'
    crossdomain =  crossdomain + '<allow-access-from domain="*" to-ports="*" secure="false"/>'
    crossdomain =  crossdomain + '<allow-http-request-headers-from domain="*" headers="*" secure="false"/>' 
    crossdomain =  crossdomain + '</cross-domain-policy>'
    response.headers [ 'Content-Type' ] = 'text/xml'
    return crossdomain


@bottle.post('/score')
def post_score():
    try:
        name = request.json['name']
        score = request.json['score']
        score = Score(name=name, score=score)
        key = score.put()
        score = Score.get(key)
        return json.dumps(dict(score=score.score, name=score.name))
    except Exception as e:
        logging.exception(e)


@bottle.get('/scores')
def get_scores():
    try:
        query = Score.all().order("-score")
        return json.dumps(dict(scores=[dict(name=result.name, score=result.score) for result in query.run(limit=10)]))
    except Exception as e:
        logging.exception(e)


# Define an handler for 404 errors.
@bottle.error(404)
def error_404(error):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.'

