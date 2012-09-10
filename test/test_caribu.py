""" Unit Tests for caribu module """


from alinea.caribu.caribu import caribu_run_case,CaribuOptionError


# Original test of caribu.csh script by M. Chelle
def test_caribu_script():
    caribu_run_case(1)
    caribu_run_case(2)
    caribu_run_case(3)
    caribu_run_case(4)
    caribu_run_case(5)
    try:
        caribu_run_case(-1)
        assert False, "This test should raise an CaribuOptionError"
    except CaribuOptionError:
        assert True
    try:
        caribu_run_case(-2)
        assert False, "This test should raise an CaribuOptionError"
    except CaribuOptionError:
        assert True