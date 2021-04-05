-- cat hackiethon.sql | heroku pg:psql --app hackiethon-backend
CREATE TABLE user_table (
    token TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    logged_in INTEGER,
    level INTEGER,
    xp INTEGER,
    PRIMARY KEY (token)
);
CREATE TABLE task (
    token TEXT,
    task_id integer UNIQUE NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    task_xp integer,
    is_custom INTEGER,
    PRIMARY KEY (task_id),
    foreign key (token) references user_table(token)
);
CREATE TABLE active_task (
    token TEXT NOT NULL,
    task_id integer NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    is_completed INTEGER,
    PRIMARY KEY (token, task_id),
    foreign key (token) references user_table(token),
    foreign key (task_id) references task(task_id)
);
INSERT INTO task(task_id, title, description, task_xp, is_custom)
VALUES (1, 'Get fit!', 'Run 1km', 5, 0);
INSERT INTO task (task_id, title, description, task_xp, is_custom)
VALUES (2, 'Eat healthy!', 'Eat a fruit', 5, 0);
INSERT INTO task (task_id, title, description, task_xp, is_custom)
VALUES (3, 'Time to learn!', 'Learn something new', 5, 0);
INSERT INTO task (task_id, title, description, task_xp, is_custom)
VALUES (
        4,
        'Meditation time!',
        'Meditate for at least 5 minutes',
        5,
        0
    );
INSERT INTO task (task_id, title, description, task_xp, is_custom)
VALUES (
        5,
        'Study time!',
        'Do some studying or homework',
        5,
        0
    );
INSERT INTO task (task_id, title, description, task_xp, is_custom)
VALUES (
        6,
        'Reading time!',
        'Read a few pages of a book',
        5,
        0
    );
INSERT INTO task (task_id, title, description, task_xp, is_custom)
VALUES (
        7,
        'Meet someone new!',
        'Befriend a random person',
        5,
        0
    );
INSERT INTO task (task_id, title, description, task_xp, is_custom)
VALUES (
        8,
        'Talk to a friend!',
        'Talk to one of your friends',
        5,
        0
    );
INSERT INTO task (task_id, title, description, task_xp, is_custom)
VALUES (
        9,
        'Play with a friend!',
        'Play a game or do an activity with a friend',
        5,
        0
    );
INSERT INTO task (task_id, title, description, task_xp, is_custom)
VALUES (
        10,
        'Wake Up Early!',
        'Wake up before 10am',
        5,
        0
    );
INSERT INTO task (task_id, title, description, task_xp, is_custom)
VALUES (
        11,
        'Attend online class!',
        'Attend an online lecture or class',
        5,
        0
    );
INSERT INTO task (task_id, title, description, task_xp, is_custom)
VALUES (
        12,
        'Relax!',
        'Watch a movie or play some games',
        5,
        0
    );
INSERT INTO user_table (
        token,
        username,
        password,
        email,
        name,
        level,
        xp
    )
VALUES (
        '1AHUFeqweqwDHIfdasfwfUYDGQUYGQDUYGwefwefweDUYQGDYUHQBffwfwefIFHAIUGBFYIJUANffwfwFJ!@&*#BDNUXGYUewqeqwABSYBQUYGUYS*&!@Y8hhUIDJANKJXNIU87638712631@&*#YY*&!@HUH#NADJNIADnji',
        'Matthew',
        'cd6357efdd966de8c0cb2f876cc89ec74ce35f0968e11743987084bd42fb8944',
        'Matthew',
        'hamster',
        120,
        0
    );
INSERT INTO user_table (
        token,
        username,
        password,
        email,
        name,
        level,
        xp
    )
VALUES (
        '2AHUFeqweqwDHIfdasfwfUYDGQUYGQDUYGwefwefweDUYQGDYUHQBffwfwefIFHAIUGBFYIJUANffwfwFJ!@&*#BDNUXGYUewqeqwABSYBQUYGUYS*&!@Y8hhUIDJANKJXNIU87638712631@&*#YY*&!@HUH#NADJNIADnji',
        'Michael',
        'cd6357efdd966de8c0cb2f876cc89ec74ce35f0968e11743987084bd42fb8944',
        'Michael',
        'hamster',
        98,
        0
    );
