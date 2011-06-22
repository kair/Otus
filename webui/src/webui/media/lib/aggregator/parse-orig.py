import os, subprocess, time
from datetime import datetime
import urllib

class RateList:
  def __init__(self):
    self.list = []
    self.ptr = 0

  def append(self, time, val):
    self.list.append([time, val])

  def begin(self):
    self.ptr = 0

  def getRate(self, time):
    length = len(self.list)
    while (self.list[self.ptr][0] < time):
      if self.ptr+1 < length:
        self.ptr = self.ptr + 1
      else:
        return -1
    return self.list[self.ptr][1]

  def __len__(self):
    return len(self.list)

def plot_cdf_real(dir, name, cdfs):
  f = open(dir+name+"_ratio.plot", "w")
  f.write("set title 'I/O %s'\n"%(name))
  f.write("set terminal png size 500, 375 enhanced\n")
  f.write("set key right bottom\n")
  f.write("set ylabel 'Number of clients'\n")
  f.write("set xlabel 'I/O Thpt Ratio (Normailized by max thpt)\n")
  f.write("set output '%s'\n"%(name+"_ratio.png"))
  f.write("set yrange [0:48]\n")
  f.write("plot ")
  for i in range(0, len(cdfs)):
    if i > 0:
      f.write(",")
    f.write("'%s' using 3:2 title '%s' with linespoints"%(cdfs[i][0], cdfs[i][1]))
  f.close()
  os.chdir(dir)
  subprocess.call(['gnuplot', name+'_ratio.plot']) 
  os.chdir("../")
  f = open(dir+name+"_rate.plot", "w")
  f.write("set title 'I/O %s'\n"%(name))
  f.write("set terminal png size 500, 375 enhanced\n")
  f.write("set key right bottom\n")
  f.write("set ylabel 'Number of clients'\n")
  f.write("set xlabel 'I/O Throughput (MB/sec)\n")
  f.write("set output '%s'\n"%(name+"_rate.png"))
  f.write("set yrange [0:48]\n")
  f.write("plot ")
  for i in range(0, len(cdfs)):
    if i > 0:
      f.write(",")
    f.write("'%s' using 1:2 title '%s' with linespoints"%(cdfs[i][0], cdfs[i][1]))
  f.close()
  os.chdir(dir)
  subprocess.call(['gnuplot', name+'_rate.plot']) 
  os.chdir("../")


def plot_cdf(dir, name, data):
  global cdf_read, cdf_write
  f = open(dir+name, "w")
  data.sort()
#  data.reverse()
  for ti in range(0, len(data)):
    f.write("%.02f %d %.02f\n"%(data[ti], ti+1, data[ti]/data[len(data)-1]))
  f.close()
  rname = name[name.find('-')+1:].replace('_',' ')
  if name.find('read') > 0:
    cdf_read.append([name, rname])
  else:
    cdf_write.append([name, rname])

def plot_tm(dir, name, anslist):
  f = open(dir+name, "w")
  st = anslist[0][0]
  for ans in anslist:
    f.write("%ld, %.02f, %.02f, %.02f, %d\n"%((ans[0]-st)/1000, ans[1], ans[2], ans[3], ans[4]))
  f.close()
  rname = name[name.find('-')+1:].replace('_',' ')
  f = open(dir+name+".plot", "w")
  f.write("set terminal png size 500, 375 enhanced\n")
  f.write("set key right bottom\n")
  f.write("set title '%s'\n"%(rname))
  f.write("set xlabel 'Running time(sec)'\n")
  f.write("set ylabel 'I/O Throughput (MB/sec)\n")
  f.write("set y2label 'Number of clients\n")
  if rname.find('write') > 0:
    f.write("set yrange [0:100]\n")
  else:
    f.write("set yrange [0:200]\n")
  f.write("set y2range [0:48]\n")
  f.write("set y2tics 0, 5\n")
  f.write("set xtics nomirror\n")
  f.write("set ytics nomirror\n")
  f.write("set output '%s'\n"%(name+".png"))
  f.write("plot '%s' using 1:2 title 'avg' with line,"%(name))
  f.write("'%s' using 1:3 title 'min' with line,"%(name))
  f.write("'%s' using 1:4 title 'max' with line,"%(name))
  f.write("'%s' using 1:5 title 'clients' with line axis x1y2\n"%(name))
  f.close()
  os.chdir(dir)
  subprocess.call(['gnuplot', name+'.plot']) 
  os.chdir("../")

