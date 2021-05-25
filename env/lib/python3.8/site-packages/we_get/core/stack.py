"""
Copyright (c) 2017 Levi Sabah <x@levisabah.com> (https://github.com/levisabah/we-get/)
See the file 'LICENSE' for copying.
"""

class Stack(object):
    """Simple stack implementation for self.items
        the stack works as dict() for example:
       
       STACK
       ---- 
       { UPPER
         'ITEM 1' : 1,
         'ITEM 2' : 1,
         ...
       } LOWER
    """
    def __init__(self, items):
        self.items = items

    def push(self, item):
        """Push new item to the stack"""
        self.items.update(item)

    def pop(self):
        """Pop item from the stack"""
        return self.items.popitem()
    
    def len(self):
        """Return the number of items in the stack"""
        return self.items.__len__()

    def isex(self, item):
        """Check if item is in the stack"""
        return self.items.__contains__(item)

    def is_empty(self):
        """Check if the stack if empty"""
        return self.len() == 0

