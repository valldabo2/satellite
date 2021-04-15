export PROJECT_ID=valued-amp-310613
docker build -t gcr.io/${PROJECT_ID}/forest-fires:v4 .
docker push gcr.io/${PROJECT_ID}/forest-fires:v4
gcloud run services update forest-fires-service-v4 --port=8080 --image=gcr.io/${PROJECT_ID}/forest-fires:v4 --update-env-vars=FLASK_APP=project/__init__.py,FLASK_ENV=production,DATABASE_URL="postgresql://postgres:ffdb1234@/postgres?host=/cloudsql/valued-amp-310613:europe-west4:ffdb",SQL_HOST="/cloudsql/valued-amp-310613:europe-west4:ffdb",SQL_PORT=5432,DATABASE=postgres,INSTANCE_CONNECTION_NAME=valued-amp-310613:europe-west4:ffdb --add-cloudsql-instances valued-amp-310613:europe-west4:ffdb --platform=managed



#gcloud run deploy forest-fires-service-v4 --allow-unauthenticated
#
#gcloud run deploy forest-fires-service-v4 --port=8080 --image=gcr.io/${PROJECT_ID}/forest-fires:v4 --update-env-vars=FLASK_APP=project/__init__.py,FLASK_ENV=production,DATABASE_URL=postgresql://postgres:ffdb1234@/postgres?host=/cloudsql/valued-amp-310613:europe-west4:ffdb/postgres,SQL_HOST=/cloudsql/valued-amp-310613:europe-west4:ffdb,SQL_PORT=5432,DATABASE=postgres --allow-unauthenticated --add-cloudsql-instances valued-amp-310613:europe-west4:ffdb
#gcloud beta run services add-iam-policy-binding --region=us-west1 --member=allUsers --role=roles/run.invoker forest-fires-service-v5
#gcloud run services update forest-fires-service-v5         \
#  --add-cloudsql-instances valued-amp-310613:europe-west4:ffdb \
#  --update-env-vars INSTANCE_CONNECTION_NAME="valued-amp-310613:europe-west4:ffdb"
