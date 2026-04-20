---
id: "docs-scripting-filters--permalink"
title: "Scripting Filter: permalink"
url: "https://cerb.ai/docs/scripting/filters/#permalink"
summary: "Convert text into a URL-friendly permalink format"
tags: ["docs", "docs-scripting"]
---
## permalink

(Added in [9.2.3](/releases/9.2.3/))

```
{% set text = "This is the title of a record!" %} {{ text | permalink | lower }}
```

```
this-is-the-title-of-a-record
```
