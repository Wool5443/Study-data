from flask import Flask, request
from jinja2 import Template
from datetime import datetime
from pathlib import Path


def render_last_note():
    global last_note_template, notes
    last_note = notes[-1] if notes else "none"
    return last_note_template.render(note=last_note)


def render_all_notes():
    global all_notes_template, notes
    return all_notes_template.render(notes=notes)


def load_notes():
    dir = Path("./notes")

    read_notes = []
    for p in dir.iterdir():
        with open(p) as f:
            try:
                note_index = int(p.name.split("-")[0][4:])
            except (ValueError, IndexError):
                continue
            read_notes.append((f.read(), note_index))

    if not read_notes:
        return []

    read_notes.sort(key=lambda x: x[1])
    notes = [x[0] for x in read_notes]

    return notes


app = Flask(__name__)

with open("./templates/template.html") as f:
    last_note_template = Template(f.read())
with open("./templates/all_notes.html") as f:
    all_notes_template = Template(f.read())
with open("./templates/create_note.html") as f:
    create_note_template = Template(f.read())

notes = load_notes()
last_note_html = render_last_note()
all_notes_html = render_all_notes()
create_note_html = create_note_template.render()


@app.route("/api/last_note")
def get_last_note():
    return last_note_html


@app.route("/")
@app.route("/add_note")
def get_add_note_page():
    return create_note_html


@app.route("/api/all_notes")
def get_all_notes():
    return all_notes_html


@app.route("/api/create_note", methods={"POST"})
def create_note():
    global last_note_html, all_notes_html

    body = request.get_json(silent=True) or {}
    content = body.get("content", "")
    content = content.strip()

    if not content:
        return "Content is required", 400

    notes.append(content)

    last_note_html = render_last_note()
    all_notes_html = render_all_notes()

    with open(f"./notes/note{len(notes)}-{datetime.now()}.txt", "w") as f:
        f.write(content)

    return "Note added"


app.run(host="localhost", port=1234, debug=True)
