class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __str__(self):
        return f"Val:{self.val}"


if __name__ == "__main__":
    A = TreeNode(1)
    B = TreeNode(2)
    C = TreeNode(3)
    A.left = B
    A.right = C


    def dfs(root: TreeNode):
        if root is None: return
        print(root)
        dfs(root.left)
        dfs(root.right)

    dfs(A)