INSERT INTO user_table (
        token,
        username,
        password,
        email,
        name,
        level,
        xp
    )
VALUES (
        '3AHUFeqweqwDHIfdasfwfUYDGQUYGQDUYGwefwefweDUYQGDYUHQBffwfwefIFHAIUGBFYIJUANffwfwFJ!@&*#BDNUXGYUewqeqwABSYBQUYGUYS*&!@Y8hhUIDJANKJXNIU87638712631@&*#YY*&!@HUH#NADJNIADnji',
        'Raymond',
        'cd6357efdd966de8c0cb2f876cc89ec74ce35f0968e11743987084bd42fb8944',
        'Raymond',
        'hamster',
        102,
        0
    );
INSERT INTO user_table (
        token,
        username,
        password,
        email,
        name,
        level,
        xp
    )
VALUES (
        '4AHUFeqweqwDHIfdasfwfUYDGQUYGQDUYGwefwefweDUYQGDYUHQBffwfwefIFHAIUGBFYIJUANffwfwFJ!@&*#BDNUXGYUewqeqwABSYBQUYGUYS*&!@Y8hhUIDJANKJXNIU87638712631@&*#YY*&!@HUH#NADJNIADnji',
        'Steven',
        'cd6357efdd966de8c0cb2f876cc89ec74ce35f0968e11743987084bd42fb8944',
        'Steven',
        'hamster',
        96,
        0
    );
INSERT INTO user_table (
        token,
        username,
        password,
        email,
        name,
        level,
        xp
    )
VALUES (
        '5AHUFeqweqwDHIfdasfwfUYDGQUYGQDUYGwefwefweDUYQGDYUHQBffwfwefIFHAIUGBFYIJUANffwfwFJ!@&*#BDNUXGYUewqeqwABSYBQUYGUYS*&!@Y8hhUIDJANKJXNIU87638712631@&*#YY*&!@HUH#NADJNIADnji',
        'Ethan',
        'cd6357efdd966de8c0cb2f876cc89ec74ce35f0968e11743987084bd42fb8944',
        'Ethan',
        'hamster',
        80,
        0
    );
INSERT INTO user_table (
        token,
        username,
        password,
        email,
        name,
        level,
        xp
    )
VALUES (
        '6AHUFeqweqwDHIfdasfwfUYDGQUYGQDUYGwefwefweDUYQGDYUHQBffwfwefIFHAIUGBFYIJUANffwfwFJ!@&*#BDNUXGYUewqeqwABSYBQUYGUYS*&!@Y8hhUIDJANKJXNIU87638712631@&*#YY*&!@HUH#NADJNIADnji',
        'Jonathan',
        'cd6357efdd966de8c0cb2f876cc89ec74ce35f0968e11743987084bd42fb8944',
        'Jonathan',
        'hamster',
        72,
        0
    );
INSERT INTO user_table (
        token,
        username,
        password,
        email,
        name,
        level,
        xp
    )
VALUES (
        '7AHUFeqweqwDHIfdasfwfUYDGQUYGQDUYGwefwefweDUYQGDYUHQBffwfwefIFHAIUGBFYIJUANffwfwFJ!@&*#BDNUXGYUewqeqwABSYBQUYGUYS*&!@Y8hhUIDJANKJXNIU87638712631@&*#YY*&!@HUH#NADJNIADnji',
        'Austin',
        'cd6357efdd966de8c0cb2f876cc89ec74ce35f0968e11743987084bd42fb8944',
        'Austin',
        'hamster',
        69,
        0
    );
INSERT INTO user_table (
        token,
        username,
        password,
        email,
        name,
        level,
        xp
    )
VALUES (
        '8AHUFeqweqwDHIfdasfwfUYDGQUYGQDUYGwefwefweDUYQGDYUHQBffwfwefIFHAIUGBFYIJUANffwfwFJ!@&*#BDNUXGYUewqeqwABSYBQUYGUYS*&!@Y8hhUIDJANKJXNIU87638712631@&*#YY*&!@HUH#NADJNIADnji',
        'Justin',
        'cd6357efdd966de8c0cb2f876cc89ec74ce35f0968e11743987084bd42fb8944',
        'Justin',
        'hamster',
        55,
        0
    );
