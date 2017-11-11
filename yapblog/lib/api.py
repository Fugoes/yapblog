"""
yapblog.lib.api

Library for creating json api.
"""

from flask import jsonify


def ok(**kwargs):
    kwargs["ok"] = True
    return jsonify(kwargs)


def not_ok(**kwargs):
    kwargs["ok"] = False
    return jsonify(kwargs)
