# AOC24
my second attempt at the Advent of Code coding puzzles, 2024 edition

## Some notes from this year

- First star of day 2 took a little more time than expected because I misunderstood the puzzle, I was checking the values of the neighbhour difference when it was expected to consider any list after dropping one element (which can be done simply by enumeration).
- On Day 4, for the first star I resisted the temptations to detect directly `XMAS` and it's reverse `SAMX` on a line because of the `S` or the `X` that can overlap. This has for effect that `XMASAMX` and `SAMXMAS` should each count 2 occurrence. It's possible to parametrize the regular expression to detect those overlapping matches, but I always found it tricky to do. I simply searched once on the string and one on its reverse. 
- Day 5 took me too much time because I wanted to compute the transitive closure of all of the '|' relationships. It turns out that all the relationship were specified and so the problem was much more easy (and my transitive closure attempt doesn't work either -_-).
- Day 8 was really easy on the first star using an integer recoding and numpy matrices. However I got confused with matrix redimensionning and 3D matrix products on star 2 and it took me an incredible amount of time to debug. Morality: sometimes it's better to stick with the easiest solution first. 
- Day 9, damn I did it too complicated for star 2, but it worked