INSERT INTO user_table (
        token,
        username,
        password,
        email,
        name,
        level,
        xp
    )
VALUES (
        '9AHUFeqweqwDHIfdasfwfUYDGQUYGQDUYGwefwefweDUYQGDYUHQBffwfwefIFHAIUGBFYIJUANffwfwFJ!@&*#BDNUXGYUewqeqwABSYBQUYGUYS*&!@Y8hhUIDJANKJXNIU87638712631@&*#YY*&!@HUH#NADJNIADnji',
        'Andrew',
        'cd6357efdd966de8c0cb2f876cc89ec74ce35f0968e11743987084bd42fb8944',
        'Andrew',
        'hamster',
        42,
        0
    );
INSERT INTO user_table (
        token,
        username,
        password,
        email,
        name,
        level,
        xp
    )
VALUES (
        '10AHUFeqweqwDHIfdasfwfUYDGQUYGQDUYGwefwefweDUYQGDYUHQBffwfwefIFHAIUGBFYIJUANffwfwFJ!@&*#BDNUXGYUewqeqwABSYBQUYGUYS*&!@Y8hhUIDJANKJXNIU87638712631@&*#YY*&!@HUH#NADJNIADnji',
        'Andy',
        'cd6357efdd966de8c0cb2f876cc89ec74ce35f0968e11743987084bd42fb8944',
        'Andy',
        'hamster',
        31,
        0
    );
INSERT INTO user_table (
        token,
        username,
        password,
        email,
        name,
        level,
        xp
    )
VALUES (
        '11AHUFeqweqwDHIfdasfwfUYDGQUYGQDUYGwefwefweDUYQGDYUHQBffwfwefIFHAIUGBFYIJUANffwfwFJ!@&*#BDNUXGYUewqeqwABSYBQUYGUYS*&!@Y8hhUIDJANKJXNIU87638712631@&*#YY*&!@HUH#NADJNIADnji',
        'Ronald',
        'cd6357efdd966de8c0cb2f876cc89ec74ce35f0968e11743987084bd42fb8944',
        'Ronald',
        'hamster',
        26,
        0
    );
INSERT INTO user_table (
        token,
        username,
        password,
        email,
        name,
        level,
        xp
    )
VALUES (
        '1AHUFeqweqwDHIfdasfwfUYDGQUYGQDUYGwefwefweDUYQGDYUHQBffwfwefIFHAIUGBFYIJUANffwfwFJ!@&*#BDNUXGYUewqeqwABSYBQUYGUYS*&!@Y8hhUIDJANKJXNIU87638712631@&*#YY*&!@HUH#NADJNIADnji2',
        'John',
        'cd6357efdd966de8c0cb2f876cc89ec74ce35f0968e11743987084bd42fb8944',
        'John',
        'hamster',
        14,
        0
    );
INSERT INTO user_table (
        token,
        username,
        password,
        email,
        name,
        level,
        xp
    )
VALUES (
        '1AHUFeqweqwDHIfdasfwfUYDGQUYGQDUYGwefwefweDUYQGDYUHQBffwfwefIFHAIUGBFYIJUANffwfwFJ!@&*#BDNUXGYUewqeqwABSYBQUYGUYS*&!@Y8hhUIDJANKJXNIU87638712631@&*#YY*&!@HUH#NADJNIADnji3',
        'Peterson',
        'cd6357efdd966de8c0cb2f876cc89ec74ce35f0968e11743987084bd42fb8944',
        'Peterson',
        'hamster',
        5,
        0
    );
INSERT INTO user_table (
        token,
        username,
        password,
        email,
        name,
        level,
        xp
    )
VALUES (
        'AHUFeqweqwDHIfdasfwfUYDGQUYGQDUYGwefwefweDUYQGDYUHQBffwfwefIFHAIUGBFYIJUANffwfwFJ!@&*#BDNUXGYUewqeqwABSYBQUYGUYS*&!@Y8hhUIDJANKJXNIU87638712631@&*#YY*&!@HUH#NADJNIADnji14',
        'Bryant',
        'cd6357efdd966de8c0cb2f876cc89ec74ce35f0968e11743987084bd42fb8944',
        'Bryant',
        'hamster',
        2,
        0
    );