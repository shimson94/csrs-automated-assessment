from .submissions import submissions_blueprint

# Register all blueprints here
def register_blueprints(app):
    """Register all application blueprints"""
    app.register_blueprint(submissions_blueprint, url_prefix="/api")
    
    # Future blueprints will be added here:
    # app.register_blueprint(auth_blueprint, url_prefix="/api/auth")
    # app.register_blueprint(assignments_blueprint, url_prefix="/api/assignments")
    # app.register_blueprint(files_blueprint, url_prefix="/api/files")