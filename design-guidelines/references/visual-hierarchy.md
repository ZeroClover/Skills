# Visual hierarchy

Source: Steve Krug, *Don't Make Me Think, Revisited*, 3rd edition, Chapter 3, "Billboard Design 101." Pages are scanned, so the look of the page has to carry the relationships: what is important, what is similar, and what is part of what. Krug also asks for clearly defined areas, obvious clickability, less noise, and text formatted for scanning. Williams supplies the visual tools; this file says what those tools must communicate. See [contrast.md](contrast.md), [proximity.md](proximity.md), and [alignment.md](alignment.md).

## Three traits

A clear hierarchy has all three:

1. **Prominence matches importance.** The most important element is larger, bolder, in a distinctive color, set off by more space, nearer the top, or some combination. Secondary items look secondary.
2. **Logical relationships are visual.** Similar things share a heading, a style, or a region. See proximity and repetition.
3. **Nesting shows what is part of what.** A section name sits over the items in that section, and a title spans the description that belongs to it. A heading that spans the wrong items is like a sentence whose "it" points at the wrong noun. People can often recover, and they still had to think.

Build the hierarchy for a glance. If you, as the designer, think a cue is already loud, Krug's experience is that hurried users still miss subtle cues, so the cue probably needs to be stronger. "You are here" marks fail this way most often. See [navigation.md](navigation.md).

## Areas, noise, and scanning

Divide the page into regions a scanner can name: navigation, content, the task, related items. A region with no visible boundary melts into its neighbor.

Noise is anything that competes without helping: a busy background, too many colors, too many boxes, or emphasis on so many words that emphasis means nothing. Remove noise before you add emphasis.

Format the text for scanning even when some people will read it. Use headings, short paragraphs, and lists. Put the informative words at the start of headings and links.

Clickable things look clickable, and non-clickable things do not. Underlines, button shapes, and placement are the usual signals. If the design language removes those signals, put them back in some other form that a glance can read. Krug discusses this under flat design and signifiers in Chapter 10; the rule belongs here because it is part of scanning.

## Examples

**Do.** A pricing page with three plans. The recommended plan is larger, has the only filled button, and sits in the visual center. Each plan name spans its price and its feature list. Feature lists share one style. Nothing else on the page is the same size as the plan names.

**Avoid.** Three plans in identical boxes, plus a banner and a testimonial at the same visual weight, plus bold phrases scattered through the feature lists. The recommended plan is marked only by a 10-pixel outline in a close color. A heading "For teams" sits above a paragraph about individual plans.

## Review questions

- What is the most important element, and is it the most prominent?
- Which items are the same kind of thing, and do they look the same?
- Does every heading span only what it names?
- Can you name the regions of the page at a glance?
- What can you remove without changing the task?
- Would a scanner know what is clickable?

## Go deeper

Chapter 3 is the full billboard list, including conventions (see [conventions-and-choices.md](conventions-and-choices.md)) and the worked pages. Use it when a whole template needs a pass, not a single control. Williams, Chapter 5, is the matching lesson on making contrast strong enough to create that prominence.
