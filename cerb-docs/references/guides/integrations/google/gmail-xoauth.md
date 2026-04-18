---
id: "guides-integrations-google-gmail-xoauth"
title: "Authenticate a Gmail mailbox using IMAP and XOAUTH2"
url: "https://cerb.ai/guides/integrations/google/gmail-xoauth/"
summary: "This page provides a detailed guide on how to authenticate a Gmail mailbox using IMAP and XOAUTH2 in Cerb. It explains the necessity of using OAuth2 access tokens for Gmail authentication due to Google's retirement of passwords for POP3 and IMAP connections. The guide includes steps for configuring Google APIs and setting up a Gmail mailbox in Cerb, detailing the necessary settings such as protocol, host, and port. It also covers testing the mailbox connection to ensure successful authentication and proper functioning, including running the scheduler to verify the mailbox setup and process new messages."
tags: ["guides"]
---
- Introduction
- Configure Google APIs
- Configure your mailbox in Cerb
  - Test your mailbox

# Introduction

Google has retired passwords when connecting to Gmail using POP3 and IMAP (but not SMTP).

To authenticate you need to use OAuth2 access tokens instead.

Cerb supports XOAUTH2 authentication for IMAP mailboxes since version 9.6.

This guide explains how to configure the new feature.

# Configure Google APIs

If you haven't already configured a Gmail connected account in Cerb, follow these instructions.

Once your connected account is created you can continue to configuring the mailbox.

# Configure your mailbox in Cerb

In Cerb, navigate to **Search&nbsp;» Email Mailboxes**.

Create or edit a mailbox with the following details:

| Name: | Gmail |
| Protocol: | IMAP (TLS/SSL) |
| Host: | imap.gmail.com |
| User: | (your Gmail address) |
| Password: | (blank) |
| XOAuth2: | (your Gmail connected account from above) |
| Port: | 993 |

Click the **Test** button at the bottom of the popup.

If connected successfully, click the **Save Changes** button.

### Test your mailbox

You can verify your mailbox is working properly by running the scheduler manually.

Navigate to **Setup&nbsp;» Configure&nbsp;» Scheduler**.

In the section for **Mailbox Checker and Email Downloader**, click the **run now** link.

This will show you a detailed log of your mailbox connection. You should see 'Connected to mailbox' and 'Closed mailbox' without any authentication errors.

If any new messages were downloaded, Cerb will automatically process them. You can manually process new messages by clicking the **run now** link in the **Inbound Email Message Processor** section.

You do not need to manually run the scheduler in the future.

