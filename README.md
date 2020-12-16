# meeting-problem

**Solution to a Meeting Scheduling Problem**

## Overview

This is a coding problem I selected semi-randomly from a collection of problems online. I figured out the solution myself and wrote the code myself. Please respect my effort and credit me if you use this code.

## The problem

A company has a single meeting room. There are N potential meetings that might happen over the course of the day. Each meeting has an already-known start time and end time. Some combinations of meetings aren't possible. The goal is to choose a combination of meetings that maximizes the number that actually take place.

Below, a set of potential meetings (from the program's output). `a` and `b` are scheduled at the very beginning of the day.
```
-------------------------------------------
0:  aaaaaaaaaaaaa
1:  bb
2:    cccc
3:      dddd
4:       eee
5:           ffffff
6:           gggg
7:            h
8:             iiiiiiiiiii
9:                 jjjjjjjj
```

Several combination that achieve the highest possible score, 4
```
(b,c,h,i)
(b,d,h,i)
(b,e,h,i)
```

## The solution

From my explorations of a recursive solution to an earlier coding problem, it occurred to me to use a recursive process again. I pondered the problem for a while, went to bed, and had the answer when I woke up the next day.

The idea is this: given N potential meetings, which I'll refer to as "items", the solution is to first generate all possible valid combinations of the first N-1 items, with a score assigned to each combination. Once that's done, we attempt to combine item N with the existing combinations, generating new combinations. Then, out of the total set of combinations, we choose the one with the highest score.

The solution for the first N-1 items is simply a recursion of the general solution. To solve the problem for only the first item yields only two possible combinations: that item (score of 1) or no items at all (score of 0). Solving the problem for the first *TWO* items yields as many as four possible combinations, or as few as three. 

### A further optimization:

Once we've generated all combinations for a given subset, `1...n`, we observe that there only N - n remaining points that can be collected. I'll pick `m = N - n` to represent that. Thus, if m points are available, we can discard combinations which score so badly that adding m points can't possibly beat the best existing combinations in subset `1...n`.

## Testing

The test code does the following, after creating a predefined set of meetings:
* Try to combine some items, yielding combinations that work
* Test several different combinations for clashes
* Run the algorithm several times, after sorting the predefined set of meetings into different orders

## Sample Output

```
Meeting list with sort method: none
meetings are
-------------------------------------------
0:           aaaaaa
1:  bbbbbbbbbbbbb
2:      cccc
3:             ddddddddddd
4:  ee
5:       fff
6:            g
7:                 hhhhhhhh
8:           iiii
9:    jjjj
------
subset: 0
combos: (),(a)
removed:
best score: 1
removal score: 0
------
subset: 1
combos: (a),(b),()
removed:
best score: 1
removal score: -
------
subset: 2
combos: (a,c),(a),(b),(c),()
removed:
best score: 2
removal score: -
------
subset: 3
combos: (a,c),(c,d),(a),(b),(c),(d),()
removed:
best score: 2
removal score: -
------
subset: 4
combos: (a,c,e),(c,d,e),(a,c),(c,d),(a,e),(c,e),(d,e),(a),(b),(c),(d),(e),()
removed:
best score: 3
removal score: -
------
subset: 5
combos: (a,c,e),(c,d,e),(a,e,f),(d,e,f),(a,c),(c,d),(a,e),(c,e),(d,e),(a,f),(d,f),(e,f),(a),(b),(c),(d),(e),(f),()
removed:
best score: 3
removal score: -
------
subset: 6
combos: (c,d,e,g),(d,e,f,g),(a,c,e),(c,d,e),(a,e,f),(d,e,f),(c,d,g),(c,e,g),(d,e,g),(d,f,g),(e,f,g),(a,c),(c,d),(a,e),(c,e),(d,e),(a,f),(d,f),(e,f),(c,g),(d,g),(e,g),(f,g)
removed: (a),(b),(c),(d),(e),(f),(g),()
best score: 4
removal score: 1
------
subset: 7
combos: (c,d,e,g),(d,e,f,g),(a,c,e,h),(a,e,f,h),(c,e,g,h),(e,f,g,h),(a,c,e),(c,d,e),(a,e,f),(d,e,f),(c,d,g),(c,e,g),(d,e,g),(d,f,g),(e,f,g),(a,c,h),(a,e,h),(c,e,h),(a,f,h),(e,f,h),(c,g,h),(e,g,h),(f,g,h)
removed: (a,c),(c,d),(a,e),(c,e),(d,e),(a,f),(d,f),(e,f),(c,g),(d,g),(e,g),(f,g)
best score: 4
removal score: 2
------
subset: 8
combos: (c,d,e,g),(d,e,f,g),(a,c,e,h),(a,e,f,h),(c,e,g,h),(e,f,g,h),(c,e,h,i),(e,f,h,i)
removed: (a,c,e),(c,d,e),(a,e,f),(d,e,f),(c,d,g),(c,e,g),(d,e,g),(d,f,g),(e,f,g),(a,c,h),(a,e,h),(c,e,h),(a,f,h),(e,f,h),(c,g,h),(e,g,h),(f,g,h)
best score: 4
removal score: 3
------
subset: 9
combos: (c,d,e,g),(d,e,f,g),(a,c,e,h),(a,e,f,h),(c,e,g,h),(e,f,g,h),(c,e,h,i),(e,f,h,i)
removed:
best score: 4
removal score: 3
-------
final outcome
(c,d,e,g)
(d,e,f,g)
(a,c,e,h)
(a,e,f,h)
(c,e,g,h)
(e,f,g,h)
(c,e,h,i)
(e,f,h,i)
```