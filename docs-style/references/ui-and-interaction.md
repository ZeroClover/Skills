# UI and interaction

This reference covers how to name UI elements and describe what the reader does with them.

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
| Keyboard key | press | Press **Enter**. |
| Collapsible section | expand, collapse | Expand **Advanced options**. |
| Dialog or panel | open, close | Open the **Export** dialog. |
| Element under a pointer | hover over | Hover over the chart to see values. |

## Locate elements by label and context

Give the reader the place first and the action second: "In the upper-right corner of the page, click **Settings**." Pair any positional cue with the element's label, because layouts change with screen size and language.

Refer to content on the page by reading order: "the following table", "the preceding steps".

## Keyboard shortcuts

Bold key names and join simultaneous keys with a plus sign: "Press **Ctrl+S**." Give the menu or button path as the primary instruction, and mention the shortcut as an alternative.
