# ！/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (c) 2017-2020 Rhilip <rhilipruan@gmail.com>

import re
import time
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from utils.database import Database

ptboard_blueprint = Blueprint('ptboard', __name__)
ptboard_blueprint.config = {}


@ptboard_blueprint.record
def record_params(setup_state):
    app = setup_state.app
    ptboard_blueprint.config = dict([(key, value) for (key, value) in app.config.items()])


mysql = Database()
mysql.init_app(ptboard_blueprint)


@ptboard_blueprint.route("/ptboard")
@cross_origin()
def ptboard():
    search_raw = request.args.get("search") or ""
    order_raw = request.args.get("order") or "desc"
    limit_raw = request.args.get("limit") or 50
    offset_raw = request.args.get("offset") or 0

    t0 = time.clock()

    search = re.sub(r"[ _\-,.]", " ", search_raw)
    search = re.sub(r"\'", r"''", search)
    search = search.split()
    search = search[:10]
    if search:
        key = ["`title` LIKE '%{key}%'".format(key=i) for i in search]
        opt = " AND ".join(key)
    else:
        opt = "1=1"

    order = "desc" if order_raw not in ["desc", "asc"] else order_raw
    try:
        limit = int(limit_raw)
    except ValueError or TypeError:
        limit = 50
    try:
        offset = int(offset_raw)
    except ValueError or TypeError:
        offset = 0

    sql = "SELECT * FROM `rss_pt_site` WHERE {opt} ORDER BY `pubDate` {_da} LIMIT {_offset}, {_limit}".format(
        opt=opt, _da=order.upper(), _offset=offset, _limit=limit
    )
    rows_data = mysql.exec(sql=sql, r_dict=True, fetch_all=True)
    total_data = mysql.exec("SELECT `TABLE_ROWS` FROM `information_schema`.`TABLES` "
                            "WHERE `TABLE_NAME`='rss_pt_site'")[0]

    return jsonify({
        "cost": time.clock() - t0,
        "rows": rows_data,
        "total": total_data
    })