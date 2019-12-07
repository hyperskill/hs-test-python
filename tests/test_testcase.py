from hstest.test_case import TestCase


def test_testcase_attach():
    testcase = TestCase()
    assert testcase.attach is None

    attach = (1, "abc")
    testcase = TestCase(attach=attach)
    assert attach == testcase.attach

    testcase = TestCase(stdin='abc', copy_to_attach=True)
    assert testcase.attach == 'abc'

    testcase = TestCase(stdin='abc', attach=attach, copy_to_attach=True)
    assert testcase.attach == 'abc'


def test_testcase_stdin():
    testcase = TestCase()
    assert testcase.input == ''

    input = 'abc'
    testcase = TestCase(stdin=input)
    assert testcase.input == input
