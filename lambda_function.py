import boto3
import datetime
import json
import os
import time

'''
Create by sj kwon
Email kofdx7@gmail.com
'''

class Rds:
	def __init__(self,rds_identifier):
		self.rds_client=boto3.client('rds');
		self.rds_identifier=rds_identifier;
		
	def get_rds_status(self):
		response = self.rds_client.describe_db_instances(DBInstanceIdentifier=self.rds_identifier);
		rds_instances=response.get("DBInstances")
		rds=rds_instances.pop(0)
		rds_status=rds.get("DBInstanceStatus")
		return rds_status

	def schedule_rds(self):
		rds_status=self.get_rds_status();
		cron_pattern=self.get_start_pattern(rds_status) if rds_status=="stopping" or rds_status=="available" else self.get_stop_pattern(rds_status);
		return cron_pattern
		
	def stop_rds(self):
		rds_snapshot = self.rds_identifier  + datetime.datetime.now().strftime("-%Y-%m-%d-%H%M").strip()
		response = self.rds_client.stop_db_instance(
	    		DBInstanceIdentifier=self.rds_identifier
		)
		print("#  SUCCESS RDS STOP")
		
	def start_rds(self):
		response = self.rds_client.start_db_instance(
    			DBInstanceIdentifier=self.rds_identifier
			)
		print("#  SUCCESS RDS START")	

	def get_start_pattern(self,rds_status):
		if rds_status=="available":
			print("# STOP RDS ...! ")
			self.stop_rds();
		#set your time for rds start. 
	#default is before 3 hours after 7 days
		_datetime=datetime.datetime.today()+datetime.timedelta(days=7)-datetime.timedelta(hours=3)
		cron_pattern=get_cron_pattern(_datetime);	
		return ("START",cron_pattern)
		
	def get_stop_pattern(self,rds_status):
		if rds_status == "stopped":
			print("# START RDS ...! ")
			self.start_rds();
		#set your time for rds stop. 
		#default is 1 hours.
		_datetime=datetime.datetime.today()+datetime.timedelta(minutes=15)
		cron_pattern=get_cron_pattern(_datetime);
		return ("STOP",cron_pattern)


class EventBridge:
	
	def __init__(self,events_rule_name):
		self.eb_client = boto3.client('events');
		self.events_rule_name=events_rule_name;

	def put_rule(self,schedule):
		response = self.eb_client.put_rule(
			Name=self.events_rule_name,
			ScheduleExpression=schedule[1],
			State='ENABLED'
		)
		print("#  PUT RULE RDS "+ schedule[0]+":" + self.events_rule_name + "[" + schedule[1] + "]")
		



			
def get_cron_pattern(_datetime):
	cron_pattern = "cron("  + _datetime.strftime("%M %H %d %m").strip() + " ? " + _datetime.strftime("%Y") + ")"
	return cron_pattern




def lambda_handler(event, context):
	# TODO implement

	rds=Rds(os.getenv('RDS_IDENTIFIER'))
	eb=EventBridge(os.getenv('EVENT_RULE'))

	schedule=rds.schedule_rds();
	eb.put_rule(schedule);
	
	return {
		'statusCode': 200,
		'body': json.dumps('End')
	}
