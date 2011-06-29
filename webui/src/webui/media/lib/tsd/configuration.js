var OpenTSDBURL="http://monitor2.cloud.pdl.cmu.local:4243";
var NumMapper=6;
var NumReducer=4;
var NumServers=64;
var ServerList=new Array();
for (var i = 1; i <= NumServers; ++i) {
	ServerList.push("cloud"+i);
}
