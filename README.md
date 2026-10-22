# Homework Submission: Inventory Agent App

This repository contains the built Docker image for the inventory agent application.

## Prerequisites
* Docker Desktop installed and running

## How to Run the Application

1. **Load the Docker image** from the provided `.tar` archive:
   ```bash
   docker load -i inventory_homework.tar
   ```

2. **Run the container** (replace `[PORT]` with the actual port your app uses, e.g., `8080:8080`):
   ```bash
   docker run -d -p [PORT]:[PORT] --name inventory-app inventory-agent-app:latest
   ```

3. **Access the application** by opening your browser and navigating to:
   ```text
   http://localhost:[PORT]
   ```

## Stopping the App
To stop and clean up the container after grading:
```bash
docker stop inventory-app
docker rm inventory-app
```
