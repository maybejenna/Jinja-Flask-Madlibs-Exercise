"""Madlibs Stories."""
from flask import Flask, request, render_template
from random import randint, choice

app = Flask(__name__)

@app.route("/")
def home_form(): 
    return render_template("home.html")

class Story:
    """Madlibs story.

    To  make a story, pass a list of prompts, and the text
    of the template.

        >>> s = Story(["noun", "verb"],
        ...     "I love to {verb} a good {noun}.")

    To generate text from a story, pass in a dictionary-like thing
    of {prompt: answer, promp:answer):

        >>> ans = {"verb": "eat", "noun": "mango"}
        >>> s.generate(ans)
        'I love to eat a good mango.'
    """

    def __init__(self, words, text):
        """Create story with words and template text."""
        self.prompts = words
        self.template = text

    def generate(self, answers):
        """Substitute answers into text."""
        return self.template.format(**answers)
    

def random_place():
    return choice(["forest", "mountain", "city", "village", "desert"])

def random_noun():
    return choice(["dragon", "castle", "river", "hero", "sword"])

def random_verb():
    return choice(["run", "jump", "fly", "swim", "climb"])

def random_adjective():
    return choice(["brave", "dark", "mysterious", "ancient", "magical"])

def random_plural_noun():
    return choice(["monsters", "treasures", "warriors", "spells", "kingdoms"])

# Here's a story to get you started
# Default story if no type is selected or if an unknown type is provided



title_templates = [
    "The {adjective} {noun} of {place}",
    "A {verb} in the {place}",
    "{plural_noun}: The {adjective} {noun} Story",
    "{place} and the {adjective} {noun}",
    "When the {noun} {verb}",
]

default_story = Story(
    ["place", "noun", "verb", "adjective", "plural_noun"],
    """Once upon a time in a long-ago {place}, there lived a
       large {adjective} {noun}. It loved to {verb} {plural_noun}."""
)

story_templates = {
    "mystery": Story(
        ["place", "noun", "verb", "adjective", "plural_noun"],
    """In the shadowy corners of {place}, a {adjective} {noun} mysteriously disappeared. 
    Rumors said it would {verb} {plural_noun} under the pale moonlight. 
    The townspeople whispered about the {adjective} {noun}, speculating wildly about its whereabouts. 
    Little did they know, the {noun} held a secret, a {adjective} truth that would {verb} the {place} forever. 
    The mystery of the {noun} and the {plural_noun} was about to unravel, leading to an unexpected and {adjective} revelation."""
    ),

    "adventure": Story(
        ["place", "noun", "verb", "adjective", "plural_noun"],
    """In the far-off lands of {place}, a {adjective} {noun} was rumored to hold the power to {verb} {plural_noun}. 
    Brave souls embarked on a perilous journey, facing {adjective} challenges to discover the {noun}. 
    As they trekked through the {place}, their resolve was tested by both friend and foe. 
    The quest to {verb} the {noun} was more than an adventure; it was a journey of self-discovery and the {adjective} courage to face the unknown."""
    ),

    "magical": Story(
        ["place", "noun", "verb", "adjective", "plural_noun"],
    """In the enchanted realm of {place}, a {adjective} {noun} was said to {verb} {plural_noun} with a mere thought. 
    The inhabitants of {place} lived in harmony, their lives intertwined with the {adjective} {noun}. 
    But when the {noun} began to {verb} unpredictably, the balance of magic was threatened. 
    The quest to restore the {noun} and {verb} the {plural_noun} became a {adjective} saga of magic, mystery, and the enduring power of belief."""
    ),

    "realistic_fiction": Story(
    ["place", "noun", "verb", "adjective", "plural_noun"],
    """In the heart of {place}, a {adjective} {noun} struggled to {verb} {plural_noun}. 
    Life in {place} was not easy, and every day, the {noun} faced {adjective} challenges. 
    Yet, amid the hustle and bustle, small moments of joy shone through when the {noun} successfully {verb}ed the {plural_noun}. 
    This tale is a tribute to the {adjective} spirit of those who persevere against all odds, making their mark in the {place} with determination and grace."""
    )  
}




@app.route("/story")
def show_story():
    story_type = request.args.get("story_type", "random")
    # Generate random words if inputs are missing
    answers = {
        "place": request.args.get("place") or random_place(),
        "noun": request.args.get("noun") or random_noun(),
        "verb": request.args.get("verb") or random_verb(),
        "adjective": request.args.get("adjective") or random_adjective(),
        "plural_noun": request.args.get("plural_noun") or random_plural_noun()
    }

    if story_type == "random":
        story = choice(list(story_templates.values()))
    else:
        story = story_templates.get(story_type, default_story)

    random_title = choice(title_templates).format(**answers).upper()
    story_text = story.generate(answers)
    username = request.args.get("username", "Anonymous")

    return render_template("simple_story.html", story_text=story_text, random_title=random_title, username=username)