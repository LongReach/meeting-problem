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
