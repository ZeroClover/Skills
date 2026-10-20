# Scanning and satisficing

Source: Steve Krug, *Don't Make Me Think, Revisited*, 3rd edition, Chapter 2, "How we really use the Web." Designers picture a careful reader who studies the page and picks the best link. What usually happens is a glance, a scan, and a click on the first thing that seems close. Design for that behavior. Krug's line is: if people treat the page like a billboard going past, design a good billboard.

## Three facts

**People scan.** They are on a mission, they need only a fraction of the page, and scanning is a skill they already have. Even on a page they will read, such as an article, they alternate between reading and scanning. They notice words that match the task, words that match a personal interest, and a few hard-wired triggers. They skip the rest.

**People satisfice.** The term is Herbert Simon's: they choose the first reasonable option, not the best one. Optimizing is slow. On the web the penalty for a wrong guess is often the Back button, so guessing is rational. A visitor weighs options when they are unhurried and they trust the site. You cannot count on that mood.

**People muddle through.** They use things without a correct mental model, including people who are technically skilled. Once something works, they stick to it. Muddling can succeed and still be slow and error-prone. When the interface is clear, people find more of what you offer, you can steer them, and they feel competent. They leave for a clearer competitor even when they could have muddled through.

There is no average user who will read it properly. Chapter 8 develops that point; see [usability-testing.md](usability-testing.md).

## What to do about it

Put the words that match the task where a scan will hit them: headings, links, buttons, and the first words of a line. A screen-reader user scans too, by listening to the start of a link or a line. See [goodwill-and-access.md](goodwill-and-access.md).

Make the first reasonable choice the correct one. If several links could be the first reasonable guess, they are too similar. See [conventions-and-choices.md](conventions-and-choices.md).

Do not require a correct theory of the system. A visitor who thinks the browser is "the search" can still finish if the control they need looks like the thing they are trying to do.

Assume large parts of the page will not be looked at. The material that matters has to survive that. See [visual-hierarchy.md](visual-hierarchy.md).

## Examples

**Do.** A support page whose heading is "Replace a lost card," with a button of the same words. A secondary link, "See all card services," is visually quieter. The visitor who scans for "lost card" hits the right control first.

**Avoid.** A page of three equal links: "Card solutions," "Account resources," and "Help center." Any of them might contain the lost-card task, so the visitor guesses. A second avoid: a paragraph that explains the company's philosophy of support above the link that actually starts the task.

## Review questions

- What is the visitor trying to do, in their words?
- Do those words appear in a heading, a link, or a button a scan will catch?
- Is the first reasonable choice the right one?
- Can someone finish the task with a wrong theory of how the product works?
- What on this page can be missed entirely without blocking the task?

## Go deeper

Chapter 2 is the evidence and the three facts. Chapter 3 turns them into page design; see [visual-hierarchy.md](visual-hierarchy.md). Chapter 5 cuts the words scanning will never read; see [omit-needless-words.md](omit-needless-words.md).
