from binaryTree import TreeNode


def bfs(root: TreeNode) -> None:
    q = [root]
    while q:
        temp = []
        for node in q:
            print(node.val)
            if node.left:
                temp.append(node.left)
            if node.right:
                temp.append(node.right)
        q = temp
