#!/bin/bash
echo "Starting Project Management MVP..."
docker build -t pm-mvp .
docker run -d --name pm-mvp-container -p 8000:8000 pm-mvp
echo "Container started. App should be available at http://localhost:8000"