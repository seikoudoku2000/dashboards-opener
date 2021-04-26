# dashboards-opener

`dashboards-opener` is a simple script to open list of dashboard urls with given timestamp.


## REQUIREMENT
- Python 3.6.x


## HOW TO USE

```
$ python dashboards-opener.py -h
usage: dashboards-opener.py [-h] [--duration DURATION] [--file FILE] timestamp

This script will open dashboards in the list with the timestamp passed as
parameter

positional arguments:
  timestamp            central timestamp you want to check in milliseconds
                       epoch format.

optional arguments:
  -h, --help           show this help message and exit
  --duration DURATION  time range you want to check before and after the
                       central timestamp(minute). default: 30
  --file FILE          csv file where dashboard urls are defined. default:
                       base_urls.csv
```


### Prepare a csv file with dashboard urls

- first line is treated as header
- lines starting with '#' are treated as comment and ignored in execution.
- `START_TIMESTAMP` AND `END_TIMESTAMP` are replaced with the actual timestamp in execution.
- Opening actual dashboards manually, get actual URLs, and replace the timestamp parts would be an easy way to prepare a csv file.


```csv
base_url
# datadog example
https://app.datadoghq.com/dashboard/aaa-bbb-ccc/abcdefg?live=false&from_ts=START_TIMESTAMP&to_ts=END_TIMESTAMP
# new relic example
https://one.newrelic.com/launcher/nr1-core.explorer?XXXXXXXXXXXXXXXXXXXXXXXXXXXXX&platform[timeRange][begin_time]=START_TIMESTAMP&platform[timeRange][end_time]=END_TIMESTAMP
# AWS RDS database insight
https://ap-northeast-1.console.aws.amazon.com/rds/home?region=ap-northeast-1#performance-insights-v20206:/resourceId/db-ABCDEFG/resourceName/test-database/startTime/START_TIMESTAMP/endTime/END_TIMESTAMP
```

### Run                       
```
# run with default setting
$ python dashboards-opener.py 1619416322931

# 30 minutes time range
$ python dashboards-opener.py 1619416322931 --duration 30
```


## Using with Datadog monitoring
If you're using [datadog](https://www.datadoghq.com/) for monitoring, by including `{{last_triggered_at_epoch}}` in datadog monitor's MESSAGE part, you can get the timestamp to pass each time an incident is triggered.  

[https://docs.datadoghq.com/monitors/guide/template-variable-evaluation/](https://docs.datadoghq.com/monitors/guide/template-variable-evaluation/)

> The {{last_triggered_at_epoch}} template variable returns the UTC time when a monitor last triggered in milliseconds epoch format.  


So, for example, if you set a message like this in a monitoring and prepare a csv file which contains related dashboard urls beforehand, 

```
Check dashboards opend below commands. 

$ python dashboards-opener.py {{last_triggered_at_epoch}} --file related_dashboard_urls.csv

```

then on-call person, even if he/she is a newbie, can open dashboards in seconds and start digging into the root cause analysis right after he/she is paged. (`{{last_triggered_at_epoch}}` would be replaced with the actual timestamp when incident is triggered.)

