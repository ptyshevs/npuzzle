import bisect

class PriorityQueue(list):
    def __init__(self):
        self.v = []
        self.k = []
    
    def add(self, key, value):
        i = bisect.bisect_right(self.k, key)
        self.v.insert(i, value)
        self.k.insert(i, key)
    
    def pop(self):
        item = self.v.pop(0)
        key = self.k.pop(0)
        return item
    
    def __len__(self):
        return len(self.v)
    
if __name__ == '__main__':
    q = PriorityQueue()
    q.add(3, 'a')
    q.add(4, 'b')
    q.add(1, 'c')
    print(q.v)
    print(q.pop())
    print(q.pop())
    print(q.pop())