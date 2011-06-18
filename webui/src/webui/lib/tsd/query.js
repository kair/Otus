/** 
*  Query to OpenTSDB to generate visual reports for Otus
*
*  Kai Ren (kair@cs.cmu.edu) 
*
**/

function genMetricQuery(metric, tags, conf) {
	var query = "m=" + conf.aggfunc;
	if (conf.downSample != "") {
		query += ":"+conf.downSample;
	}
	if (conf.isRate) {
		query += ":rate";
	}
	query += ":"+metric;
	first = true;
	for tagName in tags {
		if (first) {
			query += "{";
			first = false;
		}
		query += tagName + "=" + tags[tagName];
	}
	if (!first) {
		query += "}";
	}
	return query;
}

function procClusterView(metric, procname, conf) {
	return genMetricQuery("procmon."+metric, {proc: procname}, conf);
}

function totClusterView(metric, conf) {
	return genMetricQuery("procmon."+metric, {proc: "Node.Total"}, conf);
}

function jobClusterView(metric, _jobid, conf) {
	return genMetricQuery("mrjob."+metric, {jobid: _jobid}, conf);
}

function jobTotalClusterView(metric, conf) {
	return genMetricQuery("mrjob."+metric, {}, conf);
}

function procNodeView(metric, procname, hostid, conf) {
	return genMetricQuery("procmon."+metric, {proc: procname, host:hostid}, conf);
}

function totClusterView(metric, hostid, conf) {
	return genMetricQuery("procmon."+metric, {proc: "Node.Total", host:hostid}, conf);
}

function jobNodeView(metric, hostid, typevalue, conf) {
	return genMetricQuery("procmon."+metric, {jobid: _jobid, host:hostid, tasktype: typevalue}, conf);
}

function getOpenTSDBURL() {
	return "http://localhost:4242";
}

function genQuery(startTime, endTime, metricQueries, callback) {
	query = getOpenTSDBURL()+"/q?start="+startTime+"&end="+endTime+"&ascii&injson";
	for (var i = 0; i < metricQueries.length; ++i) {
		query += "&"+metricQueries[i];
	}
	return encodeURI(query+"&callback=?");
}

function getClusterView(startTime, endTime, conf) {
	var queries = new Array();
	queries.push(jobClusterView(conf.metric, conf));
	for (var i = 0; i < proclist.length; ++i) {
		queries.push(procClusterView(conf.metric, conf.proclist[i], conf));
	}
	for (var i = 0; i < joblist.length; ++i) {
		queries.push(jobClusterView(conf.metric, conf.joblist[i], conf));
	}
	return genQuery(startTime, endTime, queries);
}

function renderView(startTime, endTime, genViewFun, conf, plotdiv) {
	var uri = genViewFunc(startTime, endTime, conf);
	$.getJSON(uri, function(data) {
        $.plot($(plotdiv), [ data["data"], {
            series: {
            stack: false,
            lines: { show: true, fill: true, steps: false},
          },
          xaxis: { mode: "time"}
        })
    });
}
