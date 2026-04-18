---
id: "tips-owned-or-watched-by-me"
title: "Build a worklist of tickets owned or watched by me"
url: "https://cerb.ai/tips/owned-or-watched-by-me/"
summary: "This page provides a tip for creating a unified worklist in Cerb that displays both tickets owned by the user and tickets they are watching. Previously, users needed to create two separate worklists for these categories, but now they can combine them into one using a quick search query. The example query provided is '(owner.id:me OR watchers:me) status:o', which efficiently consolidates the user's assignments and watched tickets into a single view."
tags: ["tips"]
---
In earlier versions of Cerb you had to create two worklists to display your watched tickets and your assignments.

Now you can display both on a single worklist with a simple quick search:

```
( owner.id: me OR watchers:me) status:o
```

 
