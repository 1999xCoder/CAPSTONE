import os; import json;
from auth import AuthError, requires_auth
from flask import Flask, request, abort, jsonify
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

def EXECUTE(test_config=None):
    ## CREATE & CONFIGURE ##
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db = SQLAlchemy()
    db.app = app
    db.init_app(app)
    CORS(app)

    ## DATABASE MODELS ##
    class Coders(db.Model):
        __tablename__ = "coders"
        id = Column(Integer, primary_key=True)

        username = Column(String, unique=True)

        def insert(self): db.session.add(self); db.session.commit();
        def delete(self): db.session.delete(self); db.session.commit();
        def update(self): db.session.commit();
        def __repr__(self): return json.dumps(self);

    class Programs(db.Model):
        __tablename__ = "programs"
        id = Column(Integer, primary_key=True)

        title = Column(String)
        description = Column(String)
        coderUsername =  Column(String)

        def insert(self): db.session.add(self); db.session.commit();
        def delete(self): db.session.delete(self); db.session.commit();
        def update(self): db.session.commit();
        def __repr__(self): return json.dumps(self);

    db.drop_all(); db.create_all();

    ## ENDPOINTS ##
    @app.route("/programs", methods=["GET"])
    def programs():
        try: return jsonify({
            "success": True,
                "programs": [ P.format() for P in Programs.query.all() ]
                });
        except: abort(422);

    @app.route("/coders", methods=["GET"])
    @requires_auth("get:coders") # USER & STAFF #
    def coders(payload):
        try: return jsonify({
            "success": True,
                "coders": [ C.format() for C in Coders.query.all() ]
                });
        except: abort(422);

    @app.route("/programs", methods=["POST"])
    @requires_auth("post:programs") # USER & STAFF #
    def newProgram(payload):
        try:
            data = request.get_json();
            try: Coders.query.filter(Coders.username == data["username"]);
            except: newCoder = Coders(username=data["username"]); newCoder.insert();
            newProgram = Programs(title=data["title"],
                                    description=data["description"],
                                        coderUsername=data["username"]);
            newProgram.insert();
            return jsonify({
                "success": True,
                    "program": [ newProgram ]
                    });
        except: abort(422);

    @app.route("/programs/<int:PID>", methods=["PATCH"])
    @requires_auth("patch:programs") # STAFF #
    def updateProgram(payload, PID):
        try:
            data = request.get_json();
            updateProgram = Programs.query.filter(Programs.id == int(PID));
            updateProgram.title = data.get("title", None);
            updateProgram.description = data.get("description", None);
            updateProgram.update();
            return jsonify({
                "success": True,
                    "program": [ updateProgram ]
                    });
        except: abort(422);

    @app.route("/programs/<int:PID>", methods=["DELETE"])
    @requires_auth("delete:programs") # STAFF #
    def deleteProgram(payload, PID):
        try:
            deleteProgram = Programs.query.get( int(PID) );
            deleteProgram.delete();
            return jsonify({
                "success": True,
                    "delete": int(PID)
                    });
        except: abort(422);

    ## ERRORS ##
    @app.errorhandler(401)
    def Unauthorized(_ErR_):
        return jsonify({
            "success": False,
                "error": 401,
                    "message": "Unauthorized"
                    }), 401;

    @app.errorhandler(422)
    def unprocessableEntity(_ErR_):
        return jsonify({
            "success": False,
                "error": 422,
                    "message": "Unprocessable Entity"
                    }), 422;

    @app.errorhandler(AuthError)
    def authError(_ErR_):
        return jsonify({
            "success": False,
                "error": 401,
                    "message": "ERR_MES :: " + _ErR_.error["message"]
                    }), 401;

    return app

app = EXECUTE();

if (__name__ == "__main__"): app.run(host="0.0.0.0", port=8080, debug=True);
