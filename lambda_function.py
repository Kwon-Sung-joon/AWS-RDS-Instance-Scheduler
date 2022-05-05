import boto3
import datetime
import json
import os
import time

def get_rds_status(rds_identifier):
	rds_client = boto3.client('rds');
	response = rds_client.describe_db_instances(DBInstanceIdentifier=rds_identifier);
	rds_instances=response.get("DBInstances")
	rds=rds_instances.pop(0)
	rds_status=rds.get("DBInstanceStatus")
	return rds_status

def get_cron_pattern(_datetime):
	cron_pattern = "cron(0 "  + _datetime.strftime("%H %d %m").strip() + " ? " + _datetime.strftime("%Y") + ")"
	return cron_pattern

def get_start_pattern(rds_status,rds_identifier):
	if rds_status=="available":
		print("# STOP RDS ...! ")
		stop_rds(rds_identifier);
	#start pattern is now + 7days - 3 hours
	_datetime=datetime.datetime.today()+datetime.timedelta(days=7)-datetime.timedelta(hours=3)
	cron_pattern=get_cron_pattern(_datetime);	
	return ("START",cron_pattern)
	
def get_stop_pattern(rds_status,rds_identifier):
	if rds_status == "stopped":
		print("# START RDS ...! ")
		start_rds(rds_identifier);
	#stop pattern is now + 3hours 
	_datetime=datetime.datetime.today()+datetime.timedelta(hours=1)
	cron_pattern=get_cron_pattern(_datetime);
	return ("STOP",cron_pattern)

def schedule_rds(rds_identifier):
	rds_status=get_rds_status(rds_identifier);
	client = boto3.client('rds')
	cron_pattern=get_start_pattern(rds_status,rds_identifier) if rds_status=="stopping" or rds_status=="available" else get_stop_pattern(rds_status,rds_identifier);
	return cron_pattern


def stop_rds(rds_identifier):
	client=boto3.client('rds');
	rds_snapshot = rds_identifier  + datetime.datetime.now().strftime("-%Y-%m-%d-%H%M").strip()
	response = client.stop_db_instance(
    DBInstanceIdentifier=rds_identifier,
    DBSnapshotIdentifier=rds_snapshot
	)
	
	print("#  SUCCESS RDS STOP")

def start_rds(rds_identifier):
	client=boto3.client('rds');
	response = client.start_db_instance(
    DBInstanceIdentifier=rds_identifier
	)
	print("#  SUCCESS RDS START")	

def put_rule(schedule,events_rule_name):
	client = boto3.client('events')
	response = client.put_rule(
		Name=events_rule_name,
		ScheduleExpression=schedule[1],
		State='ENABLED'
	)
	print("#  PUT RULE RDS "+ schedule[0]+":" + events_rule_name + "[" + schedule[1] + "]")

def lambda_handler(event, context):
	# TODO implement

	rds_identifier = os.environ['RDS_IDENTIFIER']
	events_rule_name = os.environ['EVENT_RULE']

	schedule=schedule_rds(rds_identifier);
	put_rule(schedule,events_rule_name);

	print(rds_snapshot);



	return {
		'statusCode': 200,
		'body': json.dumps('End')
	}
