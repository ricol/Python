#!/usr/bin/env python
#-*- coding: utf-8 -*-

class Node:
    def __init__(self, data):

        self.left = None
        self.right = None
        self.data = data
# Insert Node

    def insert(self, data):

        if self.data:
            if data < self.data:
                if self.left is None:
                    self.left = Node(data)
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = Node(data)
                else:
                    self.right.insert(data)
        else:
            self.data = data

# Print the Tree

    def PrintTree(self):
        if self.left:
            self.left.PrintTree()
        print((self.data), end=' ')
        if self.right:
            self.right.PrintTree()

# Inorder traversal
# Left -> Root -> Right

    def inorderTraversal(self, root):
        res = []
        if root:
            res = self.inorderTraversal(root.left)
            res.append(root.data)
            res = res + self.inorderTraversal(root.right)
        return res

root = Node(27)
root.insert(14)
root.insert(35)
root.insert(10)
root.insert(19)
root.insert(31)
root.insert(42)
print((root.inorderTraversal(root)))

class Node:
    def __init__(self, data):

        self.left = None
        self.right = None
        self.data = data
# Insert Node

    def insert(self, data):

        if self.data:
            if data < self.data:
                if self.left is None:
                    self.left = Node(data)
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = Node(data)
                else:
                    self.right.insert(data)
        else:
            self.data = data

# Print the Tree

    def PrintTree(self):
        if self.left:
            self.left.PrintTree()
        print((self.data), end=' ')
        if self.right:
            self.right.PrintTree()

# Preorder traversal
# Root -> Left ->Right

    def PreorderTraversal(self, root):
        res = []
        if root:
            res.append(root.data)
            res = res + self.PreorderTraversal(root.left)
            res = res + self.PreorderTraversal(root.right)
        return res

root = Node(27)
root.insert(14)
root.insert(35)
root.insert(10)
root.insert(19)
root.insert(31)
root.insert(42)
print((root.PreorderTraversal(root)))

class Node:
    def __init__(self, data):

        self.left = None
        self.right = None
        self.data = data
# Insert Node

    def insert(self, data):

        if self.data:
            if data < self.data:
                if self.left is None:
                    self.left = Node(data)
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = Node(data)
                else:
                    self.right.insert(data)
        else:
            self.data = data

# Print the Tree

    def PrintTree(self):
        if self.left:
            self.left.PrintTree()
        print((self.data), end=' ')
        if self.right:
            self.right.PrintTree()

# Postorder traversal
# Left ->Right -> Root

    def PostorderTraversal(self, root):
        res = []
        if root:
            res = self.PostorderTraversal(root.left)
            res = res + self.PostorderTraversal(root.right)
            res.append(root.data)
        return res

root = Node(27)
root.insert(14)
root.insert(35)
root.insert(10)
root.insert(19)
root.insert(31)
root.insert(42)
print((root.PostorderTraversal(root)))