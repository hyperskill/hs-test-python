from hstest import StageTest, dynamic_test, correct


class ProjectTest(StageTest):

    @dynamic_test()
    def test_something(self):
        print("I'm testing something")
        return correct()

    @dynamic_test()
    def test_something_again(self):
        print("I'm testing something again")
        return correct()
