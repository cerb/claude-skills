---
id: "docs-connected-accounts"
title: "Connected Accounts"
url: "https://cerb.ai/docs/connected-accounts/"
summary: "This page discusses the use of connected accounts in Cerb to enable automations to authenticate and interact with third-party APIs through cryptographic signing of HTTP requests. It highlights the flexibility this provides by allowing bots to access a wide range of services beyond predefined actions. The sharing of connected accounts is controlled by the account owner, allowing for both team-wide and individual access. Integration examples are provided for popular services like Amazon Web Services, Dropbox, Facebook, GitHub, LinkedIn, Salesforce, Slack, Stripe, and Twilio. The page also recommends creating automation functions for each service to centralize credential management and API interactions, facilitating secure and reusable automation processes."
tags: ["docs"]
---
Automations can use **connected accounts** to cryptographically sign (or otherwise authenticate) arbitrary HTTP requests for a specific service provider.

This opens up entire third-party APIs to bots, rather than only offering a few hand-picked actions.

The _owner_ of a connected account determines how it's shared. For instance, a corporate ActivityPub account could be shared by an entire team, while a worker's private Salesforce account could be accessed by only them and their bots.

We have integration examples for many popular services:

- Airtable
- Amazon Web Services
- Azure
- Dropbox
- ElevenLabs
- Exa
- Facebook
- GitHub
- GitLab
- Gmail
- ipstack
- LinkedIn
- Linkup
- Notion
- OpenAI
- OpenWeather
- Pinecone
- Postmark
- Salesforce
- SambaNova
- Slack
- Smartsheet
- Stripe
- Tavily
- Together.ai
- Twilio

We recommend creating an automation function for each service (e.g. _Facebook Bot_) to act as a delegate. That way the credentials and API interaction for a particular service are handled in a single place, and any number of other automations can use automation.function: to interface with those services in a secure and reusable way.

