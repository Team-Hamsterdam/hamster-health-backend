CREATE TABLE user (
    token string NOT NULL,
    username string UNIQUE NOT NULL,
    password string NOT NULL,
    email string UNIQUE NOT NULL,
    name string NOT NULL,
    logged_in boolen,
    level integer,
    xp integer,
    PRIMARY KEY (token)
);

CREATE TABLE task (
    token string,
    task_id integer UNIQUE NOT NULL,
    title string NOT NULL,
    description string,
    task_xp integer,
    is_custom boolean,
    PRIMARY KEY (task_id),
    foreign key (token) references user(token)
);

CREATE TABLE active_task (
    token string NOT NULL,
    task_id integer NOT NULL,
    title string NOT NULL,
    description string NOT NULL,
    is_completed boolean,
    PRIMARY KEY (token, task_id),
    foreign key (token) references user(token),
    foreign key (task_id) references tasks(task_id)
);

INSERT INTO task (task_id, title, description, task_xp, is_custom) VALUES (1, "Get fit!", "Run 1km", 5, 0);

INSERT INTO task (task_id, title, description, task_xp, is_custom) VALUES (2, "Eat healthy!", "Eat a fruit", 5, 0);

INSERT INTO task (task_id, title, description, task_xp, is_custom) VALUES (3, "Time to learn!", "Learn something new", 5, 0);

INSERT INTO task (task_id, title, description, task_xp, is_custom) VALUES (4, "Study time!", "Do some studying or homework", 5, 0);
