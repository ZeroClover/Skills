# Word list and punctuation

This reference gives the preferred spelling, usage, and punctuation for terms that come up often in developer documentation.

## Word choices

| Use | When | Example |
| :--- | :--- | :--- |
| `sign in`, `sign out` (verb) | The reader authenticates | Sign in to the console. |
| `sign-in` (adjective), `login` (noun) | Naming the page or the credentials | Enter your login credentials on the sign-in page. |
| `can` | Ability, permission, or an optional action | You can export the report as CSV. |
| `might` | Possibility or an uncertain outcome | The build might take several minutes. |
| `may` | Official policy or legal permission | You may use this software under the Apache 2.0 license. |
| `must` | A requirement | The name must start with a letter. |
| `enable`, `turn on` | Activating a feature | Turn on two-factor authentication. |
| `lets` | A feature that gives the reader an ability | The flag lets you skip the cache. |
| `allows` | Permission granted to a person or role | The IAM policy allows editors to deploy. |
| `after` | A sequence in time | After the build completes, run the tests. |
| `because` | A cause | The request fails because the token has expired. |
| `although` | A concession | Although the API accepts both formats, JSON parses faster. |
| `for example`, `such as` | Introducing examples | Use a reserved domain, such as `example.com`. |
| `that is` | Restating | Choose the nearest region, that is, the one with the lowest latency. |
| `by using`, `with`, `through` | Means | Authenticate by using a service account. |
| `versus` | Comparing in prose | Strong consistency versus eventual consistency. |
| `cannot` | Inability, as one word | The function cannot return `null`. |

The words `once`, `since`, and `while` each carry a time-related meaning as well as a logical one, so the table's choices (`after`, `because`, `although`) read unambiguously.

## Spelling and word forms

| Verb (two words) | Noun or adjective (one word) |
| :--- | :--- |
| set up | setup |
| back up | backup |
| sign in | sign-in (adjective), login (noun) |
| plug in | plugin (noun), plug-in (adjective) |
| shut down | shutdown |
| time out | timeout |
| check out | checkout |

- One-word forms: `filename`, `codebase`, `runtime`, `metadata`, `lifecycle`, `website`, `username`, `dataset`, `toolchain`.
- Two-word forms: `data center`, `web page`, `web server`, `command line` (noun), `open source` (noun), `real time` (noun).
- Hyphenated adjectives before a noun: `command-line tool`, `open-source library`, `real-time analytics`, `third-party integration`, `read-only replica`, `built-in authentication`.
- Uppercase acronyms and initialisms: `API`, `CLI`, `SDK`, `URL`, `URI`, `JSON`, `YAML`, `SQL`, `REST`, `ID`, `IP address`, `API key`.
- American English spelling: `color`, `behavior`, `initialize`, `canceled`.
- For lists and menus, write `list` or `menu`; the qualifier `drop-down` can usually be omitted: "From the **Region** list, select **us-central1**."

Spell out an abbreviation the first time it appears on a page, with the abbreviation in parentheses: "Identity and Access Management (IAM)". Widely known abbreviations such as API, URL, and HTTP need no expansion.

Use the product's exact UI label or command terminology where it differs from the general word choice. For example, a tool whose interface says **Log in** keeps that label in its procedure.

## Punctuation

### Serial comma

Put a comma before the conjunction in a series of three or more: "The SDK supports Node.js, Go, and Python."

### Periods and sentence breaks

Write one idea per sentence and end it with a period. Where a draft joins two independent clauses with a semicolon, two sentences read better: "The client starts a handshake. The server returns a signed certificate."

### Colons

Use a colon after a complete sentence to introduce a list, table, or code block: "The API supports the following formats: JSON, XML, and YAML." Where the introductory words form an incomplete sentence, continue without a colon: "The supported formats are JSON, XML, and YAML."

### Quotation marks

- Put periods and commas inside closing quotation marks in ordinary prose: See the section titled "Configure the client."
- Put punctuation outside the quotation marks when the quoted text is a literal string the reader enters or sees: If you enter "escape", the program exits.
- Prefer code font to quotation marks for literal strings: If you enter `escape`, the program exits.
- Use straight quotation marks in code.

### Slashes

Write out the relationship the slash stands for: "input and output", "A, B, or both". Keep the slash in established terms such as `I/O` and `TCP/IP`, and in file paths.

### Dashes and hyphens

- Use an em dash (—) with no surrounding spaces to set off an aside: "The configuration file—`/etc/app.conf`—must be readable."
- Express ranges with *to* or *through* in prose: "3 to 10 retries". Use a hyphen in tables and labels: `3-10`.
- Reserve `--` for command-line flags.
- Hyphenate compound modifiers before a noun, as listed under Spelling and word forms.

### Parentheses and emphasis

- Keep parenthetical asides short, and move a long aside into its own sentence.
- Use italics for emphasis sparingly, and reserve bold for UI labels.
