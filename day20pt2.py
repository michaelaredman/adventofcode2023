from math import lcm

# we need th, bp, xc and pd to all fire for rx to be sent a low pulse
# all of these fire on cycles, with some of the cycles happening at a different
#  number of steps after the button on even and odd cycles
th = [4001, 8002]
bp = 3823
xc = [3847, 7694]
pd = [3877, 7754]

print(lcm(th[0], bp, xc[0], pd[0]))
# ok, that worked by chance
