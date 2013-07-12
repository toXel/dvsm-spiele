drop table if exists scores;
create table scores (
	gameid integer primary key autoincrement,
	gametitle string not null,
	gameurl string not null,
	timoscore string not null,
	jelescore string not null,
	higherisbetter integer not null default 1,
	unit string,
	sort integer not null
);