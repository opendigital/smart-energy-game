
IN EACH APP THERE IS A `pages.py`

This sets up a Page class for each page that is displayed
Every page also has a template file in the templates below


### OTREE PAGE ORDER

At the end of every page.py there is a `page_sequence` variable
this explicitly sets which pages will show in the app and
what their order is.

EXAMPLE:

training app pages

```
page_sequence = [
    Intro1,
    Intro2,
    Intro3,
    Intro4,
    Intro5,
    Intro6,
    Intro7,
    Examples,
    Example1,
    Example2,
    Example3,
    PracticeIntro,
    PracticeGame1,
    PracticeResults1,
    PracticeGame2,
    PracticeResults2,
    Quiz,
    Quiz1,
    ReviewGameRules,
    Quiz1,
    Quiz2,
    ReviewGameRules,
    Quiz2,
    Quiz3,
    ReviewGameRules,
    ReviewGameRules,
    Quiz3,
    Quiz4,
    ReviewGameRules,
    Quiz4,
    GameIntro,
]
```


### PAGE TITLES

The otree game doesnt store the frontend text and titles / html in a database
like what you are used to interfacing with on something like a blog or website
builder.

Instead the HTML for every page is kept in its own file (or in many files). While this
gives you lots of freedom it can also turn in to a nightmare for making chanegs later if you have to
make changes in 10 places to update one screen.   The 'base-game' has about 76 pages in total by the
time after the player has completed the game.

This produces a ton of opportunities for for small pieces of text or html to start to deviate
from the expected version, especially when working with non-developer and content sources files that
can not directly be ported in and out of the game templates and code files. (pdf, jpg, powerpoint, word.docx)

### TIPS AND TRICKS

When working on large complicated apps like otree it's important to
look for failproof ways to create links between things that are reliable
and don't require extra effort to decode how to map between things.  


It is already difficult in this framework to find a way to name your
page models instances in a away that creates some nicely organized
structure in the templates since by default your page template files must
be named exactly the same as the function that  calls it.

You can start with a numbering strategy which is 'just okay' for small number of
pages, but later on if someone tells you to date text 'Game Introduction: Examples 3'.
You are going to spend all of your time digging through 15.html or 23.html looking
for a variable names "tableVaraible23" and you will hate every second of  your life
spent on that project until you tear it apart completely and come up with a better
system. Bonus: when you get come into someone else's project who moved and never finished
because they wrote themselves into a corner and gave up. This is usually the case when
working on non-modern web frameworks

### page_sequence -> page_titles

Give every page a a title that will correspond directly
to its order in the overall sequence.

This lets you figure out exactly what the url/template/model function that
something is is a person can tell you what the title is thats showing on the  
screen.

We created the `page_titles` list at the top of each apps constant.py to
create an index for that will map to the page_sequence list at the bottom
of the pages.py file.



    page_titles = [
        "Research Participant Consent Form",
        "Instruction: Game Outline",
        "Instruction: Game Structure and Incentives",
        "Instruction: Introduction",
        "Instruction: Gameplay",
        "Instruction: Financial Outcomes",
        "Instruction: Environmental Outcomes",
        "Examples: Overview",
        "Examples: 1. Minimum Requirement",
        "Examples: 2 and 3. Min and Max Conservation",
        "Examples: 4 and 5. Only You and Everyone But You",
        "Practice: Game Intro",
        "Practice: Game",
        "Practice: Game Result",
        "Comprehension: Quiz",
        "Comprehension: Quiz 1/4",
        "Comprehension: Quiz 2/4",
        "Comprehension: Quiz 3/4",
        "Comprehension: Quiz 4/4",
        "Game: Introduction",
    ]



page_sequence = [
    Intro1,
    Intro2,
    Intro3,
    Intro4,
    Intro5,
    Intro6,
    Intro7,
    Examples,
    Example1,
    Example2,
    Example3,
    PracticeIntro,
    PracticeGame1,
    PracticeResults1,
    PracticeGame2,
    PracticeResults2,
    Quiz,
    Quiz1,
    ReviewGameRules,
    Quiz1,
    Quiz2,
    ReviewGameRules,
    Quiz2,
    Quiz3,
    ReviewGameRules,
    ReviewGameRules,
    Quiz3,
    Quiz4,
    ReviewGameRules,
    Quiz4,
    GameIntro,
]
