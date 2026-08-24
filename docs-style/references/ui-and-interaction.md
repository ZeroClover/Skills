# UI and interaction

This reference covers how to name UI elements and describe what the reader does with them.

## Focus on the task

State the outcome when the interface makes the gesture clear: "Refresh the page." Add the control and gesture when they help the reader locate or complete the action: "Click **Refresh**."

## Format UI labels in bold

Bold the text exactly as it appears in the interface: buttons, menu items, tabs, field labels, checkbox labels, dialog titles, and option names.

```markdown
1. In the console, open the navigation menu.
2. Click **IAM & Admin > Service accounts**.
3. Click **Create service account**.
4. In the **Service account name** field, enter `backend-service`.
5. Click **Done**.
```

Refer to an element by its label when the label is enough: "Click **Save**." Add the element type when it helps the reader find it: "Select the **Enable SSL** checkbox."

## Menu paths

Write a sequence of menus as a single bold span with a greater-than sign between items:

- "Click **File > New > Document**."
- "Go to **Settings > Security > API keys**."

For HTML output, put a nonbreaking space before each `>` and give the separator the accessible label "and then". For portable Markdown or a sequence that mixes different control types, spell out the transitions: "In the **File** menu, select **New**, and then select **Document**."

## Interaction verbs

| Element | Verb | Example |
| :--- | :--- | :--- |
| Button, link, menu item (pointer) | click | Click **Save**. |
| Any element (touchscreen) | tap | Tap **Confirm**. |
| Checkbox, radio button, option | select | Select the **Enable caching** checkbox. |
| Checkbox, to turn it off | clear | Clear the **Debug mode** checkbox. |
| Toggle | turn on, turn off | Turn on **Automatic backups**. |
| Text field | enter, type | In the **Port** field, enter `8080`. |
| List or menu | select | From the **Region** list, select **us-central1**. |
| Keyboard key | press | Press `Enter`. |
| Collapsible section | expand, collapse | Expand **Advanced options**. |
| Dialog or panel | open, close | Open the **Export** dialog. |
| Element under a pointer | hover over | Hover over the chart to see values. |

## Locate elements by label and context

Give the reader stable context first and the action second: "On the application toolbar, click **Settings**." Use the element's label, nearby named context, tooltip, or accessible name to help the reader find it. A screenshot can orient the reader when those cues need visual support.

Refer to content on the page by reading order: "the following table", "the preceding steps".

## Keyboard shortcuts

Format key names in `kbd` elements for HTML and monospace in Markdown. Join simultaneous keys with a plus sign: "Press `Control+S`." Lead with the menu or button path. Add a keyboard step when keyboard interaction is the task or the shortcut is itself the documented feature.
