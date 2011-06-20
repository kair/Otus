/** 
*  Query to OpenTSDB to generate visual reports for Otus
*
*  Kai Ren (kair@cs.cmu.edu) 
*
**/

function genMetricQuery(metric, tags, conf) {
	var query = "m=" + conf.aggfunc;
	if (conf.downSample != null) {
		query += ":"+conf.downSample;
	}
	if (conf.isRate) {
		query += ":rate";
	}
	query += ":"+metric;
	first = true;
	for (tagName in tags) {
		if (first) {
			query += "{";
			first = false;
		} else {
			query += ",";
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

function procNodeView(metric, hostid, procname, conf) {
	return genMetricQuery("procmon."+metric, {proc: procname, host:hostid}, conf);
}

function totNodeView(metric, hostid, conf) {
	return genMetricQuery("procmon."+metric, {proc: "Node.Total", host:hostid}, conf);
}

function jobNodeView(metric, hostid, _jobid, conf) {
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
	//return encodeURI(query+"&callback=?");
	return query+"&callback=?";
}

function getClusterView(startTime, endTime, conf) {
	var queries = new Array();
	queries.push(totClusterView(conf.metric, conf));
	for (var i = 0; i < conf.proclist.length; ++i) {
		queries.push(procClusterView(conf.metric, conf.proclist[i], conf));
	}
	for (var i = 0; i < conf.joblist.length; ++i) {
		queries.push(jobClusterView(conf.metric, conf.joblist[i], conf));
	}
	return genQuery(startTime, endTime, queries);
}

function getNodeView(startTime, endTime, conf) {
	var queries = new Array();
	queries.push(totNodeView(conf.metric, conf.hostid, conf));
	for (var i = 0; i < conf.proclist.length; ++i) {
		queries.push(procNodeView(conf.metric, conf.hostid, conf.proclist[i], conf));
	}
	for (var i = 0; i < conf.joblist.length; ++i) {
		queries.push(jobNodeView(conf.metric, conf.hostid, conf.joblist[i], conf));
	}
	return genQuery(startTime, endTime, queries);
}

function renderView(startTime, endTime, genViewFun, conf, plotdiv) {
	var uri = genViewFun(startTime, endTime, conf);
	$.getJSON(uri, function(data) {
        $.plot($(plotdiv), [ data[0]['data'], data[1]['data'] , data[2]['data'],
                data[3]['data'] ], {
            series: {
            stack: false,
            lines: { show: true, fill: true, steps: false},
          },
          xaxis: { mode: "time"}
        })
    });
}
