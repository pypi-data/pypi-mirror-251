# spaceAndTime

This package was created to evalute functions for time and space complexity. At the moment only time complexity is complete. The function runs an algorithmn over and over with new
and increasing input sizes to judge the time complexity.

## Example

```python

def testone(n):
    for x in range(len(n[0])):
        for y in range(len(n[0])):
            two = y
            one = x

real = RealTime()

testSet = real.generateTestSet(type=0)

real.complexGuess(testone,testSet)

```

![Figure_1](https://github.com/hodge-py/RealTime_Analysis/assets/105604814/fef612f2-ff1b-411a-b9b1-7d9ae8cd0af2)

![Screenshot 2024-01-15 020628](https://github.com/hodge-py/RealTime_Analysis/assets/105604814/b0b113f5-466d-4d21-9551-d3fd17e8a9bf)
