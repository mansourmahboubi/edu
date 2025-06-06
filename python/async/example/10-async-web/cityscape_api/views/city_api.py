import flask
from services import location_service, sun_service, weather_service

blueprint = flask.blueprints.Blueprint("city_api", "city_api")


@blueprint.route("/api/weather/<zip_code>/<country>", methods=["GET"])
def weather(zip_code: str, country: str):
    weather_data = weather_service.get_current(zip_code, country)
    if not weather_data:
        flask.abort(404)
    return flask.jsonify(weather_data)


@blueprint.route("/api/sun/<zip_code>/<country>", methods=["GET"])
def sun(zip_code: str, country: str):
    lat, long = location_service.get_lat_long(zip_code, country)
    sun_data = sun_service.for_today(lat, long)
    if not sun_data:
        flask.abort(404)
    return flask.jsonify(sun_data)
