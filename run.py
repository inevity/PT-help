# ！/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (c) 2017-2020 Rhilip <rhilipruan@gmail.com>

from app import app
from modules.geo import geo_blueprint
from modules.ptboard import ptboard_blueprint
from modules.infogen import getinfo_blueprint

app.register_blueprint(geo_blueprint)
app.register_blueprint(ptboard_blueprint)
app.register_blueprint(getinfo_blueprint)


@app.route('/')
#def hello():
#    return "Hello world~"
def root():
    return app.send_static_file('ptboard.html')

@app.route('/ptgen')
def ptgen():
    return app.send_static_file('ptgen.html')

@app.route('/ptsearch')
def ptsearch():
    return app.send_static_file('ptsearch.html')


@app.route('/ptfenxi')
def ptfenxi():
    return app.send_static_file('ptanalytics.html')


  # or nginx server static file


if __name__ == '__main__':
    app.run(host="::")
