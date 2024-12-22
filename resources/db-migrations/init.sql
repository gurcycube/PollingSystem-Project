DROP TABLE IF EXISTS user_answers;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS questions;


CREATE TABLE questions (
    id int(11) NOT NULL AUTO_INCREMENT,
    q_title varchar(300) NOT NULL DEFAULT '',
    a1 varchar(300) NOT NULL DEFAULT '',
    a2 varchar(300) NOT NULL DEFAULT '',
    a3 varchar(300) NOT NULL DEFAULT '',
    a4 varchar(300) NOT NULL DEFAULT '',
    PRIMARY KEY (id)
);

CREATE TABLE users (
    id int(11) NOT NULL AUTO_INCREMENT,
    first_name varchar(300) NOT NULL DEFAULT '',
    last_name varchar(300) NOT NULL DEFAULT '',
    email varchar(300) NOT NULL DEFAULT '',
    age varchar(300) NOT NULL DEFAULT '',
    address varchar(300) NOT NULL DEFAULT '',
    joining_date datetime NOT NULL DEFAULT GETDATE(),
    is_registered boolean NOT NULL DEFAULT FALSE,
    PRIMARY KEY (id)
);

CREATE TABLE user_answers (
    id int(11) NOT NULL AUTO_INCREMENT,
    user_id int(11) NOT NULL,
    question_id int(11) NOT NULL DEFAULT '',
    answer int(11),
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id)
    FOREIGN KEY (question_id) REFERENCES questions(id)
);
