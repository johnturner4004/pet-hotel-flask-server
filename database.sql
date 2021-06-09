CREATE TABLE "owner"(
	"id" SERIAL PRIMARY KEY,
	"name" VARCHAR(42),
	"number-of-pets" INT
	);

CREATE TABLE pets(
	"id" SERIAL PRIMARY KEY,
	"owner_id" INT REFERENCES "owner",
	"pet" VARCHAR(42) NOT NULL,
	"breed" VARCHAR(42) NOT NULL,
	"color" VARCHAR(42) NOT NULL,
	"check-in" VARCHAR(42) NOT NULL
);

INSERT INTO "owner" ("name", "number-of-pets")
VALUES
	('Chris', 2),
	('Ally', 1),
	('Dane', 1);

INSERT INTO pets (owner_id, pet, breed, color, "check-in") VALUES
	(1, 'Charlie', 'Shih-tzu', 'Black', 'no'),
	(1, 'Thorin', 'Rabbit', 'White', 'no'),
	(2, 'Gatsby', 'Cat', 'White', '5/5/18'),
	(3, 'Juniper', 'Cat', 'Tabby', 'no');