from hstest import SQLTest, dynamic_test, correct, wrong


class TestSQLProject(SQLTest):
    queries = {
        'create_table': None
    }

    @dynamic_test
    def test_queries(self):
        self.execute('create_table')

        result = self.db.execute("SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name;")

        if 'contacts' not in result.fetchall()[0]:
            return wrong("Can't find 'contacts' table in the database")

        return correct()
