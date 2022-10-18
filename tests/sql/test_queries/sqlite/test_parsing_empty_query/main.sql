create_book_table = "CREATE TABLE book (
    id INTEGER NOT NULL,
    isbn TEXT NOT NULL,
    book_name TEXT NOT NULL,
    book_type TEXT NOT NULL,
    book_aut TEXT NOT NULL,
    book_year INTEGER NOT NULL,
    book_amount INTEGER NOT NULL,
    book_page INTEGER NOT NULL,
    score REAL NOT NULL,
    CONSTRAINT pk_book_id PRIMARY KEY (id)
);
"



create_student_table = "CREATE TABLE student (
    id INTEGER NOT NULL,
    full_name TEXT NOT NULL,
    gender TEXT NOT NULL,
    date_of_birth TEXT NOT NULL,
    CONSTRAINT pk_student_id PRIMARY KEY (id)
);
"



create_staff_table = "CREATE TABLE staff (
    id INTEGER NOT NULL,
    full_name TEXT NOT NULL,
    gender TEXT NOT NULL,
    date_of_birth TEXT NOT NULL,
    CONSTRAINT pk_staff_id PRIMARY KEY (id)
);
"



create_operation_table = "CREATE TABLE operation (
    id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    staff_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    res_date TEXT NOT NULL,
    iss_date TEXT NOT NULL,
    is_iss NUMERIC NOT NULL,
    CONSTRAINT pk_operation_table PRIMARY KEY (id),
    CONSTRAINT fk_student_table FOREIGN KEY (student_id) REFERENCES student (id),
    CONSTRAINT fk_staff_table FOREIGN KEY (staff_id) REFERENCES staff (id),
    CONSTRAINT fk_book_table FOREIGN KEY (book_id) REFERENCES book (id)
);
"

insert_book_table = "INSERT INTO book
VALUES (1, ''0393347095'', ''The Metamorphosis'', ''Novella'', ''Franz Kafka'', 2014, 2, 128, 4.4),
       (2, ''0439358078'', ''Harry Potter And The Order Of The Phoenix'', ''Fantasy'', ''J.K. Rowling'', 2004, 3, 896,
        4.2),
       (3, ''0198800533'', ''Anna Karenina'', ''Realist Novel'', ''Leo Tolstoy'', 2017, 1, 896, 4.6);
"

insert_student_table = ""

insert_staff_table = ""

insert_operation_table = ""


