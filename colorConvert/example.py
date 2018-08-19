def hexrgba(_hex, wot=True):
    if wot: return tuple(int('{}{}'.format(_hex[-6:], 'FF')[i:i+2], 16) / 255.0 for i in (0, 2, 4, 6))
    return tuple(int('{}{}'.format(_hex[-6:], 'FF')[i:i+2], 16) for i in (0, 2, 4, 6))
    
def rgbahex(rgba):
    return "#{:02x}{:02x}{:02x}".format(int(rgba[0]), int(rgba[1]), int(rgba[2]))
    
print rgbahex((254, 14, 0, 255))
print hexrgba('#FE0E00') # convert to vector4 for wot
print hexrgba('#FE0E00', False)
