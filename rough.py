'''
step 1: need to read data from mysql
step 2: do i need to convert the rows in some format?
step 3: need to push data  to s3
--------------------------------------
step 1: to read data from any source what things i required:
    1. host url
        to check mysql is there: mysql --version
        to check status: sudo systemctl status mysql
since i need below configs to read from mysql then
    2. userid/username
    3. password
    4. db name
    5. table name
    6. need  library/connector to connect with mysql: pymysql
    7. lets print data

step 2: need to convert dataframe in some universal accepted
format so that we can store in S3

step 3:
    1. boto3 library se AWS se connect karo
    2. boto3.client("s3") se S3 ka darwaza kholo
'''

