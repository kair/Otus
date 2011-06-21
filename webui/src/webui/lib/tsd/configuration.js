var SuggestURL="http://localhost:4242/suggest?";
var QueryURL="http://monitor:4242/q?";
//var QueryURL="http://localhost:4242/q?";
var NumMapper=6;
var NumReducer=4;
var NumServers=64;
var ServerList=new Array();
for (var i = 1; i <= NumServers; ++i) {
	ServerList.push("cloud"+i);
}
