var SuggestURL="http://localhost:4242/suggest?";
//var QueryURL="http://monitor.cloud.pdl.cmu.local:4242/q?";
var QueryURL="http://kmonitor:4243/q?";
var NumMapper=6;
var NumReducer=4;
var NumServers=64;
var MetricList = ["cpu_user", "cpu_system", "vmrss", "vmsize", "readbytesrate", "writebytesrate"];
var ProcessList = ["DataNode", "TaskTracker"];
var MetricYLabel = {cpu_user:"User CPU", cpu_system:"System CPU", vmrss:"Resident Memory (Bytes)",
					vmsize:"Virtual Memory (Bytes)", readbytesrate:"Disk I/O Read Throughput (Bytes)",
					writebytesrate:"Disk I/O Write Throughput (Bytes)"};
var ServerList=new Array();
for (var i = 1; i <= NumServers; ++i) {
	ServerList.push("cloud"+i);
}
