CREATE TABLE todo(
    id UUID NOT NULL,
    text TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    its_done BOOLEAN NOT NULL,
    UNIQUE(id),
    PRIMARY KEY (id)
);
