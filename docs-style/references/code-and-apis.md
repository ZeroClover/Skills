# Code and APIs

This reference covers code in text, code blocks, command lines, placeholders, example values, and reference descriptions.

## Code in text

Use inline code font for anything the reader types, reads from a screen, or finds in source code:

| Category | Examples |
| :--- | :--- |
| Keywords and types | `const`, `async`, `boolean`, `int64` |
| Functions and methods | `getUserById()`, `JSON.stringify()` |
| Variables, fields, and keys | `userId`, `timeout_seconds`, `content-type` |
| Classes and interfaces | `HttpClient`, `EventEmitter` |
| Filenames, extensions, and paths | `package.json`, `.env`, `/etc/nginx/nginx.conf`, `src/controllers/` |
| Commands and flags | `git commit`, `npm install`, `--verbose`, `-p 8080` |
| HTTP methods and status codes | `GET`, `POST`, `200 OK`, `404 Not Found` |
| Environment variables | `PORT`, `DATABASE_URL` |
| Literal values and string inputs | `true`, `us-central1`, `application/json` |

Write product names, protocol names, and language names in regular text with their standard capitalization: Docker, Kubernetes, PostgreSQL, HTTP, gRPC, TLS, Python. Write UI labels in bold (see `ui-and-interaction.md`).

## Code blocks

- Give every fenced block a language identifier: ```` ```python ````, ```` ```bash ````, ```` ```json ````.
- Make samples complete enough to run: include imports, and show the values a reader needs.
- Introduce the block with a sentence that says what it does or where it goes: "Add the following to `server.js`:".
- Comment the reasoning behind a line where the reasoning is the point; the code itself shows what it does.
- Follow the language's published style guide, such as PEP 8 or Effective Go.

```typescript
import { Storage } from '@google-cloud/storage';

const storage = new Storage();

/**
 * Downloads an object from Cloud Storage to the local filesystem.
 *
 * @param bucketName The source bucket.
 * @param objectName The object path within the bucket.
 * @param destination The local path to write to.
 */
async function downloadObject(bucketName: string, objectName: string, destination: string): Promise<void> {
  await storage.bucket(bucketName).file(objectName).download({ destination });
  console.log(`Downloaded gs://${bucketName}/${objectName} to ${destination}`);
}
```

## Command lines

- Show a command the reader will copy without a shell prompt, so that it pastes cleanly.
- Show command output in a separate block, introduced by a sentence.
- Break long commands with a backslash and indent continuation lines.

Start the container:

```bash
docker run -d \
  --name web-server \
  -p 8080:80 \
  nginx:alpine
```

The command prints the container ID:

```text
3f4e1c9a7b2d
```

## Placeholders

- Write placeholders in uppercase with underscores: `PROJECT_ID`, `BUCKET_NAME`, `API_KEY`.
- Name the thing itself; `API_KEY` says as much as a longer possessive form.
- Keep placeholders in code font, both in code blocks and in prose.
- Explain placeholders directly after the sample. For one placeholder: "Replace `PROJECT_ID` with your project ID." For several, list them in order of appearance:

```bash
curl -X POST https://api.example.com/v2/projects/PROJECT_ID/deploy \
  -H "Authorization: Bearer API_KEY" \
  -d '{"environment": "ENVIRONMENT_NAME"}'
```

Replace the following:

- `PROJECT_ID`: your project identifier
- `API_KEY`: an access token generated in the console
- `ENVIRONMENT_NAME`: the target environment, such as `staging` or `production`

## Example values

Use reserved names and addresses, so that examples stay harmless if a reader runs them as written:

| Category | Use |
| :--- | :--- |
| Domains | `example.com`, `example.org`, `example.net` (RFC 2606) |
| IPv4 addresses | `192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24` (RFC 5737) |
| IPv6 addresses | `2001:db8::/32` (RFC 3849) |
| Email addresses | `alex@example.com` |
| Phone numbers | `+1-555-0100` through `+1-555-0199` |
| People | Short fictional names from varied backgrounds: Alex, Priya, Kenji, Amara |
| IDs and keys | Visibly synthetic values: `cust_0000001`, `sk_test_000000` |

## Reference descriptions

For method, function, and endpoint descriptions:

- Open with a third-person present-tense verb that says what the call does: "Returns the authenticated user's profile." "Adds an item to the cart and returns its ID."
- Describe parameters as noun phrases that start with *The* or *A*: "The bucket to read from." For booleans: "If `true`, retries the request. If `false`, returns the error."
- Describe return values as noun phrases: "The customer record." For booleans: "`true` if the token is valid; `false` otherwise."
- State defaults explicitly: "Default: `30`."

A complete reference entry has a summary sentence, a parameters table, a request example, a response example, and an error table. See `assets/api-reference.md` for the layout.
