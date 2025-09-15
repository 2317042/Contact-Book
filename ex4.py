from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder=".")

# In-memory contacts store
contacts = []
next_id = 1

@app.route("/")
def home():
    return render_template("ex4.html")

@app.route("/api/contacts", methods=["GET"])
def get_contacts():
    query = request.args.get("search", "").lower()
    if query:
        filtered = [c for c in contacts if query in c["name"].lower() or query in c["phone"]]
        return jsonify(filtered)
    return jsonify(contacts)

@app.route("/api/contacts", methods=["POST"])
def add_contact():
    global next_id
    data = request.get_json() or {}
    name = data.get("name")
    phone = data.get("phone")
    if not name or not phone:
        return jsonify({"error":"Name and phone required"}), 400

    contact = {"id": next_id, "name": name, "phone": phone}
    contacts.append(contact)
    next_id += 1
    return jsonify(contact), 201

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
