from flask import Flask, request
from seminar8.sqlite_repository import connect, edit_user, delete_user, get_users, create_user
from flask_cors import CORS

DB_FILE = "/Users/luchicila/work/rau/teaching/rau-webappprogramming1/user_management_api/db/users.db"

app = Flask(__name__)
CORS(app)


@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        try:
            conn = connect(DB_FILE)
            data = get_users(conn)
            conn.close()
        except Exception as e:
            response = {
                "error": f"--Failed to connect to db or to get users. Error message: {e}."
            }
            return response, 500

        try:
            response = {
                "users": []
            }
            for row in data:
                # row = (id, username, first_name, last_name, email, password)
                element = {
                    "username": row[1],
                    "first_name": row[2],
                    "last_name": row[3],
                    "email": row[4],
                }
                response["users"].append(element)
            return response, 200
        except Exception as e:
            response = {
                "error": f"--Failed to process users information. Error message: {e}."
            }
            return response, 500

    if request.method == "POST":
        """
        {
            "username": "user name",
            "email": "email@me.com",
            "first_name": "first name",
            "last_name": "last name",
            "password": "password"
        }
        """
        user_data = request.json
        try:
            conn = connect(DB_FILE)
            create_user(conn, user_data)
            conn.close()
            return "", 200
        except ValueError as ve:
            error = {
                "error": f"--Invalid value provided user. Error message: {ve}."
            }
            return error, 400
        except Exception as e:
            error = {
                "error": f"--Failed to create user. Error message: {e}."
            }
            return error, 500


@app.route("/users/<user_id>", methods=["PUT", "DELETE"])
def update_user(user_id):
    user_id = int(user_id)
    if request.method == "PUT":
        try:
            user_details = request.json
            conn = connect(DB_FILE)
            edit_user(conn=conn, user_id=user_id, details=user_details)
            conn.close()
            return "", 200
        except Exception as e:
            error = {
                "error": f"Failed to update user. Error message: {e}"
            }
            return error, 500
    if request.method == "DELETE":
        try:
            conn = connect(DB_FILE)
            delete_user(conn=conn, user_id=user_id)
            conn.close()
            return "", 200
        except Exception as e:
            error = {
                "error": f"Failed to delete user. Error message: {e}"
            }
            return error, 500


if __name__ == "__main__":
    app.run(debug=True, port=3005)