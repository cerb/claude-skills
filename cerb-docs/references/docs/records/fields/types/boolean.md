---
id: "docs-records-fields-types-boolean"
title: "Boolean Record Fields"
url: "https://cerb.ai/docs/records/fields/types/boolean/"
summary: "This page provides information on boolean record fields in Cerb, explaining that these fields hold true or false values represented as `1` or `0`. It includes examples of how boolean fields are used in JSON packages and in PUT or POST requests through the Records API, demonstrating how to set a boolean field to true or false in these contexts."
tags: ["docs"]
---
A **boolean** field contains a _true_ or _false_ value.

The value is `1` (true) or `0` (false).

### Packages

As JSON from packages:

```
{ 
	 "checkbox" : 1 
 }
```

### Records API

In PUT or POST requests from the API:

```
&amp;fields[checkbox]=1
```

\< Record Fields

Context \>

