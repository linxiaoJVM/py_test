'''
Created on 2014-8-28

@author: lin
'''

def fab(max):
    n,a,b = 0,0,1
    while(n < max):
        print b
        a,b = b,a+b
        n = n+1
def fab_1(max):
    n,a,b = 0,0,1
    l = []
    while(n < max):
        l.append(b)
        a,b = b, a+b
        n = n +1
    return l    

def fab_2(max):
    n,a,b = 0,0,1
    while(n < max):
        yield b
        a, b = b, a + b
        n = n + 1
    
    
      
class Fab(object):
    '''
    classdocs
    '''


    def __init__(self, max):
        '''
        Constructor
        '''
        self.max = max
        self.n,self.a, self.b = 0,0,1
    def __iter__(self):
        return self
    def next(self):
        while(self.n < self.max):
            r = self.b
            self.a,self.b = self.b, self.a+self.b
            self.n = self.n + 1
            return r
        raise StopIteration()
    
if __name__ == '__main__':
    #fab(5)3问2
    #print fab_1(5)
    f = fab_2(5)
    print f.next()
#     fab = Fab(5)
#     print fab.next()
