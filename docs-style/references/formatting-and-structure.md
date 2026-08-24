# Formatting and structure

This reference covers headings, lists, procedures, tables, notices, numbers, dates, paragraphs, and cross-references.

## Headings

- Use sentence case: capitalize the first word and proper nouns. "Get started with Cloud Functions", "Manage user permissions and roles", "Advanced configuration options".
- Start task headings with a bare infinitive: "Create an instance", "Install the CLI". Use noun phrases for conceptual sections: "Authentication lifecycle".
- Keep headings short and free of end punctuation. A heading that needs a colon or a question mark usually wants rewording.
- Use one H1 per page, and descend one level at a time (`#`, `##`, `###`).
- Make each heading meaningful on its own, because readers scan tables of contents and search results.

## Lists

- Use a numbered list for steps that happen in order.
- Use a bulleted list for items whose order carries no meaning: options, features, prerequisites.
- Use a table for term-and-definition pairs, parameters, and error codes.
- Introduce a list with a sentence. End that sentence with a colon when the list follows immediately: "The service supports the following protocols:".
- Keep items parallel: all imperative verbs, all noun phrases, or all complete sentences.
- Capitalize the first word of each item. End an item with a period when it's a complete sentence, and leave fragments without end punctuation. Keep one style within a list.

Parallel imperative items:

```markdown
To configure your local environment:

1. Download and install the CLI binary.
2. Export your API token to the `AUTH_TOKEN` environment variable.
3. Verify the installation by running `mycli version`.
```

Parallel fragments:

```markdown
The service supports the following protocols:

- HTTP/2 and HTTP/3
- gRPC over TLS
- WebSocket streaming
```

## Procedures

A procedure gives the steps for one task.

1. State prerequisites before the first step: permissions, tools, versions.
2. Open with one sentence that names the goal: "To create a storage bucket:".
3. Give one action per step. Combine small sequential clicks in one step with a menu path: "Click **File > New > Document**."
4. State the location or condition, then the action: "In the **Bucket name** field, enter a globally unique name."
5. Put the result in the same paragraph as the action, after the action: "Click **Create**. The console opens the **Bucket details** page."
6. Mark optional steps with the word *Optional* and a colon: "Optional: Enter a description."
7. Label sub-steps with lowercase letters (a, b, c) and sub-sub-steps with lowercase Roman numerals.
8. Format a single-step procedure as one bulleted item.
9. When another page already documents a set of steps, link to it.

```markdown
### Create a storage bucket

To create a bucket:

1. In the Google Cloud console, go to the **Buckets** page.
2. Click **Create bucket**.
3. In the **Bucket name** field, enter a globally unique name.
4. In the **Location type** section, select **Region**.
5. Click **Create**. The console creates the bucket and opens the **Bucket details** page.
```

## Tables

- Include a header row, and write column headers in sentence case.
- Fill every cell; write `None` or `N/A` where a value is absent.
- Left-align text and right-align numbers.
- Introduce the table with a sentence that says what it lists: "The following table describes the request parameters:".

```markdown
| Parameter | Type | Default | Description |
| :--- | :--- | ---: | :--- |
| `timeout_ms` | integer | `5000` | Connection timeout in milliseconds. |
| `enable_ssl` | boolean | `true` | Enables TLS for all endpoints. |
| `retry_count` | integer | `3` | Maximum number of retry attempts. |
```

## Notices

Use notices for information that stands apart from the main flow, and use them rarely so that each one keeps its weight.

| Type | Use for |
| :--- | :--- |
| Note | Background, tips, related information |
| Caution | Actions that risk data loss, cost, or security exposure |
| Warning | Severe or irreversible consequences |

Keep required steps in the numbered procedure: a notice holds context, and the procedure holds actions. Keep each notice to one short paragraph.

```markdown
> [!NOTE]
> Bucket names are visible to anyone who requests the bucket's URL.

> [!CAUTION]
> Deleting a bucket also deletes every object in it.
```

## Numbers and units

- Spell out zero through nine in running text, and use numerals from 10 upward: "three authentication methods", "up to 25 records".
- Use numerals with units, percentages, versions, step references, and in tables: "5 MB", "99.9%", "version 2", "step 1".
- Spell out a number that starts a sentence, or reword so that the numeral falls later: "The system launched 12 instances."
- Put a space between a number and its unit: `10 MB`, `500 ms`, `2.4 GHz`. Write percentages without a space: `99.9%`.
- Express ranges with *to* or *through* in prose: "from 3 to 10 retries". Use a hyphen in tables and compact labels: `3-10`.

## Dates and times

- Write dates with the month spelled out, or in ISO 8601 form: "August 25, 2026" or `2026-08-25`.
- Include the time zone with a time: "14:30 UTC", "2:30 PM PDT".

## Paragraphs

- Lead with the point of the paragraph, then support it.
- Keep paragraphs to a few sentences, with one topic per paragraph.
- Break up dense text with lists, tables, code blocks, or figures when the content has that shape.

## Cross-references

- Point to other content with a sentence that names it: "For more information, see [Configure access control](https://example.com/docs/access-control)."
- Refer to content on the same page by reading order: "the following table", "the preceding example".
- Refer to a section by its heading text, and link it when the section lives on another page.