def plot_resource(dir, name, ll, rr):
  pairs = {}
  pairs['cs'] = datetime.fromtimestamp(ll/1000).strftime("%b %d %Y %H:%M")
  pairs['ce'] = datetime.fromtimestamp(rr/1000).strftime("%b %d %Y %H:%M")
  print name, pairs['cs'], pairs['ce']
  return
  pairs['z'] = 'large'
  pairs['t'] = 'customized'
  if name.find('gluster') > 0:
    pairs['hr']= '\\bstore[123456].opencloud\\b'
  else:
    pairs['hr']= '\\bstore[789].opencloud\\b|\\bstore1[123].opencloud\\b'
  pairs['lt']= 'stack'
  pairs['f'] = 'PDF'
  metrics=[['cpu_user|cpu_system|cpu_wio|cpu_nice', 'CPU Usage', 'cpu'],\
           ['bytes_in|bytes_out', 'Network Bandwidth (bytes/sec)', 'network'],\
           ['disk_bytes_read|disk_bytes_write', 'Disk Bandwidth (bytes/sec)', 'disk'],\
           ['disk_req_read|disk_req_write', 'Disk Requests (op/sec)', 'diskops'],\
           ['hadoop.Total.vmrss', 'Resident Memory (bytes)', 'rss']]
  for met in metrics:
    pairs['mr']= met[0]
    pairs['vl'] = met[1]
    if met[2]=='cpu' or met[2]=='rss':
      pairs['div']='6'
    else:
      pairs['div']='1' 
    params = urllib.urlencode(pairs)
    header='http://monitor2.cloud.pdl.cmu.local/storagenodes/graphs/graph.php?'
    url=header+params
    subprocess.call(['curl', url, '-o', dir+name+'_%s.pdf'%(met[2])])

def path_to_name(path):
  name = ""
  for i in range(0, len(path)):
    if path[i]==".":
      continue
    if path[i]=='/':
      if name != "":
        name+='-'
    else:
      name+=path[i]
  return name

results = ['result22']
outdir = "parse3/"
try:
  os.mkdir(outdir)
except:
  pass

cdf_read = []
cdf_write = []
summary = open(outdir+"summary.txt", "w")
for res in results:
  path = './%s'%(res)
  reslist = os.listdir(path)
  for fname in reslist:
    path1 = '%s/%s'%(path, fname)
    syslist = os.listdir(path1)
    for sys in syslist:
      path2 = '%s/%s'%(path1, sys)
      testlist = os.listdir(path2)
      lines = []
      thpt = []
      avg = 0
      tot = 0
      cnt = 0
      ll = 2000000000000
      lr = 0
      rl = 2000000000000
      rr = 0
      rates = []
      for test in testlist:
        if test.endswith(".log") and test.startswith("cloud"):
          cnt += 1
          path3 = '%s/%s'%(path2, test)
          f = open(path3, "r")
          line = f.readline()
          lines.append(line)
          items = line.split()
          thpt.append(float(items[1]))
          tot += float(items[2])
          time = int(items[4])
          ll = min(ll, time)
          lr = max(lr, time)
          time = int(items[5])
          rl = min(rl, time)
          rr = max(rr, time)
          rate = RateList()
          while (1):
            line = f.readline()
            if line == "":
              break
            if line == "rate\n":
              continue
            if line == "measurement\n":
              break
            items = line.split()
            rate.append(float(items[0]), float(items[1]))
          rates.append(rate)
          f.close()
      step = (rr-ll)/200
      start = ll
      anslist = []
      while start < rr:
        ravg = 0
        rtot = 0
        rcnt = 0
        rmin = 1e20
        rmax = 0
        for rate in rates:
          r = rate.getRate(start)*1000/1024/1024
          if r < 0:
            continue
          rcnt += 1
          rtot += r
          if r < rmin:
            rmin = r
          if r > rmax:
            rmax = r
        if rcnt <= 0:
          break
        ravg = float(rtot) / rcnt
        anslist.append([start, ravg, rmin, rmax, rcnt])
        start += step
      avg = float(tot) / float(rr - ll) / 1000;
      name = path_to_name(path2)
      summary.write("%s-%s, "%(fname, sys))
      summary.write("%.02f, %d, %ld, %ld, %ld, %ld, %ld\n"%(avg, cnt, tot, ll, lr, rl, rr))
      plot_cdf(outdir, name+"-cdf", thpt)
      plot_tm(outdir, name+"-tm", anslist)
      plot_resource(outdir, name, ll, rr) 

summary.close()
plot_cdf_real(outdir, "read", cdf_read)
plot_cdf_real(outdir, "write", cdf_write)
