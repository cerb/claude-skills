# KATA Reference

**KATA** = **K**ey **A**nnotated **T**ree of **A**ttributes

KATA is Cerb's human-friendly format for modeling structured data. It is used throughout Cerb for configurations, customizations, sheets, toolbars, events, and automations. It is inspired by YAML but avoids its common pitfalls.

---

## Table of Contents

- [KATA vs YAML](#kata-vs-yaml)
- [Syntax Rules](#syntax-rules)
  - [Indentation](#indentation)
  - [Keys](#keys)
  - [Key Names with Identifiers](#key-names-with-identifiers)
  - [Values](#values)
  - [Whitespace and Blank Lines](#whitespace-and-blank-lines)
  - [Comments](#comments)
  - [Text Blocks](#text-blocks)
  - [References](#references)
- [Annotations](#annotations)
  - [Annotation Reference](#annotation-reference)
  - [Chaining Annotations](#chaining-annotations)
- [Scripting](#scripting)
  - [Tags](#tags)
  - [Variables](#variables)
  - [Strings](#strings)
  - [Arrays and Objects](#arrays-and-objects)
  - [Dates](#dates)
  - [Conditional Logic](#conditional-logic)
  - [Operators](#operators)
  - [Loops](#loops)
  - [Regular Expressions](#regular-expressions)
  - [JSON](#json)
  - [XML](#xml)
  - [Template Commands](#template-commands)
  - [Tests](#tests)
- [Functions Reference](#functions-reference)
- [Filters Reference](#filters-reference)
- [Dialects](#dialects)

---

## KATA vs YAML

| Aspect | YAML | KATA |
|-|-|-|
| **Data types** | Auto-detects types (requires quoting for text like `yes`, `no`, `1.0`)  | All values are text by default; annotations convert types explicitly |
| **Security** | Language-specific tags can execute external code | Never executes or references outside code |
| **Curly braces** | Interprets `{}` (conflicts with `{{placeholders}}`) | Does not interpret `{}` in values — placeholders work freely |
| **Text blocks** | Multiple symbols (`\|`, `\|-`, `>`) with inconsistent linefeed handling | Key annotations imply blocks; consistent linefeed behavior |
| **Lists** | Requires `-` prefix, indentation-sensitive | `@csv` and `@list` annotations; sibling keys can repeat with `/name` |
| **Comments** | Any text after unquoted `#` is ignored | Only indented lines beginning with `#` are comments |
| **Colons in values** | Requires quoting | No escaping needed |

---

## Syntax Rules

### Indentation

KATA uses spaces (not tabs) to build a tree hierarchy. Keys end with colons (`:`), and their children are indented beneath them.

**Convention:** Two spaces per indentation level.

```
parent:
  child:
    grandchild: value
```

### Keys

- Key names end with colons (`:`)
- Keys must be unique among siblings
- Multiple top-level keys are allowed (no single root required)
- Keys can contain letters, numbers, underscores, dots, and hyphens

### Key Names with Identifiers

When identical key names must appear under the same parent, append a forward slash (`/`) followed by a unique identifier:

```
picklist/status:
  options@csv: open, closed
picklist/color:
  options@csv: red, green, blue
```

The identifier (after `/`) can contain letters, numbers, and underscores. It becomes part of the key path.

### Values

Text values follow the colon on the same line. Multiple colons in values do not require escaping:

```
widget:
  label: Status:
  description: The current status of the item: active or inactive
```

### Whitespace and Blank Lines

- Blank lines can separate sibling keys for readability
- Blank lines within a block must match the indentation of the parent key

### Comments

Lines beginning with `#` (at the current indentation level) are comments. Unlike YAML, `#` in values does not need escaping:

```
# This is a comment
article:
  title: Using #commands in chat
  content@text:
    # This is a Markdown heading, not a comment
    Some **bold** text.
```

### Text Blocks

Multi-line values are created with annotations that imply text blocks (like `@text`, `@bool`, `@csv`, `@json`, `@list`, `@kata`, `@raw`, `@nowrap`). The indented text continues until indentation returns to the key level.

```
comment:
  content@text:
    This is a comment with
    multiple lines of content.

    It stops when indentation returns.
format: markdown
```

With `@text`, the first trailing linefeed is removed. Subsequent linefeeds are preserved. To keep trailing linefeeds, end with an indented blank line.

### References

Reusable sections are defined with `&` prefix on top-level keys. Other keys use `@ref` to copy reference contents:

```
picklist:
  options@ref: colors

&colors@list:
  red
  green
  blue
```

**Dot-notation targeting** — reference a nested child:
```
options@ref: options.colors
```

**Nested references** — references can themselves contain `@ref` annotations.

**Annotation replacement** — when using `@ref`, any remaining annotations after `@ref` affect the copied content.

---

## Annotations

Annotations are comma-separated tags appended to key names starting with `@`. They provide type conversion and special handling instructions for values.

```
picklist:
  options:
    color@csv: red, green, blue
    multiple@bool: no
    count@int: 3
```

### Annotation Reference

| Annotation  | Description | Example |
|-|-|-|
| `@base64` | Converts base64-encoded text to binary data | `image@base64: QnVzdGVkIQ==` |
| `@bit` | Converts to `0` or `1`. False: null/blank/`0`/`false`/`off`/`no`/`n`. True: anything else | `result@bit: off` → `0` |
| `@bool` | Converts to `true` or `false`. Same false values as `@bit` | `enabled@bool: yes` → `true` |
| `@csv` | Converts comma-separated text to array | `colors@csv: red,green,blue` |
| `@date` | Converts human-readable date to Unix timestamp. Absolute (`Jan 1 2025 08:00`) or relative (`+2 hours`) | `when@date: +2 hours` |
| `@float` | Parses value as floating-point number | `rate@float: 3.14` |
| `@int` | Parses value as whole number | `count@int: 42` |
| `@json` | Parses text as JSON-encoded value | `data@json: {"key":"value"}` |
| `@kata` | Parses text as KATA-encoded value. Useful for dynamically generating KATA via scripting | `records@kata: ...` |
| `@key` | Sets value from a dictionary key path | `status@key: response.http.status.code` |
| `@list` | Converts line-delimited text block to array | `colors@list:` (one per line) |
| `@nowrap` | Reads indented text block and removes newlines (joins into single line) | `content@nowrap: ...` |
| `@optional` | Removes the key entirely if the value is empty | `field@optional: {{maybe_empty}}` |
| `@raw` | Returns text without substituting placeholders or executing scripts | `template@raw: {{person}} is {{title}}` |
| `@ref` | Copies contents from a `&key:` reference by name or dot-notation path | `options@ref: colors` |
| `@text` | Reads indented text block. First trailing linefeed removed; subsequent preserved | `content@text: ...` |
| `@trim` | Removes leading and trailing whitespace from value | `name@trim:   padded   ` |

### Chaining Annotations

Multiple annotations chain left-to-right, separated by commas:

```
# Copy value of key 'a', then convert to integer
b@key,int: a

# Parse JSON, then treat as text block
data@text,json:
  {"key": "value"}
```

### Storing Twig arrays in `set:`

Annotations parse *text*. When the right-hand side of a `set:` is a Twig expression that produces an array (e.g. from `|filter`, `|map`, `|values`, or a `customfields`-expanded list CF), the annotation must match what the rendered text actually looks like:

- **`@json`** requires the text to already be JSON-encoded. For Twig array values, pipe through `|json_encode` first:
  ```
  set:
    tokens@json: {{some_array|json_encode}}
  ```
  Writing `tokens@json: {{some_array}}` without `|json_encode` is broken — Twig stringifies the array (often as `Array`) and `@json` fails to parse it. `@json` is the most general option and handles nested objects, mixed types, and strings containing newlines or commas.

- **`@list`** is the simplest annotation for a flat list of strings with no embedded newlines:
  ```
  set:
    tokens@list: {{some_array|join("\n")}}
  ```

- **`@csv`** suits short flat lists of strings with no embedded commas:
  ```
  set:
    tags@csv: {{some_array|join(",")}}
  ```

Pick the lightest annotation that fits: `@list`/`@csv` for plain string lists, `@json` for anything richer.

---

## Scripting

KATA features that enable scripting provide a dictionary of placeholders and support dynamic content generation. The scripting language is based on **Twig** (a PHP templating engine).

### Tags

| Tag | Purpose | Example |
|-|-|-|
| `{{ }}` | Output a placeholder or expression | `{{first_name}}` |
| `{% %}` | Execute a control flow statement | `{% if x > 5 %}...{% endif %}` |
| `{# #}` | Hidden code comment (not output) | `{# This won't appear #}` |

### Variables

Variables use double curly braces for interpolation:

```
Hello, {{first_name}}!
```

**Creating variables:**
```
{% set name = "Kina" %}
{% set quantity = 5 %}
{{name}} has {{quantity}} gold stars.
```

**Scope:** Variables are temporary and only exist within the same template/action.

**Filters** transform values via the pipe (`|`) character:
```
Hi, {{first_name|upper}}!
```

**Default values:**
```
Hi {{name|default('there')}}
```

**Filter stacking:**
```
{{first_name|default('there')|upper}}
```

### Strings

Strings use single or double quotes:
```
{{"This is literal text"|truncate(7)}}
```

**Concatenation** uses the tilde (`~`) operator:
```
{% set full_name = first_name ~ " " ~ last_name %}
```

**Whitespace control** uses a dash (`-`) at tag boundaries:
```
This text
{{-" has no leading or trailing whitespace "-}}
in it.
```
Output: `This text has no leading or trailing whitespace in it.`

### Arrays and Objects

**Arrays** — numerically indexed:
```
{% set colors = ['red','green','blue'] %}
Item 0 is {{colors.0}}
Item 2 is {{colors[2]}}
```

**Objects** — key-value pairs:
```
{% set person = {"first_name": "Kina", "last_name": "Halpue", "age": 63} %}
{{person.first_name}} is {{person.age}}.
```

**Dynamic keys:**
```
{% set key = 'first_name' %}
{{person[key]}}
```

**Modifying with `dict_set()`:**
```
{% set var = dict_set(var, 'group.name', 'Support') %}
{% set var = dict_set(var, 'group.members.[]', 'Kina') %}  {# append to array #}
```

**Array difference:**
```
{% set diff = array_diff(arr2, arr1) %}
```

### Dates

**Formatting** with `|date` filter (PHP DateTime format):
```
{{'now'|date('F d, Y h:ia T')}}
{{'tomorrow 5pm'|date('D, d F Y H:i T')}}
{{'+2 weeks 08:00'|date('Y-m-d h:ia T')}}
```

**Timezone** (second parameter):
```
{{ts_now|date(time_format, 'Asia/Kolkata')}}
```

**Unix timestamps:**
```
{{'now'|date('U')}}
```

**Date modification:**
```
{% set timestamp = date('now') %}
{{timestamp|date_modify('+2 days')|date('D, d M Y T')}}
```

### Conditional Logic

```
{% if sla_expiration >= 'now'|date('U') %}
  Your SLA coverage is active.
{% elseif sla_expiration >= '-7 days'|date('U') %}
  Your SLA recently expired.
{% else %}
  Your SLA coverage has expired.
{% endif %}
```

### Operators

| Operator | Description | Example |
|-|-|-|
| `=` | Assignment | `{% set x = 0 %}` |
| `==` | Equals | `{% if this == that %}` |
| `!=` | Not equals | `{% if this != that %}` |
| `<` | Less than | `{% if a < b %}` |
| `<=` | Less than or equal | `{% if a <= b %}` |
| `>` | Greater than | `{% if a > b %}` |
| `>=` | Greater than or equal | `{% if a >= b %}` |
| `~` | String concatenation  | `{{a ~ b}}` |
| `in` | Value in list | `{% if 'red' in colors %}` |
| `not in` | Value not in list | `{% if 'orange' not in colors %}` |
| `starts with` | String prefix test | `{% if url starts with 'https://' %}` |
| `ends with` | String suffix test | `{% if name ends with '.txt' %}` |
| `matches` | Regex match | `{% if value matches '/^\\d+$/' %}` |
| `is` | Test operator | `{% if x is empty %}` |
| `is not` | Negated test | `{% if x is not null %}` |
| `? :` | Ternary | `{{x > 0 ? 'yes' : 'no'}}` |
| `??` | Null coalescing | `{{x ?? 'default'}}` |
| `and` | Logical AND | `{% if a and b %}` |
| `or` | Logical OR | `{% if a or b %}` |
| `not` | Logical NOT | `{% if not a %}` |
| `+` `-` `*` `/` `%` `**` | Arithmetic | `{{a + b}}`, `{{2 ** 10}}` |

### Loops

**For loops:**
```
{% set names = ["Jeff", "Dan", "Darren"] %}
{% for name in names %}
* {{name}}
{% endfor %}
```

**Key-value iteration:**
```
{% for key, value in object %}
{{key}}: {{value}}
{% endfor %}
```

**Range loops:**
```
{% for n in 1..5 %}
{{n}}...
{% endfor %}
```

**Loop variable scope:** Variables defined inside a loop are not accessible outside. Define them before the loop to persist changes.

**Loop special variables:**
- `loop.index` — current iteration (1-indexed)
- `loop.index0` — current iteration (0-indexed)
- `loop.first` — true on first iteration
- `loop.last` — true on last iteration
- `loop.length` — total iterations

### Regular Expressions

```
{% set text = "Your Amazon Order #Z-1234-5678-9 has shipped!" %}
{% set order_id = text|regexp("/Amazon Order #([A-Z0-9\\-]+)/", 1) %}
Amazon Order #: {{order_id}}
```

**Match all occurrences:**
```
{% set matches = regexp_match_all("/pattern/", string, group) %}
```

### JSON

**Decoding:**
```
{% set obj = json_decode(json_string) %}
{{obj.name}}
```

**Encoding:**
```
{{data|json_encode}}
{{data|json_encode|json_pretty}}
```

**Modification with `dict_set()`:**
```
{% set json = dict_set(json, 'status.text', 'shipped') %}
```

### XML

| Function | Description |
|-|-|
| `xml_decode(string)` | Parse XML string to object |
| `xml_encode(object)` | Encode object as XML |
| `xml_xpath(xml, path)` | Extract values with XPath |
| `xml_xpath_ns(xml, prefix, uri)` | Define XML namespace for XPath |
| `xml_xpath_remove(xml, path)` | Remove elements by XPath |
| `xml_attr(node, attr)` | Get single attribute from node |
| `xml_attrs(node)` | Get all attributes from node |

### Template Commands

| Command | Syntax | Description |
|-|-|-|
| `apply` | `{% apply upper %}...{% endapply %}` | Transform enclosed text with filter |
| `do` | `{% do expression %}` | Evaluate expression without output  |
| `for` | `{% for x in list %}...{% endfor %}` | Iterate array elements |
| `if` | `{% if cond %}...{% elseif %}...{% else %}...{% endif %}` | Conditional logic |
| `set` | `{% set name = "value" %}` | Create template variable |
| `spaceless` | `{% spaceless %}...{% endspaceless %}` | Remove whitespace between HTML tags |
| `verbatim`  | `{% verbatim %}...{% endverbatim %}` | Prevent template syntax parsing |
| `with` | `{% with %}...{% endwith %}` | Create isolated variable scope |

### Tests

Tests use `is` / `is not` operators and return boolean values:

| Test | Description | Example |
|-|-|-|
| `empty` | Empty string, array, object, false, or null | `{% if "" is empty %}` |
| `even` | Number is even | `{{2 is even ? 'even' : 'odd'}}` |
| `iterable` | Is array or iterable object | `{{items is iterable}}` |
| `null` | Equals null | `{{x is null}}` |
| `numeric` | Is numeric value | `{{123 is numeric}}` |
| `odd` | Number is odd | `{{1 is odd}}` |
| `pattern` | Matches wildcard pattern(s) | `{{email is pattern ("support@*")}}` |
| `prefixed` | Starts with string(s) | `{{subject is prefixed ("[Bugs]")}}` |
| `suffixed` | Ends with string(s) | `{{domain is suffixed (".ai", ".com")}}` |
| `record type` | Matches record type(s) | `{{ctx is record type ('task','ticket')}}` |
| `same as` | Same type and value (no coercion) | `{{a is same as b}}` |

---

## Functions Reference

### Array Functions

| Function | Signature | Description |
|-|-|-|
| `array_column` | `array_column(array, column_key)` | Extract a column from array elements |
| `array_combine` | `array_combine(keys, values)` | Create array from parallel keys and values arrays |
| `array_count_values` | `array_count_values(array)` | Return distinct values as keys with occurrence counts |
| `array_diff` | `array_diff(array2, array1)` | Items in array2 not present in array1 |
| `array_extract_keys` | `array_extract_keys(records, keys)` | Return specified keys from each element |
| `array_fill_keys` | `array_fill_keys(keys, value)` | Create array with given keys all set to default value |
| `array_intersect` | `array_intersect(array2, array1)` | Elements in both arrays |
| `array_matches` | `array_matches(values, patterns)` | Compare values to wildcard patterns |
| `array_sort_keys` | `array_sort_keys(array)` | Sort associative array by keys |
| `array_unique` | `array_unique(array)` | Return only distinct values |
| `array_values` | `array_values(array)` | Return values as new indexed array |

### Dictionary Functions

| Function | Signature | Description |
|-|-|-|
| `dict_set` | `dict_set(object, path, value, delimiter)` | Set value at dot-notation path. Use `.[]` to append to arrays. Default delimiter is `.` |
| `dict_unset` | `dict_unset(object, keys_array)` | Remove items by key paths |

### Math Functions

| Function | Signature | Description |
|-|-|-|
| `clamp_float` | `clamp_float(value, min, max)` | Clamp decimal to range |
| `clamp_int` | `clamp_int(value, min, max)` | Clamp integer to range |
| `max` | `max(array_or_object)` | Return largest value |
| `min` | `min(array_or_object)` | Return smallest value  |

### Date/Time Functions

| Function | Signature | Description |
|-|-|-|
| `date` | `date(date_string)` | Create date object for use with `date_modify` |
| `date_lerp` | `date_lerp(range, unit, step, limit)` | Interpolate timestamps between two dates. Units: minute, hour, day, week, month, year |

### String/Utility Functions

| Function | Signature | Description |
|-|-|-|
| `random` | `random(input)` | Random item from array/string, or random number 0..n |
| `random_string` | `random_string(length)` | Generate random alphanumeric string |
| `range` | `range(from, to, step)` | Array of values in range (inclusive) |
| `shuffle` | `shuffle(array)` | Randomize array order |
| `cycle` | `cycle(options, position)` | Round-robin through a sequence |
| `attribute` | `attribute(object, key)` | Access object values with a variable key |
| `regexp_match_all` | `regexp_match_all(pattern, string, group)` | Match all occurrences against regex |

### Validation Functions

| Function | Signature | Description |
|-|-|-|
| `validate_email`  | `validate_email(email)`  | Validate email address (returns boolean) |
| `validate_number` | `validate_number(value)` | Validate number (returns boolean) |

### DNS Functions

| Function | Signature | Description |
|-|-|-|
| `dns_get_record` | `dns_get_record(hostname, type)` | Resolve DNS records. Types: a, aaaa, caa, cname, mx, ns, ptr, soa, srv, txt |
| `dns_host_by_ip` | `dns_host_by_ip(ip)` | Reverse DNS lookup |

### JSON Functions

| Function | Signature | Description |
|-|-|-|
| `json_decode`  | `json_decode(json_string)` | Decode JSON string to object |
| `jsonpath_set` | `jsonpath_set(json, path, value)` | Like dict_set; `path[]` appends to arrays |

### KATA/XML/Parsing Functions

| Function | Signature | Description |
|-|-|-|
| `kata_parse` | `kata_parse(text)` | Parse KATA text block into object |
| `vobject_parse` | `vobject_parse(text)` | Parse VObject format (vCard, iCal) |
| `xml_decode` | `xml_decode(xml_string, namespaces, mode)` | Decode XML string; mode `html` for HTML DOM |
| `xml_encode` | `xml_encode(xml_object)` | Encode object as XML |
| `xml_xpath` | `xml_xpath(xml, path)` | Extract values with XPath |
| `xml_xpath_ns` | `xml_xpath_ns(xml, prefix, uri)` | Define XML namespace |
| `xml_xpath_remove` | `xml_xpath_remove(xml, path)` | Remove elements by XPath |
| `xml_attr` | `xml_attr(node, attr)` | Return single attribute from XML node |
| `xml_attrs` | `xml_attrs(node)` | Return all attributes from XML node |

### Cerb-Specific Functions

| Function | Signature | Description |
|-|-|-|
| `cerb_automation` | `cerb_automation(uri, inputs)` | Invoke a `scripting.function` automation |
| `cerb_avatar_image` | `cerb_avatar_image(record_type, id, updated)` | Get avatar image HTML tag |
| `cerb_avatar_url` | `cerb_avatar_url(record_type, id, updated)` | Get avatar image URL |
| `cerb_calendar_get_relative_date` | `cerb_calendar_get_relative_date(calendar, rel_date, now)` | Calculate future timestamp using calendar availability |
| `cerb_calendar_time_elapsed` | `cerb_calendar_time_elapsed(calendar, date_from, date_to)` | Calculate elapsed time between dates using calendar availability (seconds) |
| `cerb_current_worker` | `cerb_current_worker(expand)` | Return dictionary for currently logged in worker |
| `cerb_extract_uris` | `cerb_extract_uris(html)` | Return array of URLs found in HTML with metadata |
| `cerb_file_url` | `cerb_file_url(id)` | Get download link for attachment ID |
| `cerb_has_priv` | `cerb_has_priv(privilege, actor_type, actor_id)` | Check if actor has privilege |
| `cerb_placeholders_list` | `cerb_placeholders_list(extract, prefix)` | Return all placeholders in current behavior. `extract` is the key prefix to expand; `prefix` is stripped from the returned keys. Use `{% do extract_ %}` before calling to force lazy expansion of nested keys. Example: `{% do draft_ticket_ %}` then `cerb_placeholders_list('draft_ticket_', '')` returns `{mask: ..., subject: ...}` so snippet templates can use `{{mask}}`, `{{subject}}` directly. |
| `cerb_plugin_enabled` | `cerb_plugin_enabled(plugin_id)` | Test if plugin is installed and enabled |
| `cerb_record_readable` | `cerb_record_readable(record_type, record_id, actor_type, actor_id)`  | Check read access |
| `cerb_record_writeable` | `cerb_record_writeable(record_type, record_id, actor_type, actor_id)` | Check write access |
| `cerb_url` | `cerb_url(path)` | Get full URL to page/resource |
| `cerb_workflow_config` | `cerb_workflow_config(name_or_id, key, default)` | Runtime configuration lookups from workflows |
| `cerb_workflow_resources` | `cerb_workflow_resources(name_or_id)` | Return map of workflow resources and local record IDs |

---

## Filters Reference

Filters transform values using the pipe (`|`) character: `{{value|filter_name(args)}}`.

### String Filters

| Filter | Signature | Description |
|-|-|-|
| `alphanum` | `\|alphanum(allowed_chars)` | Strip non-alphanumeric chars; optionally keep specified chars |
| `append` | `\|append(suffix, delimiter, trim)` | Append text with optional delimiter |
| `capitalize` | `\|capitalize` | Capitalize first character, lowercase rest |
| `convert_encoding` | `\|convert_encoding(target, source)` | Convert character encodings |
| `escape` / `e` | `\|escape(mode)` | Escape for: html, js, css, url, html_attr |
| `indent` | `\|indent(marker, start_line)` | Prefix each line with marker |
| `lower` | `\|lower` | Convert to lowercase |
| `nl2br` | `\|nl2br` | Newlines to `<br />` tags |
| `permalink` | `\|permalink` | Convert text to URL-friendly format |
| `quote` | `\|quote` | Quote text with `>` prefix |
| `repeat` | `\|repeat(times)` | Repeat string n times |
| `replace` | `\|replace({"old": "new"})` | Replace values using key-value map |
| `reverse` | `\|reverse(preserve_keys)` | Reverse string or array |
| `str_pos` | `\|str_pos(needle, offset, ignoreCase)` | Find substring position (-1 if not found) |
| `str_sub` | `\|str_sub(from, to)` | Extract substring by positions |
| `striptags` | `\|striptags` | Remove HTML tags |
| `title` | `\|title` | Capitalize first letter of each word |
| `trim` | `\|trim(character_mask, side)` | Remove whitespace; side: both, left, right |
| `truncate` | `\|truncate(limit)` | Limit string length with ellipsis |
| `unescape` | `\|unescape` | Decode HTML entities |
| `upper` | `\|upper` | Convert to uppercase |
| `strip_lines` | `\|strip_lines(prefixes)` | Remove lines starting with prefix |
| `tokenize` | `\|tokenize` | Extract word tokens ignoring punctuation |

### Number Filters

| Filter | Signature | Description |
|-|-|-|
| `abs` | `\|abs` | Absolute value |
| `bytes_pretty`  | `\|bytes_pretty(precision)` | Human-readable byte sizes (e.g., "123.46 MB") |
| `number_format` | `\|number_format(decimals, dec_sep, thousands_sep)` | Format numbers with separators |
| `round` | `\|round(precision, method)` | Round; method: common, ceil, floor |
| `secs_pretty` | `\|secs_pretty` | Seconds to human-readable duration |
| `base_convert`  | `\|base_convert(from_base, to_base)` | Convert between number bases |

### Array/Collection Filters

| Filter | Signature | Description |
|-|-|-|
| `array_sum`  | `\|array_sum` | Sum numeric elements |
| `batch` | `\|batch(size, padding)` | Break list into smaller chunks |
| `column` | `\|column(key)` | Extract key from each array element |
| `filter` | `\|filter((v,k) => condition)` | Filter array with arrow function |
| `first` | `\|first` | First element |
| `join` | `\|join(delimiter)` | Join array elements with delimiter |
| `keys` | `\|keys` | Return array/object keys |
| `last` | `\|last` | Last element |
| `length` | `\|length` | Length of string or array |
| `map` | `\|map((v,k) => expr)` | Transform each item |
| `merge` | `\|merge(array_or_object)` | Combine two arrays/objects |
| `reduce` | `\|reduce((carry,v) => expr, initial)`  | Reduce array to single value |
| `slice` | `\|slice(start, length, preserve_keys)` | Extract portion of string/array |
| `sort` | `\|sort(comparator)` | Sort; optional `(a,b) => a.field <=> b.field` |
| `split` | `\|split(delimiter, limit)` | String to array |
| `split_crlf` | `\|split_crlf(keep_blanks, trim_lines)` | Split on CR/LF |
| `split_csv`  | `\|split_csv` | Split on commas |
| `stat` | `\|stat(measure, decimals)` | Statistics: count, max, mean, median, min, mode, sum, stdevp, stdevs, varp, vars |
| `values` | `\|values` | Return values with sequential keys |

### Date Filters

| Filter | Signature | Description |
|-|-|-|
| `date` | `\|date(format, timezone)` | Format dates (PHP DateTime format) |
| `date_modify` | `\|date_modify(modification)` | Modify date objects (e.g., "+2 days") |
| `date_pretty` | `\|date_pretty` | Relative human-readable dates (e.g., "18 years ago") |

### Encoding Filters

| Filter | Signature | Description |
|-|-|-|
| `base64_decode` | `\|base64_decode` | Decode base64 |
| `base64_encode` | `\|base64_encode` | Encode as base64 |
| `base64url_decode` | `\|base64url_decode` | Decode base64url |
| `base64url_encode` | `\|base64url_encode` | Encode as base64url |
| `csv` | `\|csv` | Format arrays as CSV |
| `html_to_text` | `\|html_to_text(truncate)` | Convert HTML to plain text; default truncate 50000 bytes |
| `json_encode` | `\|json_encode` | Encode as JSON string |
| `json_pretty` | `\|json_pretty` | Pretty-print JSON with indentation |
| `kata_encode` | `\|kata_encode` | Emit objects/arrays as KATA text |
| `markdown_to_html` | `\|markdown_to_html` | Convert Markdown to HTML |
| `url_decode` | `\|url_decode(format)` | Decode URL query strings; format "json" for object |
| `url_encode` | `\|url_encode` | Encode as URL query string |
| `qp_decode` | `\|qp_decode` | Decode quoted-printable |
| `qp_encode` | `\|qp_encode` | Encode as quoted-printable |

### Hash/Crypto Filters

| Filter | Signature | Description |
|-|-|-|
| `hash` | `\|hash(algorithm, binary)` | Cryptographic hash. Algorithms: crc32, md5, murmur3a/c/f, sha1, sha256, sha512, sha3-224/256/384/512, whirlpool, xxh32/64/3/128 |
| `hash_hmac` | `\|hash_hmac(secret_key, algorithm, binary)` | HMAC with secret key |
| `md5` | `\|md5` | MD5 hash (shorthand) |
| `sha1` | `\|sha1` | SHA-1 hash (shorthand) |

### Parsing Filters

| Filter | Signature | Description |
|-|-|-|
| `parse_csv` | `\|parse_csv(separator, enclosure, escape)` | Parse CSV to arrays |
| `parse_emails` | `\|parse_emails` | Parse email addresses with validation |
| `parse_url` | `\|parse_url` | Parse URL into components (scheme, host, path, query, fragment) |
| `parse_user_agent` | `\|parse_user_agent` | Parse user-agent strings (platform, browser, version) |
| `regexp` | `\|regexp(pattern, group)` | Extract regex pattern match |
| `image_info` | `\|image_info()` | Extract image metadata (width, height, channels, bits, type) |

### Other Filters

| Filter | Signature | Description |
|-|-|-|
| `cerb_translate` | `\|cerb_translate` | Convert string IDs to localized text |
| `context_name` | `\|context_name(type)` | Convert context IDs to labels; type: singular, plural, id, uri |
| `default` | `\|default(fallback)`  | Default value for empty variables |
| `format` | `\|format(args...)` | sprintf-style string formatting |

---

## Dialects

KATA has several dialects that share the same syntax but have different vocabularies:

| Dialect | Used For |
|-|-|
| **Automations** | Declarative commands for workflow logic (`start:`, `set:`, `return:`, `decision:`, etc.) |
| **Maps** | Geographic map configurations |
| **Toolbars** | UI toolbar definitions |
| **Events** | Event handler configurations |
| **Sheets** | Data display schemas |

Each dialect defines its own set of valid keys and their meanings, but all follow the same KATA syntax rules for indentation, annotations, comments, references, and scripting.
