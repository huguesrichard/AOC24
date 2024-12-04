# AOC24
my second attempt at the Advent of Code coding puzzles, 2024 edition

## Some notes from this year

- First star of day 2 took a little more time than expected because I misunderstood the puzzle, I was checking the values of the neighbhour difference when it was expected to consider any list with one element less
- On Day 4, for the first star I resisted the temptations to detect directly `XMAS` and it's reverse `SAMX` on a line because of the `S` or the `X` that can overlap. This has for effect that `XMASAMX` and `SAMXMAS` should each count 2 occurrence. It's possible to parametrize the regular expression to detect those overlapping matches, but I always found it tricky to do. I simply searched once on the string and one on its reverse. 
- 