import json

class RateList:
    def __init__(self):
        self._list = []
        self.ptr = 0

    def append(self, time, val):
        self._list.append([time, val])

    def extend(self, series):
        self._list.extend(series)

    def begin(self):
        self.ptr = 0

    def getRate(self, time):
        length = len(self._list)
        while (self._list[self.ptr][0] < time):
            if self.ptr+1 < length:
                self.ptr = self.ptr + 1
            else:
                return -1
        return self._list[self.ptr][1]

    def __len__(self):
        return len(self._list)

def loadFile(fn):
    f = open(fn, "r")
    content = ""
    for l in f:
        content += l
    f.close()
    series = json.loads(content)
    ratelists = []
    for s in series:
        ratel = RateList()
        ratel.extend(s["data"])
        ratelists.append(ratel)
    return ratelists

def findStart(ratelists):
  startTime = 0
  for rl in ratelists:
    startTime = max(rl._list[0][0],startTime)
  return startTime

def findEnd(ratelists):
  endTime = 1e30
  for rl in ratelists:
    endTime = min(rl._list[len(rl._list)-1][0],endTime)
  return endTime

def aggregate(ratelists, step):
  startTime = findStart(ratelists)
  endTime = findEnd(ratelists)
  t = startTime
  for rl in ratelists:
    rl.begin()
  anslist = []
  old = 0
  while t < endTime:
    tot = 0
    for rl in ratelists:
      tot += rl.getRate(t)
    if tot != old: 
      anslist.append([t, tot])
      old = tot
    t += step
  return anslist

def amplifyTime(anslist):
  for pair in anslist:
    pair[0] = pair[0] * 1000

def dumpFile(fn, anslist):
  f = open(fn, "w")
  f.write("data=")
  f.write(json.dumps(anslist))
  f.close()

ratelists = loadFile("./test.json")
anslist = aggregate(ratelists, 10)
amplifyTime(anslist)
dumpFile("./result.json", anslist)
