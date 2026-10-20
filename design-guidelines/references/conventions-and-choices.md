# Conventions and choices

Source: Steve Krug, *Don't Make Me Think, Revisited*, 3rd edition, Chapter 3, "Billboard Design 101" (conventions), and Chapter 4, "Animal, Vegetable, or Mineral?" (mindless choices). People grasp a page faster when it works the way pages like it already work, and when each step is a choice they do not have to think about.

## Conventions

A convention is a pattern people have already learned: where the site identifier sits, where primary navigation goes, what a shopping cart is, what a search icon means, how a video control looks. Category conventions exist too, for shops, publications, schools, and apps of a given type. They exist because an idea worked often enough that people stopped needing an explanation.

Use the convention when you do not have a better idea. Innovate when the new version is so clear that there is no learning curve, or when it adds enough value to be worth a small one. Replacing a system control (a scrollbar, a date picker, a back gesture) with a custom version usually discards years of tuning. Krug's example of a creative navigation that still works is one that also kept a conventional menu for when the novelty wore off.

Consistency inside the product is worth keeping: navigation that stays put does not have to be relearned. Clarity still wins. If a small inconsistency makes a step much clearer, choose the clearer version. Krug states this directly in Chapter 3: clarity trumps consistency.

Chapter 10, "Mobile: It's not just a city in Alabama anymore," adds the constraint. The same laws apply, and people move faster and read less on a small screen. Design is constraints and tradeoffs, and many serious usability problems are a bad tradeoff (too-small chunks of a story, each behind a slow load, each repeating the same chrome). Krug deliberately avoids a catalog of mobile patterns because those patterns keep changing. Name the constraint, name what you gave up, and keep the primary task obvious. Test on the device. For current platform conventions, follow the platform's present guidance and use Chapter 10 for the tradeoff test, not for a 2014 widget list.

## Mindless choices

Krug's second law, from Chapter 4: within reason, the number of clicks or taps matters less than whether each one is a mindless, unambiguous choice and the person stays confident they are on the right track. His rule of thumb weighs one step that requires thought about as heavily as several steps that do not, on the order of three easy steps to one hard step. The exception is a path people repeat constantly, or a path where every step is slow. Then fewer steps matter more.

Links need a strong scent: the words should say what is at the other end. Ambiguous labels ("Solutions," "Resources," a business-versus-home choice the visitor cannot map onto themselves) force a guess and a second round of thinking after the page loads.

When a choice really is hard, help at the moment of the choice. Krug's standard for that help is brief, timely, and unavoidable: the smallest hint, placed where the decision happens, in a form the person will notice. A tooltip, a line beside the field, or a short label can do this. A manual somewhere else will not.

Caroline Jarrett's *Forms that Work* is the book Krug points to for questions that are hard to answer. Use it for form wording beyond this file.

## Examples

**Do.** A checkout that asks for shipping address, then shipping method, then payment. Each step's title matches its contents. The card field accepts spaces. A line under the postal-code field says "Used for tax and delivery estimates" at the moment the visitor wonders why you asked.

**Avoid.** A first screen that asks the visitor to choose "Personal," "Professional," or "Enterprise" when they only know they want to print a document. They have to invent a category and then check whether they were right. A second avoid: a custom scrollbar and a custom back control that look like the brand and behave unlike the platform.

## Review questions

- Which convention does this control replace, and is the replacement clearer or more valuable?
- Is each next step unambiguous from its label alone?
- Are you counting clicks, or counting how much thought each click takes?
- If a choice must be hard, is the help brief, next to the choice, and visible?
- What did the layout give up to satisfy a constraint, and does the primary task still win?

## Go deeper

Chapter 3's convention section includes the argument for taking advantage of conventions and the clarity-over-consistency rule. Chapter 4 is the full case on mindless choices, including the information-scent idea from Peter Pirolli and Stuart Card. Chapter 10 is the chapter to open for a mobile tradeoff, affordances, and responsive layout, with the warning that specific interface fashions in that chapter have aged.
