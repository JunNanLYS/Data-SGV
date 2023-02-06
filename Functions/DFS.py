from binaryTree import TreeNode


def preorder_traversal(root: TreeNode) -> None:
    if root is None: return
    print(root.val)
    preorder_traversal(root.left)
    preorder_traversal(root.right)


def inorder_traversal(root: TreeNode) -> None:
    if root is None: return
    inorder_traversal(root.left)
    print(root.val)
    inorder_traversal(root.right)


def postorder_traversal(root: TreeNode) -> None:
    if root is None: return
    postorder_traversal(root.left)
    postorder_traversal(root.right)
    print(root.val)
