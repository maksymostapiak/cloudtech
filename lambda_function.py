import boto3
import re
import urllib.parse
from datetime import datetime


csv_pattern = re.compile(r'^data_.*\.csv$')
json_pattern = re.compile(r'^config_.*\.json$')

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(record['s3']['object']['key'], encoding='utf-8')
        
        if key == 'incoming/':
            continue
            
        filename = key.split('/')[-1]
        name_parts = filename.rsplit('.', 1)
        base_name = name_parts[0]
        ext = f".{name_parts[1]}" if len(name_parts) > 1 else ""
        
        if csv_pattern.match(filename) or json_pattern.match(filename):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_key = f"processed/{base_name}_{timestamp}{ext}"
        else:
            new_key = f"ignored/{filename}"
            
        s3.copy_object(
            CopySource={'Bucket': bucket, 'Key': key},
            Bucket=bucket,
            Key=new_key
        )
        
        s3.delete_object(Bucket=bucket, Key=key)
        
        print(f"Файл {filename} успішно переміщено до {new_key}")

    return {'statusCode': 200, 'body': 'Success'}