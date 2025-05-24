# meeting-problem

**Solution to a Meeting Scheduling Problem**

## 2025 Note

To potential employers: I created this back in 2020. My Python skills have improved a great deal since then.

## Overview

_Original Text:_

This is a coding problem I selected semi-randomly from a collection of problems online. My work here is entirely original. I deliberately spelled out my thought process.

## The problem

![](images/MeetingWithTheBobs.jpg) 

`from "Office Space"`

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

### Still more optimization through initial sorting

Given a set of potential meetings, we can sort them into different orders before presenting them to the algorithm:

Sort method | Description
------------|-----------
`none`|No sorting
`start`|Sort by start time
`shortest`|Sort from shortest to longest
`longest`|Sort from longest to shortest

Stat collection shows that pre-sorting by start time is generally the best, and pre-sorting from shortest to longest is the worst.

```
Best sort method
    none: 6
    start: 53
    shortest: 0
    longest: 41
Worst sort method
    none: 4
    start: 0
    shortest: 96
    longest: 0
```

![](images/ByePrinter.jpg)

`You are the worst, shortest-to-longest` 

## Testing

Run with:

> python MeetingProblem --test CODE

Code | Description
------------|-----------
0     | Predefined meetings. Try to combine some items, yielding combinations that work. Test several different combinations for clashes
1 | Predefined meetings. Run the algorithm several times, after sorting the predefined set of meetings into different orders.
2 | Generate a random set of meetings. Run the algorithm several times, after sorting the predefined set of meetings into different orders.
3 | Generate many sets of meetings. Determine which pre-sorting method is best on average, which is worst.

## Potential Improvements

* Allow for some meetings to have a higher priority (a higher score)
* Allow the company to have multiple meeting rooms

Neither improvement would be difficult to implement. In the latter case, a single combination would list the meetings in each room as separate sets.

## Sample Output

This is for an unsorted set of meetings:
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
combos: 2 (),(a)
removed: 0
best score: 1
removal score: 0
------
subset: 1
combos: 3 (a),(b),()
removed: 0
best score: 1
removal score: -
------
subset: 2
combos: 5 (a,c),(a),(b),(c),()
removed: 0
best score: 2
removal score: -
------
subset: 3
combos: 7 (a,c),(c,d),(a),(b),(c),(d),()
removed: 0
best score: 2
removal score: -
------
subset: 4
combos: 13 (a,c,e),(c,d,e),(a,c),(c,d),(a,e),(c,e),(d,e),(a),(b),(c),(d),(e),()
removed: 0
best score: 3
removal score: -
------
subset: 5
combos: 19 (a,c,e),(c,d,e),(a,e,f),(d,e,f),(a,c),(c,d),(a,e),(c,e),(d,e),(a,f),(d,f),(e,f),(a),(b),(c),(d),(e),(f),()
removed: 0
best score: 3
removal score: -
------
subset: 6
combos: 23 (c,d,e,g),(d,e,f,g),(a,c,e),(c,d,e),(a,e,f),(d,e,f),(c,d,g),(c,e,g),(d,e,g),(d,f,g),(e,f,g),(a,c),(c,d),(a,e),(c,e),(d,e),(a,f),(d,f),(e,f),(c,g),(d,g),(e,g),(f,g)
removed: 8 (a),(b),(c),(d),(e),(f),(g),()
best score: 4
removal score: 1
------
subset: 7
combos: 23 (c,d,e,g),(d,e,f,g),(a,c,e,h),(a,e,f,h),(c,e,g,h),(e,f,g,h),(a,c,e),(c,d,e),(a,e,f),(d,e,f),(c,d,g),(c,e,g),(d,e,g),(d,f,g),(e,f,g),(a,c,h),(a,e,h),(c,e,h),(a,f,h),(e,f,h),(c,g,h),(e,g,h),(f,g,h)
removed: 12 (a,c),(c,d),(a,e),(c,e),(d,e),(a,f),(d,f),(e,f),(c,g),(d,g),(e,g),(f,g)
best score: 4
removal score: 2
------
subset: 8
combos: 8 (c,d,e,g),(d,e,f,g),(a,c,e,h),(a,e,f,h),(c,e,g,h),(e,f,g,h),(c,e,h,i),(e,f,h,i)
removed: 17 (a,c,e),(c,d,e),(a,e,f),(d,e,f),(c,d,g),(c,e,g),(d,e,g),(d,f,g),(e,f,g),(a,c,h),(a,e,h),(c,e,h),(a,f,h),(e,f,h),(c,g,h),(e,g,h),(f,g,h)
best score: 4
removal score: 3
------
subset: 9
combos: 8 (c,d,e,g),(d,e,f,g),(a,c,e,h),(a,e,f,h),(c,e,g,h),(e,f,g,h),(c,e,h,i),(e,f,h,i)
removed: 0
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
biggest subset size: 23
```