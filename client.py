from azure.storage.table import TableService
from azure.storage.queue import QueueService

import argparse
import datetime
import time
import os
import subprocess
import base64
import json
import uuid

# Parse the configuration arguments
parser = argparse.ArgumentParser(description="MentorMate Azure Processing Client Configuration")
# File Share Args
parser.add_argument("--storage-endpoint", required = True)
parser.add_argument('--storage-account', required = True)
parser.add_argument('--storage-key', required = True)

args = parser.parse_args()

# Configure the table service
table_service = TableService(
	account_name = args.storage_account,
	account_key = args.storage_key)
# Configure the queue service
queue_service = QueueService(
	account_name = args.storage_account,
	account_key = args.storage_key)

def p(message, log = False):
	"Custom print implementation with Azure logging"
	print(">> %s >> %s" % (datetime.datetime.now(), message))
	
	if log is True:
		# A timestamp column is automatically added by Azure
		table_service.insert_entity("logs", { "PartitionKey": "processing", "RowKey": uuid.uuid1().hex, "Message": message })

def mount(share):
	"Mount Azure File Share"
	p("Mounting %s" % share, True)
	
	mount_source = os.path.join(args.storage_endpoint, share)
	mount_destination = os.path.join("/mnt", share)
	mount_args = "vers=3.0,user=%s,password=%s,dir_mode=0777,file_mode=0777" % (args.storage_account, args.storage_key)
	
	if not os.path.exists(mount_destination):
		os.makedirs(mount_destination)
	
	# Mount the Azure File Share on the host
	p("Exec: mount -t cifs %s %s -o %s" % (mount_source, mount_destination, mount_args))
	subprocess.call(["mount", "-t", "cifs", mount_source, mount_destination, "-o", mount_args])

def process(share, message):
	"Process here"
	p("Processing message: %s" % message, True)
	
	if share is not None:
		# Simulate work by listing all files in the attached share
		mount_destination = os.path.join("/mnt", share)
		subprocess.call(["ls", mount_destination])

	# Simulate processing time
	time.sleep(30)

def unmount(share):
	"Unmount Azure File Share"
	p("Unmounting %s" % share, True)
	
	mount_destination = os.path.join("/mnt", share)
	
	# Unmount the Azure File Share on the host
	p("Exec: umount %s" % mount_destination)
	subprocess.call(["umount", mount_destination])

p("")
p("================")
p("Starting MentorMate Azure Processing Client")
p("Storage Endpoint %s" % args.storage_endpoint)
p("Storage Key %s" % args.storage_key)
p("================")

while True:
	share = None
	message = None

	p("Polling Pending queue...")
	# Peek the next pending message
	messages = queue_service.get_messages("pending")
	for m in messages:
		message = m
		break

	# Parse the message
	if message is None:
		p("No new messages")
	else:
		message_text = base64.b64decode(message.message_text)
		message_json = json.loads(message_text)
		
		if "share" in message_json:
			share = message_json["share"]
		
		# Delete the peding message
		p("Dequeue Pending: %s" % message_text, True)
		queue_service.delete_message("pending", message.message_id, message.pop_receipt)
		
		if share is not None:
			mount(share)
		
		# Enqueue a processing message
		# Use the original message as it is properly encoded
		p("Enqueue Processing: %s" % message_text, True)
		queue_service.put_message("processing", message.message_text)    
		process(share, message_text)
		
		# Enqueue a finished message with the result
		# Use the original message as it is properly encoded
		message_json["success"] = True
		message_text = json.dumps(message_json)
		p("Enqueue Finished: %s" % message_text, True)
		message_text = base64.b64encode(message_text)
		queue_service.put_message("finished", message_text)

		if share is not None:
			unmount(share)

	p("Done")
	p("Sleep...")
	p("================")
	
	time.sleep(10)
	