from hstest.exception.outcomes import TestPassed as Tp, WrongAnswer as Wa


# old location of these classes to ensure backwards compatibility
TestPassed = Tp
WrongAnswer = Wa

# simple rename, but have to be sure old tests work as expected
TestPassedException = TestPassed
WrongAnswerException = WrongAnswer
