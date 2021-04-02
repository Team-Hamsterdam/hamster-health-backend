CREATE TABLE user (
    token string NOT NULL,
    u_id integer NOT NULL,
    password string NOT NULL,
    name_first string NOT NULL,
    name_last string NOT NULL,
    level integer,
    experience integer,
    PRIMARY KEY (token)
)

CREATE table task (
    task_id integer NOT NULL,
    name string,
    description string,
    xp integer,
    PRIMARY KEY (task_id)
)

CREATE TABLE active task (
    token string NOT NULL,
    task_id integer NOT NULL,
    PRIMARY KEY (token, task_id),
    foreign key (token) references user(token),
    foreign key (task_id) references tasks(task_id)
)