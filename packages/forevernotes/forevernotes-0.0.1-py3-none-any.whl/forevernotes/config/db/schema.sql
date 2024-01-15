CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY,
    creation_date TEXT NOT NULL,
    creation_time TEXT NOT NULL,
    last_modif_date TEXT NOT NULL,
    last_modif_time TEXT NOT NULL,
    note TEXT NOT NULL,
    color TEXT
);

CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY,
    creation_date TEXT NOT NULL,
    last_modif_date TEXT NOT NULL,
    tag TEXT NOT NULL,
    color TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS note_tags (
    note_id INTEGER,
    tag_id INTEGER,
    PRIMARY KEY (note_id, tag_id),
    FOREIGN KEY (note_id) REFERENCES notes(id),
    FOREIGN KEY (tag_id) REFERENCES tags(id)
);
