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
	print(obj)
	return 1

def reduce_filter_function(results):
	return sum(results)

# Obtain files (path?)
files = get_s3_files()
for f in files:
	print(f)

#files = ['task3-marcel-bucket', 'task3-marcel-bucket', 'task3-marcel-bucket']
with lithops.FunctionExecutor() as executor:
	futures = executor.map_reduce(map_filter_function, files, reduce_filter_function)
	results = executor.get_result(futures)
	print(f'insults censurats: {results}')
