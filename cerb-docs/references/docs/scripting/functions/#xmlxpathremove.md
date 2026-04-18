---
id: "docs-scripting-functions--xmlxpathremove"
title: "Scripting Function: xml_xpath_remove"
url: "https://cerb.ai/docs/scripting/functions/#xmlxpathremove"
summary: "Remove elements from XML document with XPath query"
tags: ["docs", "docs-scripting"]
---
## xml\_xpath\_remove

Remove elements from an XML document with an XPath query.

`xml_xpath_remove(xml,path)`

- **xml**: An XML object created by xml\_decode.
- **path**: The XPath query to match elements for removal.

```
{% set string_of_xml = " < response > < client_id > 1 </ client_id > < invoice_id > 123 </ invoice_id > </ response > " - %} {% set xml = xml_decode ( string_of_xml ) %} {% set xml = xml_xpath_remove ( xml , '//invoice_id' ) %} {{ xml_encode ( xml ) }}
```

```
<?xml version="1.0"?>
<response>
  <client_id>1</client_id>
</response>
```

\< Commands

Filters \>

# References

1. Wikipedia: XML - https://en.wikipedia.org/wiki/XML&nbsp;↩

2. Wikipedia: XPath - https://en.wikipedia.org/wiki/XPath&nbsp;↩&nbsp;↩2