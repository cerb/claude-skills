---
id: "docs-scripting-filters--column"
title: "Scripting Filter: column"
url: "https://cerb.ai/docs/scripting/filters/#column"
summary: "Extract a key from each item in an array as a new array"
tags: ["docs", "docs-scripting"]
---
## column

(Added in [10.1.1](/releases/10.1.1/))

Extract a key from each item in an array as a new array. This has the same effect as the [array\_column()](/docs/scripting/functions/#array_column) function.

```
{% set people = [
  {'name':'Kina Halpue', 'email':'kina@cerb.example'},
  {'name':'Milo Dade', 'email': 'milo@cerb.example'}
] %}
{{people|column('email')|join(', ')}}
```

```
kina@cerb.example, milo@cerb.example
```
