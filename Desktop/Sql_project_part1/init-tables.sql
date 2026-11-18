-- drop table project.users cascade;
-- drop table project.games cascade;
-- drop table project.game_players cascade;
-- drop table project.stats cascade;
-- drop table project.achievements cascade;
-- drop table project.player_achievements cascade;
-- drop schema project;
-- create schema project;

create Table
    project.users (
        id serial primary key,
        username varchar(30) not null unique,
        fullname varchar(255) not null,
        password varchar(255) not null,
        email varchar(255) unique not null,
        check (
            email like '%@%.%'
            and length (email) >= 5
            and length (password) >= 12
            and length (username) >= 3
        )
    );

create Table
    project.games (
        gameId serial primary key,
        gameName varchar(255) not null
    );

create Table
    project.game_players (
        gameId int not null references project.games (gameId),
        playerId int not null references project.users (id),
        playerScore int not null,
        placement int not null,
        playTimes timestamp default NOW (),
        check (
            playerScore >= 0
            and placement <= 6
            and 0 >= placement
        ),
        primary key (gameId, playerId)
    );

create table
    project.stats (
        playerId int primary key references project.users (id),
        totalWins int,
        games_played int,
        win_percentage int
    );

create table
    project.achievements (
        Achievement_Id serial primary key,
        AchievementName varchar(255) unique,
        description varchar(255),
        gameId int references project.games (gameId)
    );

create table
    project.player_achievements (
        playerId int not null references project.users (id),
        Achievement_Id int not null references project.achievements (Achievement_Id),
        achieveDate date default NOW (),
        primary key (Achievement_Id, playerId)
    );