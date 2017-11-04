"""
yapb.lib.api

Library for creating json api.
"""

from flask import jsonify


def ok(msg=None):
    result = {"ok": True, "msg": msg}
    return jsonify(result)


def not_ok(msg=None):
    result = {"ok": False, "msg": msg}
    return jsonify(result)
