#!/bin/bash
now=$(date +'%Y-%m-%d')
status() {
  if [ $1 -ne 0 ]; then
    echo $2
    exit 1
  fi
}

if [ $ENV == "dev" ]; then
  database_name="${ENV}_landing_$DB"
  echo "Datbase name:" $database_name
fi

dump="${DB}-$now.sql.gz"

mysqldump -uroot --single-transaction --set-gtid-purged=OFF -h non-prod-landing-mysql-bq8gpk.cluster-c7mtdbojeffh.ap-south-1.rds.amazonaws.com -p${PASSWORD} ${database_name} | gzip > $dump
status $? "Error while taking dump of ${DB}"

aws s3 cp $dump s3://non-prod-landing-config/db-backup/
link=$(aws s3 presign s3://non-prod-landing-config/db-backup/$dump --expires-in 86400 --region ap-south-1)
echo "Click on the link below to download the ${DB} DB dump: $link"
rm -f $dump

