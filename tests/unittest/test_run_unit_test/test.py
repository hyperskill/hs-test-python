from hstest import dynamic_test, correct, TestCase, PlottingTest


class ProjectTest(PlottingTest):

    def generate(self):
        return [
            TestCase(stdin=[''])
        ]

    def check(self, reply: str, attach):
        print('print from generate')
        return correct()

    @dynamic_test()
    def test_something(self):
        print("I'm testing something")
        return correct()

    @dynamic_test()
    def test_something_again(self):
        print("I'm testing something again")
        return correct()
