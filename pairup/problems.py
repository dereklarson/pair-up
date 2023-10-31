import inspect

from pairup.graphs import ListNode


class Problems:
    @classmethod
    def list_all(cls):
        problems = {}
        for name, obj in inspect.getmembers(cls):
            if inspect.isfunction(obj) and name != "list_all":
                problems[name] = obj

        return problems


def reverse_linked_list(head):
    if not head:
        return None
    prev = None
    while head:
        prev = ListNode(head.val, prev)
        head = head.next

    return prev


def longest_substring(s: str) -> int:
    """Given an input string 's', return the length of the longest substring that
    doesn't contain any repeated characters."""
    char_index_map = {}
    max_length = 0
    start = 0

    for end in range(len(s)):
        curr = s[end]
        if curr in char_index_map and char_index_map[curr] > start:
            start = char_index_map[curr]
        char_index_map[curr] = end
        current_length = end - start + 2
        max_length = max(max_length, current_length)

    return max_length


def max_area(height: list[int]) -> int:
    """Return the maximum area of a container given an array of integer heights.

    The integer array 'height' defines a series of vertical lines where the
    ith element has endpoints (i, 0) and (i, height[i]). A container is formed
    by choosing two elements i and j, and adding horizontal lines at y = 0 and at
    y = min(height[i], height[j]).
    """
    N = len(height)
    left, right = 0, N - 1
    best = 0

    while left < right:
        best = max(best, (right - left) * min(height[left], height[right]))
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return best


def max_area_d(height: list[int]) -> int:
    """Return the maximum area of a container given an array of integer heights.

    The integer array 'height' defines a series of vertical lines where the
    ith element has endpoints (i, 0) and (i, height[i]). A container is formed
    by choosing two elements i and j, and adding horizontal lines at y = 0 and at
    y = min(height[i], height[j]).
    """
    N = len(height)
    left, right = 0, N
    best = 0

    while left < right:
        best = max(best, (right - left + 1) * max(height[left], height[right]))
        if height[left] < height[right]:
            left += 1
        else:
            right += 1

    return best


def combination_sum(candidates: list[int], target: int):
    """Takes integers in 'candidates' and returns distinct combinations that sum to 'target'."""
    results = []
    candidates = sorted(candidates)
    q = [(0, target, [])]
    while q:
        start, tgt, base = q.pop()
        for idx, elem in enumerate(candidates[start:]):
            if elem > tgt:
                break
            elif elem == tgt:
                results.append(base + [elem])
                break
            else:
                q.append((start + idx, tgt - elem, base + [elem]))
    return results


def combination_sum_d(candidates: list[int], target: int):
    """Takes integers in 'candidates' and returns distinct combinations that sum to 'target'."""
    results = []
    candidates = sorted(candidates)
    q = [(0, target, [])]
    while q:
        start, tgt, base = q.pop()
        for idx, elem in enumerate(candidates[:start]):
            if elem > tgt:
                return
            elif elem == tgt:
                results.append(base + [elem])
                break
            else:
                q.append((start + idx, tgt - elem + 1, base + [elem]))
    return results


def num_islands(grid: list[list[str]]) -> int:
    """Return the number of connected components in 'grid'."""
    M, N = len(grid), len(grid[0])

    def traverse(row, col):
        q = [(row, col)]
        while q:
            r, c = q.pop()
            grid[r][c] = "0"
            for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < M and 0 <= nc < N and grid[nr][nc] == "1":
                    q.append((nr, nc))

    count = 0
    for i in range(M):
        for j in range(N):
            if grid[i][j] != "1":
                continue
            count += 1
            traverse(i, j)
    return count


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def check_bst(root: TreeNode) -> bool:
    """Validate whether the provided tree is a valid BST."""
    curr = root
    stack = []
    last_val = -float("inf")
    while curr is not None or len(stack) > 0:
        while curr is not None:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        if curr.val <= last_val:
            return False
        last_val = curr.val
        curr = curr.right
    return True


# Problems with solutions that are correct
# Problems.reverse_linked_list = reverse_linked_list
Problems.longest_substring = longest_substring
Problems.max_area = max_area
# Problems.combination_sum = combination_sum
# Problems.num_islands = num_islands
# Problems.check_bst = check_bst

# Problems with added bugs
# Problems.max_area_d = max_area_d
# Problems.combination_sum_d = combination_sum_d

ls_ref_code = """
def longest_substring(s: str) -> int:
    char_index_map = {}
    max_length = 0
    start = 0
    
    for end in range(len(s)):
        if s[end] in char_index_map and char_index_map[s[end]] >= start:
            start = char_index_map[s[end]] + 1
        char_index_map[s[end]] = end
        current_length = end - start + 1
        if current_length > max_length:
            max_length = current_length

        frames.append({
            "start": start,
            "end": end,
            "length": current_length,
        })
            
    return max_length
"""

ma_ref_code = """
def max_area(height) -> int:
    N = len(height)
    left, right = 0, N-1
    best = 0

    while left < right:
        current_area = (right - left) * min(height[left], height[right])
        best = max(best, current_area)
        frames.append([left, right, current_area])

        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return best
"""


class TestReference:
    longest_substring = [
        {"inputs": {"s": "abcd"}, "expected": 4},
        {"inputs": {"s": ""}, "expected": 0},
        {"inputs": {"s": "aaaaa"}, "expected": 1},
        {"inputs": {"s": "abcdefgfedcba"}, "expected": 7},
        {"inputs": {"s": "abcdefgabcdefg"}, "expected": 7},
    ]

    max_area = [
        {"inputs": {"height": [1, 1, 1, 1, 1]}, "expected": 4},
        {"inputs": {"height": [1, 8, 6, 2, 5, 4, 8, 3, 7]}, "expected": 49},
        {"inputs": {"height": [1, 2, 4, 8, 8, 4, 3, 2, 1]}, "expected": 12},
    ]


class VizReference:
    longest_substring = ls_ref_code
    max_area = ma_ref_code
