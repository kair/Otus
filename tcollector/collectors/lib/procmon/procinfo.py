import sys
from constant import *

def getCmdLine(pid):
  try:
    f = open(PATH.PROCPID_CMDLINE%(pid), 'r');
    lines = f.readlines()
    f.close()
    ret = ''.join(lines)
  except:
    return ''
  return ret

def getPPidAndUid(pid):
  try:
    f = open(PATH.PROCPID_STATUS%(pid), 'r');
    lines = f.readlines();
    f.close()
  except Exception, e:
    sys.stderr.write(str(e))
    return (None, None)
  ppid = 1
  uid = 0
  for line in lines:
    items = line.split()
    if items[0].startswith("PPid"):
      ppid = int(items[1])
    if items[0].startswith("Uid"):
      uid = int(items[1])
  return (ppid, uid)

class ProcInfoStat:
  SIZE = 4 #1
  INDEX = [13, 14]

  def __init__(self):
    try:
      f = open("/proc/stat", "r")
      self.numP = 0
      for l in f:
        if l.startswith("cpu"):
          self.numP += 1
      if self.numP > 1:
        self.numP -= 1
    except:
      self.numP = 0

  def size(self):
    return ProcInfoStat.SIZE

  def naming(self):
    return ["cpu_user_time", "cpu_system_time", "cpu_user", "cpu_system"]
#    return ["cpu_usage"]

  def names(self):
    return [ "procmon.CPUTime", "procmon.CPUTime", "procmon.CPU", "procmon.CPU"]
#    return ["procmon.CPU"]

  def types(self):
    return ["type=user", "type=system", "type=user", "type=system"]
#    return [""]

  def update(self, pid, met, intv):
    try:
      f = open(PATH.PROCPID_STAT%(pid), 'r');
      line = f.readline()
      f.close()
    except Exception, e:
      sys.stderr.write(str(e))
      return
    items = line.split()
#    met[0] = (float(items[13])+float(items[14])) / self.numP
    i = 0
    for ind in ProcInfoStat.INDEX:
      newmet = float(items[ind]) / self.numP
      if met[i] >= 0:
        met[i+2] = (newmet - met[i]) / intv
      else:
        met[i+2] = 0
      met[i] = newmet
      i += 1

class ProcInfoIO:
  SIZE = 6

  def size(self):
    return ProcInfoIO.SIZE

  def naming(self):
    return ["readbytes", "writebytes", "canwritebytes", \
            "readbytesrate", "writebytesrate", "canwritebytesrate"]

  def names(self):
    return ['procmon.DiskRead', 'procmon.DiskWrite', 'procmon.DiskCancelWrite',\
            'procmon.DiskReadRate', 'procmon.DiskWriteRate', 'procmon.DiskCancelWriteRate'] 

  def types(self):
    return ['','','','','','']

  def update(self, pid, met, intv):
    try:
      f = open(PATH.PROCPID_IO%(pid), 'r');
      lines = f.readlines();
      f.close()
    except Exception, e:
      sys.stderr.write(str(e))
      return 
    for i in range(3):
      newmet = float(lines[4+i].split()[1])
      if met[i] >= 0:
        met[i+3] = (newmet - met[i]) / intv
      else:
        met[i+3] = 0
      met[i] = newmet

class ProcInfoStatus:
  SIZE = 2

  def size(self):
    return ProcInfoStatus.SIZE

  def naming(self):
    return ["vmsize", "vmrss"]

  def names(self):
    return ['procmon.VirtualMem', 'procmon.ResidentMem']

  def types(self):
    return ['', '']

  def update(self, pid, met, intv):
    try:
      f = open(PATH.PROCPID_STATUS%(pid), 'r');
      lines = f.readlines();
      f.close()
    except Exception, e:
      sys.stderr.write(str(e))
      return
    for line in lines:
      items = line.split()
      if items[0].startswith("VmSize"):
        met[0] = long(items[1]) * 1024
      if items[0].startswith("VmRSS"):
        met[1] = long(items[1]) * 1024

def test(module, pid, ans):
  assert module.size() == len(module.naming())
  assert module.size() == len(module.names())
  assert module.size() == len(module.types())
  met = [0] * module.size()
  module.update(pid, met)
  for i in range(0, len(met)):
    if ans[i] != met[i]:
      print "wrong"
  print module.names()
  print module.types()
  print met

if __name__ == '__main__':
  PATH.PROCPID_CMDLINE='./test/proc1/%d/cmdline'
  PATH.PROCPID_STATUS='./test/proc1/%d/status'
  PATH.PROCPID_STAT='./test/proc1/%d/stat'
  PATH.PROCPID_IO='./test/proc1/%d/io'

  assert getCmdLine(1) == "/sbin/init"
  (ppid, uid) = getPPidAndUid(1)
  assert ppid == 0
  assert uid == 0
  test(ProcInfoStat(), 1, [(16+244)/4])
  test(ProcInfoStatus(), 1, [2812*1024, 1680*1024])
  test(ProcInfoIO(), 1, [743696896, 2420928512, 181018624])
