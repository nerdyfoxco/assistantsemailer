import express from 'express';
import { OAuth2Client } from 'google-auth-library';
import { GmailPoller } from './client';
import { IngestionService } from './ingestion';

const app = express();
const port = process.env.PORT || 3002;
const BRAIN_URL = process.env.BRAIN_URL || 'http://localhost:3000';

app.use(express.json());

// Routes
app.get('/healthz', (req, res) => {
  res.json({ status: 'ok', service: 'ears-gmail-gateway' });
});

// Start Server
app.listen(port, () => {
  console.log(`[Ears] Gmail Gateway listening on port ${port}`);

  // Start Background Ingestion
  // Note: In real app, we might wait for explicit start or separate worker process.

  // MOCK AUTH for MVP:
  // We need a real token to hit Gmail. Assuming we pass it via ENV or use Default Creds.
  // For this "Skeleton" phase, we'll initialize it.
  const auth = new OAuth2Client(
    process.env.GMAIL_CLIENT_ID || 'dummy_id',
    process.env.GMAIL_CLIENT_SECRET || 'dummy_secret'
  );
  // Important: We need a Refresh Token to actually work!
  if (process.env.GMAIL_REFRESH_TOKEN) {
    auth.setCredentials({ refresh_token: process.env.GMAIL_REFRESH_TOKEN });
  }

  const poller = new GmailPoller(auth);
  const ingestion = new IngestionService(poller, { brainUrl: BRAIN_URL });

  ingestion.startLoop(30000); // 30s loop
});
