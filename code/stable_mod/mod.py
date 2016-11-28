
def stable_mod(x,b,bmask):
    if (x & bmask) < b:
        return x & bmask
    else:
        return x & (bmask >> 1)

bmask=19
x = 89

for b in range(10,1000):
    print stable_mod(x,b,bmask)
