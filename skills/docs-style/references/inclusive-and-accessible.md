# Inclusive and accessible writing

This reference covers terminology, pronouns, and the practices that make documentation usable with screen readers and translation.

## Terminology

Use precise, neutral terms that describe the technical relationship or action.

| Context | Preferred terms |
| :--- | :--- |
| Access control and filtering | `allowlist`, `denylist`, allow, block |
| Replication, clusters, and workers | `primary` / `replica`, `main` / `worker`, `leader` / `follower` |
| Version control | `main branch`, `default branch` |
| Testing | `smoke test`, `preflight check`, `validation` |
| Examples and tests | `sample value`, `placeholder`, `test fixture` |
| Billing and feature access | `legacy`, `exempt` |
| Feature descriptions | `built-in`, `integrated` |
| Estimates | `person-hours`, `engineering time` |
| Addressing readers | `everyone`, `team`, `developers` |
| Documentation gaps | `institutional knowledge` |
| Software impact | `disable`, `degrade`, `limit` |

When an external tool, API, or protocol supplies an exact identifier, preserve it in code font and use the preferred project term in surrounding prose.

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

- Give an informative image concise alt text that states its purpose and, for diagrams, what it conveys: `alt="Request flow from the client through the API gateway to the auth and billing services."`
- Give a decorative image or a visual repetition of nearby text an empty alt attribute: `alt=""`.
- Put any instruction that appears inside an image into the body text as well.
- Use screenshots for orientation, and carry the actual steps in the numbered list.

## Tables and color

- Include a header row so that screen readers can announce column names.
- Fill every cell.
- Carry meaning in text as well as color: mark required parameters with a **Required** column or the word "Required".

## Reading and interaction

- Provide a keyboard-accessible route through an interactive task.
- Refer to controls by label, accessible name, tooltip, or stable surrounding context.
- Use reading-order references such as "the following table" and "the preceding diagram".
- Put the distinguishing information in the first sentence of a paragraph.

## Words about people and abilities

Describe what a person does or needs: "people who use screen readers", "readers who are new to Kubernetes". Use literal words for software behavior: *stops*, *fails*, *ignores*, *blocks*.
