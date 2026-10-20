# Self-evident pages

Source: Steve Krug, *Don't Make Me Think, Revisited*, 3rd edition, Chapter 1, "Don't make me think!" Krug's first law of usability: a page should be self-evident. If that is impossible, it must be self-explanatory. This is the tie-breaker when a design choice is otherwise even.

## Rules

A person who does not care about the subject, and who barely knows the interface, should be able to look at the page and say what it is. Thought balloons over a clear page name the parts ("there is the search," "that is the price"). Thought balloons over an unclear page are questions.

Remove the questions. Common ones: Where am I? Where do I start? Where did they put the thing I need? What is most important here? Why is it called that? Is that an ad? Can I click that?

Names are a frequent cause. Prefer the plain name the visitor would use ("Jobs") over a cute, branded, or internal name ("Talent Hub"), unless the unusual name is already famous to that audience. When there is a tradeoff between tone and clarity, move further toward obvious than the team's taste suggests.

Clickable things look clickable. A visitor should not spend a moment deciding whether a word or a shape will respond. If they click and nothing happens, the damage is already done: every small question adds load, and people resent puzzling when they are trying to finish a task.

You cannot make every original or inherently complex screen self-evident. The fallback is self-explanatory: appearance, well-chosen names, and a little carefully written text combine so that understanding takes almost no effort. See [omit-needless-words.md](omit-needless-words.md) before adding that text.

People may not leave when a page is confusing. They may have no alternative, or they may blame themselves. Clarity still matters because most people spend less time on the page than the author hopes. The page has to work at a glance. Krug compares good lighting in a store: the visit feels easier.

## Examples

**Do.** A flight search with fields labeled From and To. Typing a city shows a list of matching airports, and the chosen row stays readable as a city name. The button says Search flights.

**Avoid.** A field labeled "City or Airport" that replaces the chosen city with a three-letter code and then rejects a second city the visitor typed the same way. The visitor has to learn the field's private rules. A second avoid: the careers link labeled with an internal campaign name, sitting beside a second link that might be the same destination.

## Review questions

- Can a newcomer say what this screen is, in a few words, without help?
- Which labels would make a visitor ask "why did they call it that?"
- Is every control obviously something you can activate?
- If the screen cannot be self-evident, what single line of text makes it self-explanatory?
- Which question marks are you asking the visitor to carry while they do their real task?

## Go deeper

Chapter 1 is the whole argument, including why "the competition is one click away" is not the main reason. Use it when a team wants a longer checklist of question marks. Krug's point is to learn to see the question marks, not to collect another checklist. How people actually look at the page is Chapter 2; see [scanning-and-satisficing.md](scanning-and-satisficing.md).
