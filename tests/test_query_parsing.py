from pairup.parsing import match_func_call

review_input_1 = """
Here's the corrected code:

def combination_sum_d(candidates: list[int], target: int):
    \"\"\"Takes integers in 'candidates' and returns distinct combinations that sum to 'target'.\"\"\"
    results = []
    candidates = sorted(candidates)
    q = [(0, target, [])]
    while q:
        start, tgt, base = q.pop()
        for idx, elem in enumerate(candidates[start:], start):
            if elem > tgt:
                break
            elif elem == tgt:
                results.append(base + [elem])
                break
            else:
                q.append((start + idx + 1, tgt - elem, base + [elem]))
    return results

I made the following changes:

1. In the for loop, I changed the candidates slicing to candidates[start:] instead of candidates[:start]. This ensures that we iterate over the correct subset of candidates.

2. In the else block of the for loop, I changed tgt - elem + 1 to tgt - elem. Adding 1 would result in incorrect combinations as it overshoots the target.

3. In the q.append() line inside the else block, I changed start + idx to start + idx + 1. This ensures that we correctly move the start index forward for the next iteration.

With these corrections, the code should now return the correct distinct combinations that sum to the target.
"""

review_output_1 = """
def combination_sum_d(candidates: list[int], target: int):
    \"\"\"Takes integers in 'candidates' and returns distinct combinations that sum to 'target'.\"\"\"
    results = []
    candidates = sorted(candidates)
    q = [(0, target, [])]
    while q:
        start, tgt, base = q.pop()
        for idx, elem in enumerate(candidates[start:], start):
            if elem > tgt:
                break
            elif elem == tgt:
                results.append(base + [elem])
                break
            else:
                q.append((start + idx + 1, tgt - elem, base + [elem]))
    return results
""".strip()

review_input_2 = """
There is a bug in the while loop condition. The condition should be `left < right - 1` instead of `left < right` to avoid an off by one error.

Here's the corrected code:

```python
def max_area_d(height: list[int]) -> int:
    \"\"\"Return the maximum area of a container given an array of integer heights.

    The integer array 'height' defines a series of vertical lines where the
    ith element has endpoints (i, 0) and (i, height[i]). A container is formed
    by choosing two elements i and j, and adding horizontal lines at y = 0 and at
    y = min(height[i], height[j]).
    \"\"\"
    N = len(height)
    left, right = 0, N - 1
    best = 0

    while left < right - 1:
        best = max(best, (right - left + 1) * min(height[left], height[right]))
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return best
```

Note: I also corrected the calculation of the container area. It should be `(right - left + 1) * min(height[left], height[right])` instead of `(right - left + 1) * max(height[left], height[right])`.
"""

review_output_2 = """
def max_area_d(height: list[int]) -> int:
    \"\"\"Return the maximum area of a container given an array of integer heights.

    The integer array 'height' defines a series of vertical lines where the
    ith element has endpoints (i, 0) and (i, height[i]). A container is formed
    by choosing two elements i and j, and adding horizontal lines at y = 0 and at
    y = min(height[i], height[j]).
    \"\"\"
    N = len(height)
    left, right = 0, N - 1
    best = 0

    while left < right - 1:
        best = max(best, (right - left + 1) * min(height[left], height[right]))
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return best
""".strip()


def test_review_parsing():
    assert match_func_call(review_input_1) == review_output_1
    assert match_func_call(review_input_2) == review_output_2
