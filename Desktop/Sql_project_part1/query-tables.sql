-- User Management
-- Validate that a username and password are correct.
-- Add a new user account.
insert into
    project.users
values
    (
        default,
        'Aras',
        'Aras Ahmet Yesiltan',
        'EnBuyukFenerbahce',
        'Aras@duru.com'
    );

-- Searching for accounts by name? Username?
select
    *
from
    project.users
where
    username ilike 'Aras';

select
    *
from
    project.users
where
    fullname ilike '%Aras%';

--both works fine but i didn't know how you wanted me to search so i just did it like this
-- Game Management
-- 5 most recently played games with player information.
select
    project.users.username,
    project.games.gameName,
    project.game_players.playerScore,
    project.game_players.placement,
    project.game_players.playTimes
from
    project.users
    join project.game_players on project.users.id = project.game_players.playerId
    join project.games on project.games.gameId = project.game_players.gameId
order by
    project.game_players.playTimes desc
limit
    5;

-- Show games completed by a player.
select
    project.users.username,
    project.games.gameName,
    project.game_players.playerScore,
    project.game_players.placement,
    project.game_players.playTimes
from
    project.users
    join project.game_players on project.users.id = project.game_players.playerId
    join project.games on project.games.gameId = project.game_players.gameId
where
    username ilike 'Aras';

-- Leaderboard & Stats
-- Show top 10 players by win rate who have played at least 3 games.
select
    project.users.username,
    project.stats.totalWins,
    project.stats.games_played,
    project.stats.win_percentage
from
    project.users
    join project.stats on project.users.id = project.stats.playerId
where
    project.stats.games_played >= 3
order by
    project.stats.win_percentage desc
limit
    10;

-- Achievements & Badges
-- List all badges unlocked by a specific player.
select
    project.users.username,
    project.player_achievements.achieveDate,
    project.achievements.AchievementName,
    project.achievements.description,
    project.games.gameName
from
    project.users
    join project.player_achievements on project.users.id = project.player_achievements.playerId
    join project.achievements on project.player_achievements.Achievement_Id = project.achievements.Achievement_Id
    join project.games on project.achievements.gameId = project.games.gameId
where
    project.users.username ilike 'Aras';

--I love alt + shift + f