drop table if exists scores;
create table scores (
	gameid integer primary key autoincrement,
	gametitle string not null,
	gameurl string not null,
	gamer1name string not null,
	gamer2name string not null,
	gamer1score string not null,
	gamer2score string not null,
	higherisbetter integer not null default 1,
	unit string,
	sort integer not null
);
