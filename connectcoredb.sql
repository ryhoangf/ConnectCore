USE connectcore;

CREATE TABLE team (
    team_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    team_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    team_code VARCHAR(255) NOT NULL
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
    user_team_id INT NOT NULL,
    created_at TIMESTAMP,
    content TEXT NOT NULL
);

CREATE TABLE userteams (
    user_team_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    team_id INT NOT NULL,
    role VARCHAR(255),
    joined_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE script (
    script_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    user_team_id INT NOT NULL,
    content TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE userteams 
ADD CONSTRAINT FK_userteams_user FOREIGN KEY (user_id) REFERENCES user(user_id),
ADD CONSTRAINT FK_userteams_team FOREIGN KEY (team_id) REFERENCES team(team_id);

ALTER TABLE message 
ADD CONSTRAINT FK_message_userteam FOREIGN KEY (user_team_id) REFERENCES userteams(user_team_id);

ALTER TABLE script 
ADD CONSTRAINT FK_script_team FOREIGN KEY (user_team_id) REFERENCES userteams(user_team_id);