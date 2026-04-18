---
id: "docs-records-fields-types-float"
title: "Float Record Fields"
url: "https://cerb.ai/docs/records/fields/types/float/"
summary: "This page provides information on float record fields in Cerb, which are used to store numbers with decimal precision. It explains how these floating point numbers are represented in JSON format within packages and how they can be utilized in PUT or POST requests through the Records API."
tags: ["docs"]
---
A **float** field contains a number with decimal precision.

The value is a floating point number.

### Packages

As JSON from packages:

```
{ 
	 "spam_score" : 0.9999 
 }
```

### Records API

In PUT or POST requests from the API:

```
&amp;fields[spam_score]=0.9999
```

\< Extension

Image \>

