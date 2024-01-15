#!/bin/sh
# needed so a database file is created to be able to create a admin user automatically
/app/data/pocketbase serve --http 0.0.0.0:8090 --automigrate=0 --dir=/app/data/pb_data/ --publicDir=/app/data/pb_public/  &
sleep 4
kill $(pidof pocketbase)
# creates admin from env vars or errors if nothing is provided
/app/data/pocketbase admin create $PRIVATE_POCKETBASE_ADMIN $PRIVATE_POCKETBASE_PASSWORD
# starts PocketBase
/app/data/pocketbase serve --http 0.0.0.0:8090 --automigrate=0 --dir=/app/data/pb_data/ --publicDir=/app/data/pb_public/ 
