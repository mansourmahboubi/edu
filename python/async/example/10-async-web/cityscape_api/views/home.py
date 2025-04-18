import flask

blueprint = flask.blueprints.Blueprint("home", "home")


@blueprint.route("/")
def index():
    return (
        "Welcome to the city_scape API. "
        "Use /api/sun/[zipcode]/[country code (e.g. us)] and"
        "/api/weather/[zipcode]/[country code (e.g. us)] for API calls."
    )


@blueprint.errorhandler(404)
def not_found(_):
    return flask.Response("The page was not found.", status=404)
