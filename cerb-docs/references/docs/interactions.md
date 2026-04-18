---
id: "docs-interactions"
title: "Interactions"
url: "https://cerb.ai/docs/interactions/"
summary: "This page provides an overview of 'Interactions' in Cerb, which are automated, conversational processes designed to collect additional input through web-based forms or external events. These interactions can pause between steps and resume once the necessary input is received. Examples include troubleshooting interactions that ask specific questions to diagnose issues and verification interactions that send codes for email verification. Users can create custom interactions and integrate them into various Cerb components like widgets, cards, and email messages. The page also lists triggers used to build these interactions, such as those for worker interactions and website visitor interactions."
tags: ["docs"]
---
**Interactions** are automated, conversational processes that can pause between steps to collect additional input, such as web-based forms or other external events.

An interaction continues to the next step once additional input is received.

The most common source of additional input is a web-based form with multiple fields.

 

For instance, a troubleshooter interaction can ask a series of increasingly specific questions to help narrow down the potential cause of a problem. A verification interaction can send a code to a new email address and ask the user to verify it.

You can build your own interactions and add them to toolbars found through Cerb on widgets, cards, profiles, sheets, worklists, email messages, and more.

The following triggers are used to build interactions:

| Trigger | &nbsp; |
| --- | --- |
| interaction.worker | Interactions with a worker using web forms. |
| interaction.worker.explore | Interactions use custom logic to return the next record in explore mode. |
| interaction.website | Interactions with visitors on third-party websites using web forms. |

