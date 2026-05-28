from __future__ import annotations

from flask import request


def install_cors(app, origins: str) -> None:
    allowed = [item.strip() for item in origins.split(",") if item.strip()]

    @app.after_request
    def add_cors_headers(response):
        request_origin = request.headers.get("Origin")
        if "*" in allowed:
            response.headers["Access-Control-Allow-Origin"] = "*"
        elif request_origin in allowed:
            response.headers["Access-Control-Allow-Origin"] = request_origin
            response.headers["Vary"] = "Origin"
        elif allowed:
            response.headers["Access-Control-Allow-Origin"] = allowed[0]
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
        return response
