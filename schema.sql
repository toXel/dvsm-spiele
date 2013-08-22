drop table if exists scores;
create table scores (
	gameid integer primary key autoincrement,
	gametitle string not null,
	gameurl string not null,
    userid integer,
	user1score string not null,
    user2score string not null,
	higherisbetter integer not null default 1,
	unit string,
	sort integer not null
);

drop table if exists users;
create table users (
    user1name string not null,
    user2name string not null
);

