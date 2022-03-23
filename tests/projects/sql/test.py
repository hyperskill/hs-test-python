from hstest import SQLTest, dynamic_test, correct, wrong


class TestSQLProject(SQLTest):

    queries = {
        'create_table': None,
        'test': None
    }

    @dynamic_test()
    def simple_test(self):
        for query in self.queries:
            if self.queries[query] is None:
                return wrong(f"Can't find '{query}' query from SQL files!")
        return correct()
