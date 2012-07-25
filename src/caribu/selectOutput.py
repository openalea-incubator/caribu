from label import decode_label


def selectOutput(EnergyLabel,variable):
    '''    split canestra output (Etri.vec) into a list of values and select an output
    '''
    
    if variable in ['Opt', 'Opak', 'Plt', 'Elt']:
        print('Warning!!!! Opt, Opak, Plt and Elt will be removed from caribu output in the future. Select label and use decode_label node instead')
        opt,opak,plt,elt = decode_label(EnergyLabel['label']) 
        EnergyLabel['Opt'] = opt
        EnergyLabel['Opak'] = opak
        EnergyLabel['Plt'] = plt
        EnergyLabel['Elt'] = elt
    # return outputs
    return EnergyLabel[variable],variable
