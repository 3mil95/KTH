import array

class ArrayQ:
    def __init__(self, inputArray=array.array('i')):
        self.__queue = inputArray

    def enqueue(self, x):
        """"adds x to the queue"""
        self.__queue.append(x)

    def dequeue(self):
        """takes the last element in the queue and
        removes it and returns the value"""
        return self.__queue.pop(0)

    def isEmpty(self):
        """Check if the queue is empty"""
        empty = False
        if len(self.__queue) == 0:
            empty = True
        return empty


def testArraQ():
    q = ArrayQ()
    q.enqueue(1)
    q.enqueue(2)
    x = q.dequeue()
    y = q.dequeue()
    if (x == 1 and y == 2):
        print("Fungerar")
    else:
        print("Något är fel. 1 och 2 förväntades men vi fick", x, y)


if __name__ == '__main__':
    testArraQ()