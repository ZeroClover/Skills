# Inclusive and accessible writing

This reference covers terminology, pronouns, and the practices that make documentation usable with screen readers and translation.

## Terminology

Use precise, neutral terms. The table lists the recommended term first and the term it replaces, for use when you review existing text.

| Use | In place of | Context |
| :--- | :--- | :--- |
| `allowlist`, `denylist` | `whitelist`, `blacklist` | Access control, filtering |
| `primary` / `replica`, `main` / `worker`, `leader` / `follower` | `master` / `slave` | Replication, clusters, CI runners |
| `main branch`, `default branch` | `master branch` | Version control |
| `smoke test`, `preflight check`, `validation` | `sanity check` | Testing |
| `sample value`, `placeholder`, `test fixture` | `dummy value` | Examples and tests |
| `legacy`, `exempt` | `grandfathered` | Billing and feature access |
| `built-in`, `integrated` | `native` (as in "native support") | Feature descriptions |
| `person-hours`, `engineering time` | `man-hours` | Estimates |
| `everyone`, `team`, `developers` | `guys` | Addressing readers |
| `institutional knowledge` | `tribal knowledge` | Documentation gaps |
| `disable`, `degrade`, `limit` | `cripple` | Impact descriptions |

When an external tool, API, or protocol uses one of the replaced terms as an identifier, quote the identifier in code font (`git checkout master`) and use the neutral term in your own sentences.

## Pronouns

- Use singular *they*, *them*, and *their* for a person of unspecified gender: "When an admin signs in, they see the dashboard."
- Address the reader as *you* wherever the sentence is about the reader, which removes most third-person pronouns.
- Use the pronouns a named real person uses.

## Link text

Write link text that names the destination, so that it makes sense when a screen reader lists links out of context:

- "Download the SDK from the [Cloud SDK downloads page](https://example.com/sdk)."
- "For details, see [Authorize with OAuth 2.0](https://example.com/oauth)."
- "The [API reference](https://example.com/api) lists every endpoint."

Put the link on the noun phrase that names the target, and keep the sentence readable with the link removed.

## Images

- Give every image alt text that states what the image shows and, for diagrams, what it conveys: `alt="Request flow from the client through the API gateway to the auth and billing services."`
- Put any instruction that appears inside an image into the body text as well.
- Use screenshots for orientation, and carry the actual steps in the numbered list.

## Tables and color

- Include a header row so that screen readers can announce column names.
- Fill every cell.
- Carry meaning in text as well as color: mark required parameters with a **Required** column or the word "Required".

## Words about people and abilities

Describe what a person does or needs: "people who use screen readers", "readers who are new to Kubernetes". Use literal words for software behavior: *stops*, *fails*, *ignores*, *blocks*.
