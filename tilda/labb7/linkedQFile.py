class Node:
    def __init__(self, data=None):
        self.data = data
        self.nextNode = None

class LinkedQ:
    def __init__(self):
        self._first = None
        self._last = None

    def enqueue(self, x):
        """"adds x to the queue"""
        if self._first == None:
            self._first = Node(x)
            self._last = self._first
        else:
            self._last.nextNode = Node(x)
            self._last = self._last.nextNode

    def dequeue(self):
        """takes the last element in the queue and
        removes it and returns the value"""
        data = None
        if self._first != None:
            data = self._first.data
            self._first = self._first.nextNode
        return data

    def isEmpty(self):
        """Check if the queue is empty"""
        empty = False
        if self._first == None:
            empty = True
        return empty

    def printQueue(self):
        """prints the queue"""
        thisNode = self._first
        print(thisNode.data)
        while thisNode.nextNode != None:
            thisNode = thisNode.nextNode
            print(thisNode.data, ',')


if __name__ == '__main__':
    # test LinkedQ class
    q = LinkedQ()
    q.enqueue(9)
    q.enqueue(5)
    print(q.dequeue())
    print(q.dequeue())
    print(q.dequeue(), '\n')
    q.enqueue(1)
    q.printQueue()
