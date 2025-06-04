# Here we process a set of files in batches, defined by 'maxfunc'.
# Once a batch has been processed, another starts
# until all files have been processed.

import queue
import threading
import boto3
import lithops
import re

bucket_name_p4 = 'task4-marcel-bucket'
prepath = 'aws_s3://' + bucket_name_p4 + '/'
lock = threading.Lock()

def get_s3_files(bucket):
	s3 = boto3.resource('s3', region_name='us-east-1')
	bucket_found = s3.Bucket(bucket)

	files_list = [(prepath + obj.key) for obj in bucket_found.objects.all()]
	return files_list

def map_filter_function(obj):
	insults = ["bobo", "ridiculo", "tonto"]

	data = obj.data_stream.read()
	text = data.decode('utf-8')

	print(text)

	for insult in insults:
		text = re.sub(insult, "CENSORED", text, flags=re.IGNORECASE)
	
	output = obj.key.split("/")[-1] 
	tmp_file = f'/tmp/censored_{output}'

	with open(tmp_file, 'w', encoding='utf-8') as fitxer_output:
		fitxer_output.write(text)

	boto3.client('s3').upload_file(
		Filename=tmp_file,
		Bucket=obj.bucket,
		Key=f'censored_{output}'
	)

def batch_execution(files_queue, function):
	end = False
	fexec = lithops.FunctionExecutor()
	while not end:
		with lock:
			if files_queue.empty():
				end = True
			else:
				file = files_queue.get()

		if not end:
			# Execute lambda and wait til it ends
			future = fexec.map(function, file)
			fexec.get_result(future)
	
def process_files(function, maxfunc, bucket):
	# Get all files inside bucket
	files = get_s3_files(bucket)
	files_queue = queue.Queue()
	for file in files:
		files_queue.put(file)

	threads = []
	for i in range(maxfunc):
		thread = threading.Thread(target=batch_execution, args=(files_queue, function))
		threads.append(thread)
		thread.start()
	
	for thread in threads:
  		thread.join()

process_files(map_filter_function, 2, bucket_name_p4)
