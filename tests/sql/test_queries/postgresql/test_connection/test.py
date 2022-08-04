from hstest import SQLTest, dynamic_test, correct, wrong


class TestSQLProject(SQLTest):
    dialect = 'postgresql'
    connection_params = {
        'user': 'postgres',
        'password': '1'
    }
    queries = {
        'create_table': None
    }

    @dynamic_test
    def test_queries(self):
        self.execute('create_table')
        return correct()
