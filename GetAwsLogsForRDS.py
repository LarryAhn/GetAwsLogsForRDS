# -*- encoding: utf-8 -*-
import sys
import boto.rds
import datetime

AWS_REGION = '{INPUT AWS REGION}'
AWS_ACCESS_KEY = '{INPUT AWS ACCES KEY}'
AWS_SECRET_KEY = '{INPUT AWS SECRET KEY}'
DB_INSTANCE_NAME = '{INPUT DB INSTANCE NAME}'

now = datetime.datetime.now()
nowDateTime = now.strftime('%Y-%m-%d,%H:%M:%S')

OUTPUT_FILE_NAME = DB_INSTANCE_NAME + '_' + nowDateTime +'.log'

def get_rds_logs(dbinstance_id, output, max_records=None,
                 aws_access_key_id=None, aws_secret_access_key=None):
    conn = boto.rds.connect_to_region(
        AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY)

    with open(output, 'w') as f:
        for log_file in conn.get_all_logs(dbinstance_id, max_records=max_records):
            print 'Download logfile Name: %s(fileSize : %d)' % (log_file.log_filename, int(log_file.size))
            
	    try:
                log = conn.get_log_file(dbinstance_id, log_file.log_filename)
                try:
                    f.write(log.data)
                except AttributeError:
                    pass
            except:
                print 'Error while download %s' % log_file.log_filename

if __name__ == '__main__':
    get_rds_logs(dbinstance_id=DB_INSTANCE_NAME,
                 output=OUTPUT_FILE_NAME,
                 aws_access_key_id=AWS_ACCESS_KEY,
                 aws_secret_access_key=AWS_SECRET_KEY)
