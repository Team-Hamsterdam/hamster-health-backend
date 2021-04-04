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

CREATE TABLE days (
    token string NOT NULL,
    date string NOT NULL,
    status boolean NOT NULL,
    completion int,
    note string,
    PRIMARY KEY (token, date),
    foreign key (token) references user(token)

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

INSERT INTO task (task_id, title, description, task_xp, is_custom) VALUES (1, "Run", "Run 1km", 5, 0);

-- INSERT INTO active_task (token, task_id, title, description, is_completed) VALUES ("{}", {}, "{}", "{}", 0);

-- INSERT INTO task (task_id, title, description, task_xp, is_custom) VALUES (1, "Run", "Run 1km", 5, 0);

-- select count(t.task_id) from task t

-- INSERT INTO task (task_id, title, description, xp, is_custom) values ({}, {}, {}, {}, {});

-- BEGIN TRANSACTION;
-- UPDATE task t
--    SET  t.title = {},
--         t.description = {}
--  WHERE t.id = {};
-- COMMIT;

-- select u.token from user.u where u.token = {}

-- select t.xp from task t where t.task_id = {};

-- select u.level, u.experience from user u where u.token = '{}';

-- BEGIN TRANSACTION;
--     UPDATE user u
--         SET u.level = {},
--             u.xp = {}
--     WHERE u.token = {};
-- COMMIT;

-- select t.task_id, t.title, t.description, t.task_xp from task
-- join active_task active on active.task_id = t.task_id
-- where active.token = {};

-- select u.username, u.level, u.xp from user u:

-- UPDATE user set logged_in = 1 where user.token = "{}";

-- SELECT u.username, u.level, u.xp
-- FROM user u
-- LIMIT 50
-- ORDER BY u.level DESC, u.xp DESC;

-- select task.task_id, task.title, task.description from task where task.token = "{}" and task.task_id = {};

-- UPDATE user
--     SET user.level = {},
--         user.xp = {}
-- WHERE user.token = "{}";