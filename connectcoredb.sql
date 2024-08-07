USE connectcore;

CREATE TABLE team (
    team_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    team_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user (
    user_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR(255),
    dob DATE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE message (
    message_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    team_id INT NOT NULL,
    user_id INT NOT NULL,
    content TEXT NOT NULL
);

CREATE TABLE teamtask (
    task_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    status VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL
);

CREATE TABLE task (
    task_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    team_id INT NOT NULL
);

CREATE TABLE personaltask (
    task_id INT NOT NULL,
    user_id INT NOT NULL,
    PRIMARY KEY (task_id, user_id)
);

CREATE TABLE userteams (
    user_team_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    team_id INT NOT NULL,
    role VARCHAR(255),
    joined_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE badges (
    badge_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE userbadges (
    user_badges_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    badge_id INT NOT NULL,
    awarded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE message 
ADD CONSTRAINT FK_message_team FOREIGN KEY (team_id) REFERENCES team(team_id),
ADD CONSTRAINT FK_message_user FOREIGN KEY (user_id) REFERENCES user(user_id);

ALTER TABLE task 
ADD CONSTRAINT FK_task_teamtask FOREIGN KEY (task_id) REFERENCES teamtask(task_id),
ADD CONSTRAINT FK_task_team FOREIGN KEY (team_id) REFERENCES team(team_id);

ALTER TABLE personaltask 
ADD CONSTRAINT FK_personaltask_teamtask FOREIGN KEY (task_id) REFERENCES teamtask(task_id),
ADD CONSTRAINT FK_personaltask_user FOREIGN KEY (user_id) REFERENCES user(user_id);

ALTER TABLE userteams 
ADD CONSTRAINT FK_userteams_user FOREIGN KEY (user_id) REFERENCES user(user_id),
ADD CONSTRAINT FK_userteams_team FOREIGN KEY (team_id) REFERENCES team(team_id);

ALTER TABLE userbadges 
ADD CONSTRAINT FK_userbadges_user FOREIGN KEY (user_id) REFERENCES user(user_id),
ADD CONSTRAINT FK_userbadges_badges FOREIGN KEY (badge_id) REFERENCES badges(badge_id);
