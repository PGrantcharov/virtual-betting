import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
        SECRET_KEY='dev',  
        # need to modify key for security later
        # By Po
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        # Not sure how to change it for our database
        # By Po
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
        # overrides the default configuration with values taken 
        # from the config.py file in the instance folder if it exists.
        # By Po

    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    ############## simple page demo ###########################################
    # a simple page that says hello
    @app.route('/sample')
    def sample():
        text = '''
        Each page can be renderred by html template, or just a function (app) output like this.
        The route name must be the same as fucntion name. 'sample' in this case.
        By Po
        '''
        return text
    ##############################################################################

    ############ database demo ###################################################
    from . import db 
    # need to import what we wrote in db
    db.init_app(app)
    # then initiate it
    ###############################################################################


    ############# auth, blueprint demo ############################################
    from . import auth
    app.register_blueprint(auth.bp)
    ###############################################################################


    ############# blog, blueprint, we can modify it to main betting page ##########
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    ###############################################################################

    return app