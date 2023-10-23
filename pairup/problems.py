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
        if curr in char_index_map and char_index_map[curr] >= start:
            start = char_index_map[curr] + 1
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


# def isValidBST(root: any) -> bool:
#     def isValidBounded(root, low, hi):
#         print(root.val, low, hi)
#         if root.val <= low or root.val >= hi:
#             return False
#         if root.left is None and root.right is None:
#             return True
#         if root.left is not None:
#             valid = isValidBounded(root.left, low, min(root.val, hi))
#             if not valid:
#                 return False
#         if root.right is not None:
#             valid = isValidBounded(root.right, max(root.val, low), hi)
#             if not valid:
#                 return False
#         return True

#     return isValidBounded(root, -float("inf"), float("inf"))


# Problems with solutions that are correct
Problems.reverse_linked_list = reverse_linked_list
Problems.longest_substring = longest_substring
Problems.max_area = max_area
Problems.combination_sum = combination_sum
Problems.num_islands = num_islands
Problems.check_bst = check_bst

# Problems with added bugs
Problems.max_area_d = max_area_d
Problems.combination_sum_d = combination_sum_d
