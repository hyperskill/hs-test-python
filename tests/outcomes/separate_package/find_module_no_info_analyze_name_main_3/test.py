from hstest.check_result import CheckResult
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.testing.tested_program import TestedProgram
from hstest.testing.unittest.user_error_test import UserErrorTest


class FindModuleNoInfoAnalyzeImports(UserErrorTest):
    contain = """
    Error in test #1
    
    Cannot decide which file to run out of the following: "main.py", "main4.py"
    They all have "if __name__ == \'__main__\'". Leave one file with this line.
    """

    @dynamic_test
    def test(self):
        main = TestedProgram()
        result = main.start()
        return CheckResult(
            result ==
            'Main 3\n'
            'Main 2\n', '')
