import unittest

from hstest import SQLTest, dynamic_test, correct, wrong


class TestSQLProject(SQLTest):
    queries = {
        'create_table': None,
        'insert_data': None
    }

    @dynamic_test
    def test_create_table(self):
        self.db.execute(self.queries['create_table'])

        result = self.db.execute("SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name;")

        if 'contacts' not in result.fetchall()[0]:
            return wrong("Can't find 'contacts' table in the database")

        return correct()

    @dynamic_test
    def test_insert_data(self):
        self.db.execute(self.queries['insert_data'])
        result = self.db.execute("SELECT * FROM contacts").fetchall()[0]

        correct_result = [1, 'first_name', 'last_name', 'email', 'phone']

        if list(result) != correct_result:
            return wrong('Wrong data was inserted!')

        return correct()
