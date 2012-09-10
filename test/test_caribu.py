""" Unit Tests for caribu module """


from alinea.caribu.caribu import caribu_run_case,CaribuOptionError


# Original test of caribu.csh script by M. Chelle
def test_caribu_script():
    for i in range(1,6):
        yield caribu_run_case,i#this makes nose generate 5 tests
        
def test_caribu_script_inconsistent():
    for i in range(1,3):
        yield caribu_run_inconsistent_case,i

def caribu_run_inconsistent_case(i):
    try:
        caribu_run_case(-i)
        assert False, "This test uses inconsistent options, it should raise an CaribuOptionError"
    except CaribuOptionError:
        assert True
