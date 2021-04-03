CREATE TABLE user (
    token string NOT NULL,
    username string UNIQUE NOT NULL,
    password string NOT NULL,
    email string UNIQUE NOT NULL,
    name string NOT NULL,
    level integer,
    xp integer,
    PRIMARY KEY (token)
);

CREATE table task (
    task_id integer NOT NULL,
    title string NOT NULL,
    description string,
    task_xp integer,
    is_custom boolean,
    PRIMARY KEY (task_id)
);

CREATE TABLE active_task (
    token string NOT NULL,
    task_id integer NOT NULL,
    is_completed boolean,
    PRIMARY KEY (token, task_id),
    foreign key (token) references user(token),
    foreign key (task_id) references tasks(task_id)
);

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