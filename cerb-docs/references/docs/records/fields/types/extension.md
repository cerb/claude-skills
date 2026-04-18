---
id: "docs-records-fields-types-extension"
title: "Extension Record Fields"
url: "https://cerb.ai/docs/records/fields/types/extension/"
summary: "This page provides information on extension record fields in Cerb, which refer to plugin extensions that can alter the functionality of a record based on the selected extension. It includes examples of how to specify an extension using JSON in packages and how to use the Records API to set an extension in PUT or POST requests. The page is part of a larger documentation context, likely detailing how to manage and utilize extensions within Cerb."
tags: ["docs"]
---
An **extension** field refers to a plugin extension. The functionality of a record may change based on the selected extension.

### Packages

As JSON from packages:

```
{ 
	 "extension_id" : "example.plugin.extension.name" 
 }
```

### Records API

In PUT or POST requests from the API:

```
&amp;fields[extension_id]=example.plugin.extension.name
```

\< Context

Float \>

