# [Quickstart title in sentence case, for example: Quickstart: Deploy a REST API to Cloud Run]

In this quickstart, you build a small HTTP service, deploy it to [Target platform], and send a test request. The whole process takes about 15 minutes.

## Objectives

- Set up a local development environment.
- Write and run a sample application.
- Deploy the application to [Target platform].
- Test the live endpoint.

## Before you begin

Make sure that you have the following:

- [Prerequisite, for example: Node.js 20 or later installed.]
- [Prerequisite, for example: A cloud account with permission to deploy services.]
- [Prerequisite, for example: The Cloud CLI authenticated to your project.]

## Set up the project

To create a workspace and install dependencies:

1. Create a project directory and change into it:
   ```bash
   mkdir my-api && cd my-api
   ```
2. Initialize a Node.js package:
   ```bash
   npm init -y
   ```
3. Install the web framework:
   ```bash
   npm install express
   ```

## Write the application

Create a file named `server.js` with the following content:

```javascript
const express = require('express');

const app = express();
const port = process.env.PORT || 8080;

app.use(express.json());

app.get('/health', (req, res) => {
  res.status(200).json({ status: 'healthy', timestamp: new Date().toISOString() });
});

app.post('/items', (req, res) => {
  const { name, category } = req.body;
  if (!name) {
    return res.status(400).json({ error: 'name is required' });
  }
  res.status(201).json({ id: 'item-101', name, category });
});

app.listen(port, () => {
  console.log(`Listening on port ${port}`);
});
```

To run the service locally:

1. Start the server:
   ```bash
   node server.js
   ```
2. In a second terminal, send a request:
   ```bash
   curl -i http://localhost:8080/health
   ```
   The server responds with `200 OK` and a JSON body that contains `"status": "healthy"`.

## Deploy the service

Deploy from source. The command builds a container image and creates the service:

```bash
gcloud run deploy my-api \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

When the deployment completes, the CLI prints the service URL.

## Test the service

To confirm that the deployed service responds:

1. Send a request to the health endpoint:
   ```bash
   curl -i https://SERVICE_URL/health
   ```
   Replace `SERVICE_URL` with the URL printed by the deploy command.
2. Confirm that the response returns `200 OK` and the health payload:
   ```json
   {
     "status": "healthy",
     "timestamp": "2026-08-25T02:00:00.000Z"
   }
   ```

## Clean up

To stop incurring charges for the resources in this quickstart:

1. Delete the service:
   ```bash
   gcloud run services delete my-api --region us-central1 --quiet
   ```
2. Delete the container images that the source deploy created:
   ```bash
   gcloud artifacts repositories delete cloud-run-source-deploy \
     --location us-central1 --quiet
   ```

## What's next

- Configure [authentication for Cloud Run services](https://example.com/docs/auth).
- Connect the service to [Cloud SQL](https://example.com/docs/cloud-sql).
- Read the [API design guidelines](https://example.com/docs/api-guidelines).
