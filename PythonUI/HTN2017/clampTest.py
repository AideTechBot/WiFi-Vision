from scipy.interpolate import interp1d

OUTER_INPUT_RANGE = [10.0,80.0]
INPUT_RANGE = [30.0,60.0]

print (OUTER_INPUT_RANGE[0])

for fl in [20,10]:
    #interpolate to 0->1
    print fl
    print (OUTER_INPUT_RANGE[0] <= fl)
    print (INPUT_RANGE[0] >= fl)
    if OUTER_INPUT_RANGE[0] <= fl <= INPUT_RANGE[0]:
        print 'a'
        fl = INPUT_RANGE[0]
    if OUTER_INPUT_RANGE[1] >= fl >= INPUT_RANGE[1]:
        print 'b'
        fl = INPUT_RANGE[1]
    m   = interp1d(INPUT_RANGE, [0, 1])

    print fl
    fl = float(m(fl))

    print fl
    print '\n'