# Welcome to PyRun!

# To help you get started, we have included a small example
# showcasing how to use lithops.

# To install more packages, please edit the environment.yml
# file found in the .pyrun directory.

import boto3
import lithops
import re

bucket_name_p3 = 'task3-marcel-bucket'
prepath = 'aws_s3://' + bucket_name_p3 + '/'

def get_s3_files():
	s3 = boto3.resource('s3', region_name='us-east-1')
	bucket = s3.Bucket(bucket_name_p3)

	file_list = [(prepath + obj.key) for obj in bucket.objects.all()]
	return file_list

def map_filter_function(obj):

	insults = ["bobo", "ridiculo", "tonto"]

	data = obj.data_stream.read()
	text = data.decode('utf-8')

	print(text)

	for insult in insults:
		text = re.sub(insult, "CENSORED", text, flags=re.IGNORECASE)
	count = text.count('CENSORED')
	print(f"Count: {count}")

	output = obj.key.split("/")[-1] 
	tmp_file = f'/tmp/censored_{output}'

	with open(tmp_file, 'w', encoding='utf-8') as fitxer_output:
		fitxer_output.write(text)
	
	# Subir el archivo censurado a S3
	boto3.client('s3').upload_file(
		Filename=tmp_file,
		Bucket=obj.bucket,
		Key=f'censored_{output}'
	)
	return count

def reduce_filter_function(results):
	return sum(results)

files = get_s3_files()
for f in files:
	print(f)

with lithops.FunctionExecutor() as executor:
	futures = executor.map_reduce(map_filter_function, files, reduce_filter_function)
	results = executor.get_result(futures)
	print(f'Insults censurats: {results}')
