# Definition for a binary tree node.
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution(object):
    def isBalanced(self, root):
        return (self.Height(root) >= 0)

    def Height(self, root):
        if root is None:
            return 0
        leftheight = self.Height(root.left)
        rightheight = self.Height(root.right)
        if abs(leftheight - rightheight) > 1:
            return -1
        return max(leftheight, rightheight) + 1


sol = Solution()
sol.isBalanced(TreeNode(1, TreeNode(2, TreeNode(10, TreeNode(11, None, None)), TreeNode(5, None, None)), None))
