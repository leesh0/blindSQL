import threading
import time
import sys
import requests as req
class ezt:
    def __init__(self):
        self.threads = []
    
    def new(self,f,args=()):    # add new cycle
        t = threading.Thread(target=f,args=args)
        self.threads.append(t)
        return t
    
    def recycle(self,f,args=()):    # reuse cycle
        while len(self.termed()) < 1:
            time.sleep(0.1)
        index = self.termed()[0]
        t = self.threads[index] = threading.Thread(target=f,args=args)
        return t

    def termed(self):       #return terminated thread No.
        return [i for i,t in enumerate(self.threads) if not t.is_alive()]


class blind_SQL:
    def __init__(self, f, charlist, targetLength):
        self.fx = f
        self.cSet = charlist
        self.tLen = targetLength
        self.flag = ["?" for x in range(targetLength)]
        self.run()
    

    def run(self):
        t = ezt()
        tlist = []
        for i in range(1,self.tLen+1):
            r = t.new(self.fuzz, args=(i,))
            tlist.append(r)
            r.start()
        while True:
            for t in tlist:
                if t.is_alive():
                    val = False
                    break
                else: val = True
            sys.stdout.write("\r"+"".join(self.flag))
            time.sleep(0.1)
            if val: break
    
    def fuzz(self,i):
        for c in self.cSet:
            if self.fx(i,c):
                self.flag[i-1] = c
                break

 
req = req.Session()




#USAGE
def bex(i,c):       #must have 2args (i = position, c = charset[n])
    res = req.get("http://blog.leesh0.kr")
    if c =="a": return True         #if
    return False

cset = [chr(i) for i in range(90,100)]
o = blind_SQL(bex,cset,100)
print("\n------------------------\n",o.flag)

#OUTPUT
"""
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
------------------------
 ['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a']
"""