from hstest.check_result import CheckResult
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest


class TestParametrizedData5(StageTest):
    test_data = [
        [[1]],
        [[2, 3]],
        [[3, 4, 5]],
        [[4, 5, 6, 7]],
        [[5, 6, 7, 8, 9]]
    ]

    counter = 0

    @dynamic_test(data=test_data)
    def test(self, a):
        self.counter += 1
        print(a)
        return CheckResult(self.counter == len(a), '')
