To run it:

`docker-compose up -d --build`

It will populate the database with fake data.

To retrieve all Fire objects:

`curl --location --request GET 'localhost:5000/api/fires/'`

To create a new Fire object:

`curl --location --request POST 'localhost:5000/api/fires/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "location": "Some random country",
    "url": "http://image.jpeg",
    "longitude": 1022.2,
    "latitude": 1232.2,
    "processing_date": "Tue, 13 Apr 2021 00:00:00 GMT",
    "confidence_level": 22.2
}'`

The service is deploy on Google Cloud Run:

`forest-fires-service-v4`

The Database is on Google Cloud SQL:
	
`ffdb`

The public bucket on Google Cloud Storage:

`forest_fires_model_results`

To run the `deploy.sh` script, you need to install `gcloud`