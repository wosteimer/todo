CREATE TABLE todo(
    id UUID NOT NULL,
    content VARCHAR(24) NOT NULL,
    its_done BOOLEAN NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE(id),
    PRIMARY KEY (id)
);
