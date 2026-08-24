# Voice and tone

The Google developer documentation voice sounds like a knowledgeable friend: conversational, direct, and respectful of the reader's time. This reference covers person, voice, tense, sentence order, and tone.

## Write to the reader as "you"

Address the reader directly and give instructions in the imperative.

- "You can view your billing history on the **Billing** page."
- "Set up the database connection."

Reserve "we" for an explicit recommendation from the documentation team: "We recommend OAuth 2.0 for server-to-server calls."

When a sentence describes a role other than the reader, name the role and use singular *they*: "When an administrator approves the request, they receive a confirmation email."

## Use active voice

Make the actor the subject of the sentence. The actor is usually the reader, the product, or a component of the product.

| Context | Sentence |
| :--- | :--- |
| Instruction | Edit the configuration file. |
| System behavior | The gateway rejects requests that carry an expired token. |
| API output | The API returns a JSON object that contains user metadata. |
| UI action | Click **Deploy**. |

To find the actor in a draft sentence, ask "who or what does this?" and move that answer to the front. The passive form fits when the actor is unknown or unimportant: "The certificate was issued in 2019."

## Use present tense

Describe what the software does now.

- "This function validates the payload."
- "Running the script generates a certificate."
- "If the token has expired, the server returns `401 Unauthorized`."

Use "will" for an event that happens later relative to the reader's action: "After you submit the form, you'll receive an email within 24 hours."

## Put conditions before actions

State the location, prerequisite, or goal first, then the action. Readers can then decide whether the step applies before they perform it.

- "To remove the cluster, click **Delete**."
- "After the build completes, run `npm test`."
- "In the **Token** field, enter your access token."
- "If you use a proxy, set the `HTTPS_PROXY` environment variable."

## Keep sentences short and single-purpose

Give each sentence one idea. When a draft sentence joins two ideas with *and*, *while*, or *as well as*, split it. Short sentences translate cleanly and read well on small screens.

Vary how sentences begin. A paragraph reads naturally when some sentences open with the condition, some with the actor, and some with the action.

## Use contractions where they sound natural

Contractions keep the tone conversational: *it's*, *don't*, *can't*, *you'll*, *you've*, *isn't*, *aren't*, *won't*. Spell out the words when the contraction would be ambiguous or awkward, such as *it would* and *there would*.

## Write timeless content

Describe the current behavior as a plain fact, so that the sentence stays true after the next release.

| Situation | Timeless sentence |
| :--- | :--- |
| A feature that arrived in the latest release | The API supports WebSockets. |
| A default that holds at the time of writing | Python 3.12 is the default runtime. |
| A feature planned for a later release | For supported architectures, see [System requirements](https://example.com/docs/requirements). |
| A version that replaced an earlier one | Use the v2 endpoint. For v1 migration steps, see [Migrate to v2](https://example.com/docs/migrate). |

Words that anchor a sentence to a moment (`currently`, `now`, `soon`, `recently`, `at this time`) can usually be removed without changing the meaning. Where the timing matters, give the version or date: "Starting with version 3.2, the client retries automatically."

## State facts instead of judgments

Describe capability with specifics that a reader can verify:

- "Processes up to 50,000 requests per second on a 4-vCPU instance."
- "Encrypts data at rest with AES-256."
- "To compile the project, run `make build`."

Specifics replace both marketing adjectives and reassurances about difficulty. A step that needs documentation deserves a plain instruction; the reader judges the difficulty.

## Keep the tone plain and professional

- Give instructions directly: "Click **Save**." The word `please` belongs in requests for permission or forgiveness.
- End sentences with periods. Emphasis comes from word choice and sentence position.
- Choose literal wording over idioms, humor, and pop-culture references, which translate poorly and age fast.
- Describe software in terms of what it does: "The load balancer marks the backend as unhealthy after three failed health checks." "Cyclic dependencies cause a compilation error."

## Write for a global audience

- Prefer the common word: *use* rather than *utilize*, *start* rather than *commence*, *help* rather than *facilitate*.
- Prefer a single verb where one exists: *remove* rather than *take out*, *continue* rather than *carry on*.
- Keep at most two nouns in a row as modifiers: "the configuration file for the storage bucket".
- Give every pronoun an unmistakable antecedent. When *this* or *it* could point to two things, repeat the noun.
- Keep helper words such as *that* and *then*: "Verify that the service is running."
- State what the reader can do. When a limit matters, state it as a boundary: "The name can contain up to 63 characters."
