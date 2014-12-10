"""
Test the generic light tutorial with caribu
"""


from alinea.adel.data_samples import adel_two_metamers

# step 1 create g

g = adel_two_metamers()

# inspect geometry

g.property('geometry')


