from portal import views
from portal.bootstrap import application

application.register_blueprint(views.proxy_bp)


if __name__ == "__main__":
    application.run(host=application.config["HOST"], port=application.config["PORT"])
