//Here is the complete content for `app.js`:


const AWS = require('aws-sdk');
const { Client } = require('@elastic/elasticsearch');

// Configure AWS SDK
AWS.config.update({ region: 'us-east-1' });
const cloudwatchlogs = new AWS.CloudWatchLogs();

// Configure Elasticsearch client
const esClient = new Client({ node: 'http://localhost:9200' });

async function getElasticSearchLogs(index, query) {
  const { body } = await esClient.search({
    index,
    body: {
      query: {
        match_all: {}
      }
    }
  });

  return body.hits.hits;
}

async function putLogsToCloudWatch(logGroupName, logStreamName, logEvents) {
  try {
    // Create log group if it doesn't exist
    await cloudwatchlogs.createLogGroup({ logGroupName }).promise();
  } catch (err) {
    if (err.code !== 'ResourceAlreadyExistsException') {
      throw err;
    }
  }

  try {
    // Create log stream if it doesn't exist
    await cloudwatchlogs.createLogStream({ logGroupName, logStreamName }).promise();
  } catch (err) {
    if (err.code !== 'ResourceAlreadyExistsException') {
      throw err;
    }
  }

  // Put log events to CloudWatch
  const params = {
    logEvents,
    logGroupName,
    logStreamName
  };

  await cloudwatchlogs.putLogEvents(params).promise();
}

async function convertElasticSearchLogsToCloudWatch() {
  const esIndex = 'your_elasticsearch_index';
  const cwLogGroupName = 'your_cloudwatch_log_group';
  const cwLogStreamName = 'your_cloudwatch_log_stream';

  // Get logs from Elasticsearch
  const esLogs = await getElasticSearchLogs(esIndex);

  // Transform logs into CloudWatch format
  const logEvents = esLogs.map(log => ({
    message: JSON.stringify(log._source),
    timestamp: new Date(log._source['@timestamp']).getTime()
  }));

  // Put logs to CloudWatch
  await putLogsToCloudWatch(cwLogGroupName, cwLogStreamName, logEvents);
}

// Run the conversion
convertElasticSearchLogsToCloudWatch()
  .then(() => console.log('Logs have been successfully converted and sent to CloudWatch'))
  .catch(err => console.error('Error converting logs:', err));

/*
This script does the following:
1. Configures AWS SDK and Elasticsearch client.
2. Fetches logs from an Elasticsearch index.
3. Transforms the logs into CloudWatch format.
4. Creates the necessary log group and log stream in CloudWatch if they don't exist.
5. Puts the transformed logs into CloudWatch.

Adjust `your_elasticsearch_index`, `your_cloudwatch_log_group`, and `your_cloudwatch_log_stream` with your actual values.
*/