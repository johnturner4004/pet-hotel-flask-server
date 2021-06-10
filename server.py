import flask
import psycopg2
from flask import request, jsonify
from psycopg2.extras import RealDictCursor

app = flask.Flask(__name__)
app.config["DEBUG"] = True


connection = psycopg2.connect(
    user="john", host="127.0.0.1", port="5432", database="pet-hotel"
)


@app.route("/", methods=["GET"])
def home():
    return "<h1>Hello World!</h1><p>From Python and Flask!</p>"


@app.route("/api/pets", methods=["GET"])
def list_pets():
    # Use RealDictCursor to convert DB records into Dict objects
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    postgreSQL_select_Query = (
        'SELECT * FROM pets JOIN "owner" ON pets.owner_id = "owner".id'
    )
    # execute query
    cursor.execute(postgreSQL_select_Query)
    # Selecting rows from mobile table using cursor.fetchall
    pets = cursor.fetchall()
    # respond, status 200 is added for us
    return jsonify(pets)


@app.route("/api/pets", methods=["POST"])
def create_pet():
    print("request.json is a dict!", request.json)
    print(
        "if you're using multipart/form data, use request.form instead!", request.form
    )
    ownerId = request.form["owner_id"]
    pet = request.form["pet"]
    breed = request.form["breed"]
    color = request.form["color"]
    checkIn = request.form["check-in"]
    print(ownerId, pet, breed, color, checkIn)
    try:
        # Avoid getting arrays of arrays!
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        insertQuery = 'INSERT INTO pets (owner_id, pet, breed, color, "check-in") VALUES (%s, %s, %s, %s, %s)'
        # if only only one param, still needs to be a tuple --> cursor.execute(insertQuery, (title,)) <-- comma matters!
        cursor.execute(
            insertQuery,
            (
                ownerId,
                pet,
                breed,
                color,
                checkIn,
            ),
        )
        # really for sure commit the query
        connection.commit()
        count = cursor.rowcount
        print(count, "Pet inserted")
        # respond nicely
        result = {"status": "CREATED"}
        return jsonify(result), 201
    except (Exception, psycopg2.Error) as error:
        # there was a problem
        print("Failed to insert pet", error)
        # respond with error
        result = {"status": "ERROR"}
        return jsonify(result), 500
    finally:
        # clean up our cursor
        if cursor:
            cursor.close()


app.run()
