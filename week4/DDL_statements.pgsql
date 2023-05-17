
DROP TABLE IF EXISTS lists, tasks, tag, tasks_tag;

CREATE TABLE IF NOT EXISTS lists (
    id SERIAL PRIMARY KEY,
    title varchar (25) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    list_id INT NOT NULL,
    task_title varchar (25) NOT NULL,
    task_description varchar (100) NOT NULL,
    CONSTRAINT fk_list FOREIGN KEY(list_id) REFERENCES lists(id) 
);

CREATE TABLE IF NOT EXISTS tag (
    id SERIAL PRIMARY KEY,
    tag_value varchar (15)
);

CREATE TABLE tasks_tag (
    task_id INT,
    tag_id INT,
    PRIMARY KEY (task_id, tag_id),
    CONSTRAINT fk_task FOREIGN KEY(task_id) REFERENCES tasks(id) ON DELETE CASCADE,
    CONSTRAINT fk_tag FOREIGN KEY (tag_id) REFERENCES tag(id) ON UPDATE NO ACTION ON DELETE CASCADE
);

INSERT INTO lists (title) VALUES ('supermarket');
INSERT INTO lists (title) VALUES ('gym');
INSERT INTO lists (title) VALUES ('doctor');

INSERT INTO tasks (list_id, task_title, task_description)
VALUES (1, 'milk','buy non fat milk');
INSERT INTO tag (tag_value) VALUES ('complete');
INSERT INTO tasks_tag (task_id, tag_id) VALUES (1, 1);

INSERT INTO tasks (list_id, task_title, task_description)
VALUES (1, 'hamburguer','buy 10 hamburguers');
INSERT INTO tag (tag_value) VALUES ('in process');
INSERT INTO tasks_tag (task_id, tag_id) VALUES (2, 2);

INSERT INTO tasks (list_id, task_title, task_description)
VALUES (2, 'arms','arms routine 15 minutes');
INSERT INTO tag (tag_value) VALUES ('todo');
INSERT INTO tasks_tag (task_id, tag_id) VALUES (3, 3);
INSERT INTO tag (tag_value) VALUES ('routine');
INSERT INTO tasks_tag (task_id, tag_id) VALUES (3, 4);

INSERT INTO tasks (list_id, task_title, task_description)
VALUES (2, 'legs','Legs routine 20 minutes');
INSERT INTO tag (tag_value) VALUES ('complete');
INSERT INTO tasks_tag (task_id, tag_id) VALUES (4, 5);
INSERT INTO tag (tag_value) VALUES ('routine');
INSERT INTO tasks_tag (task_id, tag_id) VALUES (4, 6);

INSERT INTO tasks (list_id, task_title, task_description)
VALUES (3, 'legs','knee revision');
INSERT INTO tag (tag_value) VALUES ('complete');
INSERT INTO tasks_tag (task_id, tag_id) VALUES (5, 7);
INSERT INTO tag (tag_value) VALUES ('revision');
INSERT INTO tasks_tag (task_id, tag_id) VALUES (5, 8);

INSERT INTO tasks (list_id, task_title, task_description)
VALUES (1, 'soda','buy 3 sodas');
