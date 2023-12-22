# the grid is split into four equally sized regions
# find distance to every point in the four regions

# each copy of the grid is split as follows
#  -------------------
#  |        :        |
#  |   2    :    1   |
#  |        :        |
#  |- - - - S - - - -|
#  |        :        |
#  |   3    :    4   |
#  |        :        |
#  -------------------

# 1 =======

# pattern A:
# for reaching 1 from the lower left, the count is:
# sum_{rs = 0}^steps 1 +  (steps - rs)
# = (steps + 1) + (steps + 1)*steps - 1/2 * (steps) * (steps + 1)
# = steps + 1 + steps^2 + steps - 1/2 steps^2 - 1/2 steps
# = 1/2 steps^2
# also need the zero term!

# we want the sum of this up to the:
# (total_steps - dist_to_point_from_corner) // (side_length * 2)
# symmetry gives us the similar terms

# now we just need the other ones

#  pattern B:
# 1 from lower right is simply
# (total_steps - dist_to_point_from_corner - side_length) // (side_length * 2)
# count is the same

# pattern C:
# exact same for 1 for upper left

#  pattern D:
# upper right is the same but with
#  (total_steps - dist_to_point_from_corner - side_length*2) // (side_length * 2)

# 2 =======
#

total_steps = 26_501_365
side_length = 66

# count[i] = number of subsquares of a given pattern and corner reached in i (side_length*2) steps
count = []


# sum(count[:(k+1)]) is the total number of these identical pattern and corners reachable from the zeroth case of this pattern
# in k steps
