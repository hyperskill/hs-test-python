from hstest.check_result import CheckResult, accept, wrong


def test_check_result():
    r = CheckResult.true()
    assert r.result
    assert r.feedback == ''

    r = CheckResult.false("hello")
    assert not r.result
    assert r.feedback == "hello"

    r = wrong('fff')
    assert not r.result
    assert r.feedback == 'fff'

    r = accept()
    assert r.result
    assert r.feedback == ""
