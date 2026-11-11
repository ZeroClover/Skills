---
name: design-guidelines
description: "Review or design pages, screens, and layouts so people can see what matters and act without puzzling. Use when creating or critiquing a website, app, form, slide, poster, flyer, or navigation; when the user mentions contrast, repetition, alignment, proximity, type, color, hierarchy, scanning, clutter, labels, or usability; or when a layout looks busy, uneven, or unclear. Based on Robin Williams' four design principles and Steve Krug's usability guidance. Before changing layout, type, color, wording, navigation, or a test plan, open the reference named in the index."
---

# Design guidelines

Make the piece look organized, and make the next action obvious. Robin Williams' *The Non-Designer's Design Book*, 4th edition (Peachpit, 2015; Chinese edition 《写给大家看的设计书》), covers visual organization. Steve Krug's *Don't Make Me Think, Revisited*, 3rd edition (New Riders, 2014), covers how people actually use screens. Ideas below name the book they come from. This file is the working set. Open a reference only for the topic you are changing.

The user's request, the product's design system, and any accessibility requirement they name take precedence over this skill. For developer-documentation voice, follow the `docs-style` skill. Use this skill to judge layout and whether the words need to be there.

## Which book leads

Use Williams when the job is a composed layout: page, slide, poster, flyer, or a screen that looks unorganized. Use Krug when someone must operate the thing: website, app, form, or navigation.

On an interface, satisfy Krug's clarity first, then use Williams to make that clarity visible. Proximity shows what belongs together. Alignment connects elements. Repetition shows that separated items are the same kind of thing. Contrast shows what matters more.

Krug's rule when the two pulls differ: if a small inconsistency makes the page much clearer, choose clarity. Williams' matching rule: once a principle is visible, break it only on purpose, and make the break strong enough to look intentional.

## Core principles

Williams introduces them in Chapter 1, "Introduction," and teaches them in Chapters 2–5:

1. **Proximity.** Group related items so they read as one unit. Space separates unrelated items.
2. **Alignment.** Place every element so it shares an edge or axis with another element.
3. **Repetition.** Repeat a visible element (type, color, rule, spacing, or mark) so the parts feel like one piece.
4. **Contrast.** If two elements are not the same, make them clearly different. The strongest element is the one people should see first.

Krug, Chapters 1–5 and 9:

1. **Self-evident.** A glance should answer what this is and what to do. If it cannot be self-evident, make it self-explanatory with a little carefully chosen text.
2. **Real use.** People scan, choose the first reasonable option, and muddle through. Design for that behavior.
3. **Mindless choices.** A few obvious steps beat one step that requires thought. Use familiar conventions unless the replacement is immediately clear or worth a short learning curve.
4. **Fewer words.** Remove words that do not help the task. Instructions are a last resort.
5. **Watch people try.** Settle "can they use it?" by watching a few people attempt real tasks, early and again later.

## Quick review

Check the artifact the user will actually see. Mark each item pass, fail, or not applicable. For every fail, open the reference in the index and change the design.

**Layout (Williams)**

- Related items sit together. A heading is closer to the content it names than to the block above it.
- Squinting at the layout yields a few visual groups, not a field of equal gaps.
- Every element lines up with another element. One alignment dominates.
- A repeated type style, color, spacing, or mark ties the sections together.
- Differences in size, weight, or color are obvious. The loudest element is the one that should be first.
- Body text is readable. Text and background differ clearly in lightness. A constraint can change the palette. It does not drop the lightness difference.

**Use (Krug)**

- A newcomer can say what this is and what to do next without puzzling over names or controls.
- Clickable things look clickable. The label says what the control does.
- Importance, grouping, and nesting are visible at a glance.
- The layout follows a convention the audience already knows, or the new pattern explains itself.
- Each choice is unambiguous. A hard choice has a short hint at the moment of the choice.
- Removing half the words would leave the task intact.
- On a deep page, the viewer can find the site identifier, the page name, the main sections, the local options, the current location, and search.
- An entry screen answers what this is, what a person can do here, what is here, and why it is worth staying.
- The primary task works from the keyboard, with field labels in place. Alt text matches the image's purpose: the action for a functional image, a longer equivalent for a chart or diagram, and an empty alt for decoration or a repeat of nearby text. Open [references/goodwill-and-access.md](references/goodwill-and-access.md) before writing those alternatives.

Stop when each item passes, or when a remaining miss names a narrow constraint and what is still provided. A constraint does not drop keyboard operation, labels, text contrast, or alt text.

If the remaining disagreement is about personal taste, run the small task test in [references/usability-testing.md](references/usability-testing.md). Another visual variant will not settle it.

## Index

Open the file for the check that failed. Each file has rules, examples, and review questions, and names the book chapter for anything finer.

| Open this file when | File | Source |
| :--- | :--- | :--- |
| Related items look scattered, or unrelated items look glued together | [references/proximity.md](references/proximity.md) | Williams, Chapter 2, Proximity |
| Edges feel accidental, or several alignments compete | [references/alignment.md](references/alignment.md) | Williams, Chapter 3, Alignment |
| Pages or sections look unrelated, or a motif is repeated until it dominates | [references/repetition.md](references/repetition.md) | Williams, Chapter 4, Repetition |
| The page feels flat, or two elements almost match | [references/contrast.md](references/contrast.md) | Williams, Chapter 5, Contrast |
| Typefaces, caps, punctuation, or type hierarchy are in question | [references/typography.md](references/typography.md) | Williams, Chapters 9–12 |
| A palette, tint, or print-versus-screen color choice is in question | [references/color.md](references/color.md) | Williams, Chapter 7, Design with Color |
| Names, controls, or the purpose of the screen make people pause | [references/self-evident-pages.md](references/self-evident-pages.md) | Krug, Chapter 1, Don't make me think! |
| The layout assumes people will read everything and compare every option | [references/scanning-and-satisficing.md](references/scanning-and-satisficing.md) | Krug, Chapter 2, How we really use the Web |
| Importance, grouping, or nesting is hard to see while scanning | [references/visual-hierarchy.md](references/visual-hierarchy.md) | Krug, Chapter 3, Billboard Design 101 |
| A control reinvents a familiar pattern, or a choice requires thought | [references/conventions-and-choices.md](references/conventions-and-choices.md) | Krug, Chapters 3 and 4 |
| Navigation, page titles, search, or the entry screen is in question | [references/navigation.md](references/navigation.md) | Krug, Chapters 6 and 7 |
| Intro copy, instructions, or labels are longer than the task | [references/omit-needless-words.md](references/omit-needless-words.md) | Krug, Chapter 5, Omit needless words |
| The team is debating usability, or you need to plan a test | [references/usability-testing.md](references/usability-testing.md) | Krug, Chapters 8, 9, and 13 |
| The design hides information, asks for too much, or ignores access | [references/goodwill-and-access.md](references/goodwill-and-access.md) | Krug, Chapters 10, 11, and 12 |

For a specific printed piece (business card, letterhead, flyer, newsletter, brochure, postcard, ad, or résumé), apply the four principles here, then use Williams, Chapter 8, "Extra Tips & Tricks," for the piece. For a full redesign exercise, use Williams, Chapter 13, "Does it Make Sense?". For the facilitator script of a usability test, use Krug, Chapter 9, and his companion *Rocket Surgery Made Easy*.
