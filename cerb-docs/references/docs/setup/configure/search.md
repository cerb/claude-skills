---
id: "docs-setup-configure-search"
title: "Search"
url: "https://cerb.ai/docs/setup/configure/search/"
summary: "This page discusses the implementation of full-text search filters in Cerb worklists, which allow users to search record content using specific terms and phrases. It explains that while MySQL's FULLTEXT indexes are used by default and optimized for efficiency, they may not be ideal for larger environments. For scalability, the page suggests switching to more robust search engines like Elasticsearch or Sphinx, which offer faster performance and greater control over content indexing, albeit requiring additional service management."
tags: ["docs"]
---
 

Many worklists provide a full-text1 search filter to match record content based on terms and phrases.

For instance, you may need to search your email history for the phrase: `"facebook ads" receipt`.

By default, these searches are implemented as `FULLTEXT` indexes in MySQL2. We've done a lot of optimization to keep these searches efficient, and it _"just works"_. However, MySQL isn't an optimal search engine for larger environments.

As you scale, you may decide to switch to Elasticsearch or Sphinx. We support both. These options require you to manage an additional service, but they're much faster and provide you with more control over how your content is indexed.

# References

1. https://en.wikipedia.org/wiki/Full-text\_search&nbsp;↩

2. http://dev.mysql.com/doc/refman/5.7/en/fulltext-search.html&nbsp;↩

