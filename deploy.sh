#!/bin/bash

# Install Railway CLI
npm install -g @railway/cli

# Login to Railway using API key
railway login --apikey $RAILWAY_API_KEY

# Initialize Railway project
railway init

# Link to existing project (if needed)
# railway link

# Set environment variables
railway variables set PINECONE_API_KEY=$PINECONE_API_KEY
railway variables set GEMINI_API_KEY=$GEMINI_API_KEY
railway variables set WHAPI_API_URL=$WHAPI_API_URL
railway variables set WHAPI_API_TOKEN=$WHAPI_API_TOKEN

# Deploy to Railway
railway up
