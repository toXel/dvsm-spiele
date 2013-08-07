drop table if exists scores;
create table scores (
	gameid integer primary key autoincrement,
	gametitle string not null,
	gameurl string not null,
    userid integer,
	userscore string not null,
	higherisbetter integer not null default 1,
	unit string,
	sort integer not null
);

drop table if exists users;
create table users (
    userid integer primary key autoincrement,
    username string not null,
    password string not null
);
