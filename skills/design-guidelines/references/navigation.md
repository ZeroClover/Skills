# Navigation

Source: Steve Krug, *Don't Make Me Think, Revisited*, 3rd edition, Chapter 6, "Street signs and Breadcrumbs," and Chapter 7, "The Big Bang Theory of Web Design." Navigation answers where I am, what the sections are, and how to move. The entry screen answers what this place is before any of that can stick.

People often arrive in the middle of a site from search, mail, or a link. They did not walk your happy path from the home page. Design every deep page for that arrival.

## Persistent navigation

Persistent (global) navigation appears on every page, in the same place, working the same way, so it only has to be learned once. Include the four things people need at all times:

- **Site identifier.** The name or logo of the whole site. Place it at the top, where it frames the page (on the upper left for left-to-right languages). It should look like an identifier. It links home, because it stands for the whole site. Also include an explicit Home item among the sections, so the way back does not depend on knowing that the logo is a link. The identifier should frame the page rather than outshout the page's own title, except on the entry screen.
- **Sections.** The primary sections. Keep this list to the sections people need from everywhere. Deeper levels belong in local navigation.
- **Utilities.** Sign-in, cart, help, and the other tools that are not sections of the content. Krug's rule of thumb is about four or five utilities, the ones people need most often. Less-used leftovers belong in the footer.
- **Search.** A real search field on sites that have enough content to search, including the entry screen. Chapter 6 covers search wording and how many options to expose. Keep the default to a single obvious field.

On a form whose only job is to be finished (payment, registration), use a reduced bar: the site identifier, a way home, and the utilities that help complete the form. Full navigation there is a distraction.

## Page names

Page names are the street signs. Every page needs one. Highlighting the section in the nav is not a substitute.

- Put the name where it frames the content unique to this page, not the chrome.
- Make it look like the heading of the whole page. It is often the largest text.
- Match the words the visitor clicked. If the words must differ, keep them obviously equivalent ("Gifts for Her" landing on "Gifts for Women") and make the reason for the difference plain. A mismatch, or a pile of small mismatches, costs trust.

## You are here

Mark the current section in the navigation. The mark has to be obvious. Subtle color shifts get missed. Use more than one distinction, such as weight plus color. If you think the mark is already too loud, it may still be too quiet for a hurried visit.

Breadcrumbs show the path from home to the current page and make it easy to go up. They help most on a large site with a deep hierarchy. They do not replace thought-out navigation.

- Put them at the top, in a small size, so they read as an accessory.
- Separate levels with a greater-than sign, which suggests moving down the path.
- The last item is the current page name. Make it bold, and do not make it a link.

Tabs work when the selected tab looks physically in front: a different color or shade, and a shape that connects to the panel below it. A row of buttons that does not connect to the panel is not a tab.

## The trunk test

Krug's check for a deep page: imagine being dropped on it, unable to study it closely. You should answer without hesitation:

- What site is this? (site identifier)
- What page am I on? (page name)
- What are the major sections? (primary navigation)
- What are my options at this level? (local navigation)
- Where am I in the structure? (you-are-here marks)
- How do I search?

Run it by squinting or holding the screen at a distance, then circle those six. Ask someone else to do it. Failure means the chrome is too quiet or too clever, not that the visitor should have looked harder.

## The entry screen

Chapter 7's point: the first seconds set the interpretation of everything later. If the first guess about what this is is wrong, people force later details to fit that guess.

An entry screen has to carry identity and mission, the hierarchy of what is here and what you can do, search when the site needs it, teasers of the good stuff (content promos and feature promos), signs of life if freshness matters, deals and shortcuts the business requires, and a way in for registration if you use it. It also has to show people what they came for, expose something they did not know to ask for, show where to start, and look credible.

That list always overflows. The item that gets lost, and the item you cannot lose, is the big picture. A newcomer should answer four questions at a glance:

- What is this?
- What can I do here?
- What do they have here?
- Why should I be here, and not somewhere else?

Krug notes that people now often land deep and then visit the entry screen to get their bearings. Every deep page should still orient them, and the entry screen remains the place that does it fully.

Three places carry an explicit statement of what the site is: a tagline visually tied to the site identifier, a short welcome line, and the content itself. Open Chapter 7, "How to get the message across," before you write those lines. A tagline is a clear, specific phrase next to the identifier, long enough to say what this is and how it differs, and short enough to read at a glance. Krug suggests that good ones are often about six to eight words. A tagline is not a motto. A motto praises you. A tagline tells the visitor what they get. Generic taglines fail. Some famous sites can skip one; Chapter 7 lists the cases. If you are not in those cases, write the tagline.

The entry screen is where every stakeholder wants a promotion. Protect the four questions from that pressure. Space above the first scroll is the most fought-over part because people scan until they find a promising link and then stop.

## Examples

**Do.** A documentation page with the product name at the top left, the same five sections on every page, the current section in bold and in the accent color, the page title in the same words as the link that opened it, and a breadcrumb in small type: Docs > Billing > Invoices. Search is a field, not a link.

**Avoid.** A page whose only title is a highlighted nav item, a breadcrumb used instead of sections, and a home page full of campaign banners with no line that says what the product does. The visitor who arrived from search cannot tell whether they are in the right place.

## Review questions

- Does every page show the site identifier, the sections, the utilities, and search, unless it is a focused form?
- Does every page have its own name, in the right place, matching the link that led there?
- Is the current location obvious if you are not already familiar with the site?
- Can a newcomer answer the four entry questions at a glance?
- Is the tagline specific to this product, and is it visually tied to the identifier?

## Go deeper

Chapter 6 is the long chapter on persistent navigation, page names, breadcrumbs, tabs, and the trunk test. Use it when you are designing a navigation system rather than checking one page. Chapter 7 covers the entry screen's competing jobs, the excuses for not stating the big picture, and how to write a tagline. Lower-level navigation and search options are in Chapter 6 and are too specific to summarize here.
