from flask import Flask, request
from jinja2 import Template
from datetime import datetime
from pathlib import Path


def render_last_node():
    global template, notes
    last_note = notes[-1] if notes else "none"
    return template.render(note=last_note)


def load_notes():
    dir = Path("./notes")

    read_notes = []
    for p in dir.iterdir():
        with open(p) as f:
            read_notes.append((f.read(), int(p.name[4])))

    if not read_notes:
        return []

    read_notes.sort(key=lambda x: x[1])
    notes = [x[0] for x in read_notes]

    return notes


app = Flask(__name__)

notes = load_notes()

load_notes()

with open("./templates/template.html") as f:
    template = Template(f.read())

html = render_last_node()


@app.route("/api/last_note")
def get_last_note():
    return html


@app.route("/api/create_note", methods={"POST"})
def create_note():
    global html

    body = request.get_json()

    content = body["content"]
    notes.append(content)

    html = render_last_node()

    with open(f"./notes/note{len(notes)}-{datetime.now()}.txt", "w") as f:
        f.write(content)

    return "Note added"


app.run(host="localhost", port=1234, debug=True)
