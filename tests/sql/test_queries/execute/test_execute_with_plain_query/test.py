from hstest import correct, dynamic_test, SQLTest, wrong


class TestSQLProject(SQLTest):
    queries = {
        'create_table': None
    }

    @dynamic_test
    def test_queries(self):
        self.execute("""CREATE TABLE contacts (
            contact_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL UNIQUE
        );""")

        result = self.db.execute("SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name;")

        if 'contacts' not in result.fetchall()[0]:
            return wrong("Can't find 'contacts' table in the database")

        return correct()
