from portal import views
from portal.bootstrap import application

# Registers the blueprints
application.register_blueprint(views.proxy_bp)
application.register_blueprint(views.about_bp)


if __name__ == "__main__":
    # Point of entry
    application.run(host=application.config["HOST"], port=application.config["PORT"])
