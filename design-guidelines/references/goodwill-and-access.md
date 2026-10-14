# Goodwill and access

Source: Steve Krug, *Don't Make Me Think, Revisited*, 3rd edition, Chapter 10, "Mobile: It's not just a city in Alabama anymore," Chapter 11, "Usability as common courtesy," and Chapter 12, "Accessibility and you." Clarity is half of usability. The other half is behaving as if the visitor's time and dignity matter, including visitors who use the product differently from the team.

## Goodwill

Chapter 11 asks you to picture a reservoir of goodwill that each problem drains. The reservoir is personal, it is already low when someone arrives in a hurry or from a bad experience, it can be refilled, and a single offense can empty it. Leaving is not the only cost. People also come back less willingly and think worse of the organization.

Things that drain it:

- Hiding what people came to learn, especially price, shipping, and a way to reach a person.
- Punishing a format. Accept a phone number or a card number with or without spaces and punctuation.
- Asking for information the task does not need.
- Faux sincerity, including reassurance that does not match the wait or the policy.
- Making people pass through decoration to reach the task.
- A sloppy, disorganized surface. People comment freely on colors; they rarely leave for color alone. Krug's advice is to ignore color opinions in a test unless several people react violently. An amateurish, broken, or chaotic page is a different problem. See [visual-hierarchy.md](visual-hierarchy.md).

Sometimes the business chooses to annoy people, for a measured gain. Make that choice explicitly. An accidental annoyance spends the reservoir without the gain.

Things that refill it:

- Make the few main tasks obvious and easy. Teams usually agree on what those tasks are, and then fail to prioritize them.
- Say the unwelcome fact up front: fees, outages, limits.
- Save a step you could have left to the visitor, such as a tracking link that opens the right shipment.
- Put real effort into the help content: accurate, findable, and current.
- Publish the questions people actually ask, including the awkward ones, and keep that list current. A list of questions you wish they would ask does not count.
- Offer a practical kindness, such as a print view that keeps the figures and drops the ads.
- Make errors recoverable, with an obvious way back.
- If you cannot do what they want, say that you know it is an inconvenience.

## Access

Chapter 12: a product is not usable if people with disabilities cannot use it. Krug's reason for doing the work is that it is the right thing and it can change what someone is able to do. Legal requirements arrive as well. Do not wait for the fear of extra work, or the fear that access and a good design are opposed, to settle the question. Many of the important fixes do not force that tradeoff.

A technical constraint can narrow the method. It does not remove the checks. If a control cannot use the platform's usual keyboard behavior, provide another keyboard path and name what that control cannot do. Still label every field, still keep text contrast, and still give each image the alternative its purpose requires.

The highest-leverage step is to fix the usability problems that confuse everyone. A confusing error is worse when you cannot see the page. Guidelines applied to an unclear interface still leave it unusable.

Then do the high-impact implementation work. Krug's list, which he tells you to learn properly from a current accessibility reference such as WebAIM rather than from memory:

- Give every image alternative text that matches its purpose. A functional image names the action: an icon-only search button is "Search," not "magnifying glass." A complex image, such as a chart or diagram, needs a longer equivalent of the information it shows. A decorative image, or one that repeats nearby text, gets an empty alt so it is not announced again.
- Use real headings in order, and style them with CSS. Headings are navigation for someone listening.
- Associate each form field with its label.
- Provide a way to skip repeated navigation.
- Make the content operable from the keyboard.
- Give text a significant lightness difference from its background. Do not rely on color alone.
- Start from a template or component set that was built to be accessible.

Screen-reader users scan with their ears. They listen to the first words of a link or a line and move on. Put the distinctive words first. Krug points to Mary Theofanos and Janice (Ginny) Redish, "Guidelines for Accessible and Usable Web Sites: Observing Users Who Work with Screen Readers," as the article to read before other accessibility writing. Two books he names for the broader picture are Sarah Horton and Whitney Quesenbery, *A Web for Everyone*, and Jim Thatcher and others, *Web Accessibility: Web Standards and Regulatory Compliance*. Prefer current editions and the standard you are required to meet. A validator finds some missing text and then a pile of warnings. It is not a spellchecker. Use it, and still watch people.

Chapter 10's durable point on small screens: the same principles apply, people read even less, and serious problems often come from a bad tradeoff under a real constraint. Test on the device. Do not copy aged mobile patterns out of that chapter. See [conventions-and-choices.md](conventions-and-choices.md).

## Examples

**Do.** A pricing page that shows the monthly price, the annual price, and what is not included, before the signup button. The signup form asks for an email and a password. The error "That email is already in use" offers a sign-in link. The price is text, not an image, and the button is reachable by keyboard. An icon-only search button is named "Search." A chart of the same prices has a text equivalent of the trend. A decorative rule, or a logo that repeats the product name beside it, has an empty alt.

**Avoid.** A wireless-portal flow that takes three promotional screens to reveal the price. The card field rejects spaces. Support contact is absent. The heading structure is a row of styled divs, so a screen-reader user cannot jump to "Price." An icon-only search control is announced as "magnifying glass," and a chart has no text equivalent.

## Review questions

- What are the three things people come here to do, and can they start each one immediately?
- Which facts would you rather hide, and are they visible before the commitment?
- Are you asking only for what this step needs, in whatever format the visitor naturally types?
- Can someone complete the primary task by keyboard, with headings and labels in place?
- Does each image's alt text match its purpose: the action, a longer equivalent, or an empty alt?
- Do links and headings start with the words a person would scan for?
- If a constraint narrows the method, is the primary task still the easy path, with keyboard operation, labels, text contrast, and purpose-based alt text still in place?

## Go deeper

Chapter 11 is the goodwill reservoir and both lists. Chapter 12 is the case for access, why the slogan "it helps everyone" is the wrong lead, and the four things to do now, including the article and the two books. Chapter 10 is the mobile tradeoff discussion. Numeric contrast ratios and current techniques change; take them from the standard and from WebAIM, not from this skill.
