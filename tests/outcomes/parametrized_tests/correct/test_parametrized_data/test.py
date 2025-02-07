from hstest.check_result import CheckResult
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest


class TestParametrizedData(StageTest):
    test_data = [[1, 2], [2, 3], [3, 4], [4, 5], [5, 6]]

    counter = 0

    @dynamic_test(data=test_data)
    def test(self, a, b):
        self.counter += 1
        print(a, b)
        return CheckResult(self.counter == a and self.counter + 1 == b, "")
