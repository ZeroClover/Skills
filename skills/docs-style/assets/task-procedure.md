# [Task in sentence case, for example: Create a storage bucket]

[One or two sentences that say what the reader accomplishes, who the guide is for, and the end result.]

## Before you begin

Make sure that you have the following:

- [Prerequisite, for example: The Cloud CLI, version 2.0 or later, installed.]
- [Prerequisite, for example: A project with billing enabled.]
- [Prerequisite, for example: The `roles/storage.admin` role on your account.]

## [First phase in sentence case, for example: Configure your environment]

To [goal of this phase]:

1. [Location or condition first], [action]:
   ```bash
   [command --flag VALUE]
   ```
2. [Next action]:
   ```bash
   [command --output]
   ```
   [Result of the step, for example: The CLI prints a confirmation message.]

## [Main task in sentence case, for example: Create the resource]

To [perform the main action]:

1. In the [console or UI area], go to the **[Page name]** page.
2. Click **[Button name]**.
3. In the **[Field label]** field, enter *`SAMPLE_VALUE`*.
4. From the **[List label]** list, select **[Option name]**.
5. Optional: Select the **[Checkbox label]** checkbox.
6. Click **[Submit button name]**. [Result, for example: The console creates the resource and opens the **Resource details** page.]

> [!NOTE]
> [Background detail or tip that helps but is separate from the steps.]

## Verify the result

To verify that the [resource] is working:

1. Send a test request:
   ```bash
   curl -i https://api.example.com/v1/resources/RESOURCE_ID \
     -H "Authorization: Bearer API_KEY"
   ```
   Replace the following:
   - *`RESOURCE_ID`*: the ID returned when you created the resource
   - *`API_KEY`*: an access token generated in the console
2. Confirm that the response returns `200 OK` and the resource payload:
   ```json
   {
     "status": "ready",
     "id": "res-12345",
     "created_at": "2026-08-25T00:00:00Z"
   }
   ```

## What's next

- [Descriptive link, for example: Learn how to [configure access control](https://example.com/docs/access-control).]
- [Descriptive link, for example: Set up [monitoring and alerting](https://example.com/docs/monitoring).]
