import os, os.path

import cherrypy

from webapp.libs.tools.satool import SATool
from webapp.libs.tools.makotool import MakoTool
from webapp.libs.plugins.saplugin import SAEnginePlugin
from webapp.libs.plugins.makoplugin import MakoTemplatePlugin

cur_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(cur_dir, 'templates')
template_cache_dir = os.path.join(cur_dir, 'templates', '.cache')
conf_dir = os.path.join(cur_dir, 'conf')
conf_path = os.path.join(cur_dir, 'conf', 'server.conf')

cherrypy.tools.db = SATool()
cherrypy.tools.render = MakoTool()

from webapp.app import RatingApp
app = RatingApp()
cherrypy.tree.mount(app, '/', conf_path)

MakoTemplatePlugin(cherrypy.engine, template_dir, template_cache_dir).subscribe()

db_uri = "mysql://%s:%s@%s:%s/theobject_rating" % (
    os.environ['THEOBJECTRATING_MYSQL_USER'],
    os.environ['THEOBJECTRATING_MYSQL_PASSWORD'],
    os.environ['THEOBJECTRATING_MYSQL_ADDR'],
    os.environ['THEOBJECTRATING_MYSQL_PORT']
)

# TODO: возиожно, SqlAlchemy нам и ни к чему, подумать об этом и избавиться от библиотеки при необходимости
cherrypy.engine.db = SAEnginePlugin(cherrypy.engine, db_uri)
cherrypy.engine.db.subscribe()

if os.environ['THEOBJECTRATING_DEBUG'] == 'TRUE':
    cherrypy.engine.start()
