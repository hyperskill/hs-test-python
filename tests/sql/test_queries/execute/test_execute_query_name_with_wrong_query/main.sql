create_table = "CRE TABLE contacts (
	contact_id INTEGER PRIMARY KEY,
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL,
	email TEXT NOT NULL UNIQUE,
	phone TEXT NOT NULL UNIQUE
);"

insert_data = "INSERT INTO contacts VALUES(1, 'first_name', 'last_name', 'email', 'phone');"