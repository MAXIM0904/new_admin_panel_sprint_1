CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE IF NOT EXISTS content.film_work (
	id uuid PRIMARY,
	title TEXT NOT NULL,
	description TEXT,
	creation_date DATE,
	rating FLOAT,
	type TEXT NOT NULL,
	created timestamp with time zone,
	modified timestamp with time zone
);

CREATE UNIQUE INDEX IF NOT EXISTS film_work_idx
	ON content.film_work (creation_date);

CREATE TABLE IF NOT EXISTS content.genre (
	id uuid PRIMARY KEY,
	name TEXT NOT NULL,
	description TEXT,
	created timestamp with time zone,
	modified timestamp with time zone
);

CREATE UNIQUE INDEX IF NOT EXISTS genre_idx
	ON content.genre (description);

CREATE TABLE IF NOT EXISTS content.person (
	id uuid PRIMARY KEY,
	full_name TEXT NOT NULL,
	created timestamp with time zone,
	modified timestamp with time zone
);

CREATE UNIQUE INDEX IF NOT EXISTS person_idx
	ON content.person (full_name);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
	id uuid PRIMARY KEY,
	genre_id uuid NOT NULL,
	film_work_id uuid NOT NULL,
	created timestamp with time zone,
	FOREIGN key (genre_id) REFERENCES content.genre (id) ON DELETE CASCADE,
	FOREIGN key (film_work_id) REFERENCES content.film_work (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS content.person_film_work (
	id uuid PRIMARY KEY,
	person_id uuid NOT NULL,
	film_work_id uuid NOT NULL,
	role TEXT,
	created timestamp with time zone,
	FOREIGN key (person_id) REFERENCES content.person (id) ON DELETE CASCADE,
	FOREIGN key (film_work_id) REFERENCES content.film_work (id) ON DELETE CASCADE
);

CREATE UNIQUE INDEX IF NOT EXISTS person_film_work_idx
	ON content.person_film_work (role);
