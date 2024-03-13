#!/bin/bash

# Define the path to your .env file
ENV_FILE=".env"

# Define the name of the Kubernetes Secret you want to create
SECRET_NAME="my-taskscheduler-api-secret"

# Prepare the command to create a Kubernetes secret
CMD="kubectl create secret generic $SECRET_NAME"

# Loop through each line in the .env file
while IFS='=' read -r key value || [[ -n "$key" ]]; do
  # Skip if line is empty
  if [ -z "$key" ]; then
    continue
  fi
  # Add each key-value pair as a literal to the command
  CMD+=" --from-literal=$key=$value"
done < "$ENV_FILE"

# Execute the command to create the Secret
echo "Executing: $CMD"
eval $CMD
