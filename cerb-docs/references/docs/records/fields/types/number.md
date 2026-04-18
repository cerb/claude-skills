---
id: "docs-records-fields-types-number"
title: "Number Record Fields"
url: "https://cerb.ai/docs/records/fields/types/number/"
summary: "This page provides information on number record fields in Cerb, which are used to store integer (whole number) values. It includes examples of how these fields are represented in JSON format for packages and how they can be utilized in PUT or POST requests through the Records API. The page serves as a guide for implementing and managing number fields within Cerb's system."
tags: ["docs"]
---
A **number** field contains an _integer_ (whole number) value.

The value is an integer.

### Packages

As JSON from packages:

```
{ 
	 "importance" : 50 
 }
```

### Records API

In PUT or POST requests from the API:

```
&amp;fields[importance]=50
```

\< Links

Object \>

