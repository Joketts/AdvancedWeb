# cyoa_game.py

class CYOAGame:
    def __init__(self, story):
        self.story = story
        self.current_page = 'start'  # Initial page
        self.previous_page = None

    def get_current_page_content(self):
        return self.story[self.current_page]

    def make_choice(self, choice_name):
        current_page = self.story[self.current_page]
        if choice_name in current_page['choices']:
            self.previous_page = self.current_page
            self.current_page = current_page['choices'][choice_name]
            return self.get_current_page_content()
        else:
            return None

    def go_back(self):
        if self.previous_page:
            self.current_page, self.previous_page = self.previous_page, None  # Swap current and previous
            return {'text': self.story[self.current_page]['text'], 'choices': self.story[self.current_page]['choices']}
        else:
            return None  # No previous page, cannot go back



# Your story dictionary containing pages and choices
story = {
    'start': {
        'text': "You wake up in a clearing, surrounded by dense forest. The air is thick with an unknown scent, "
                "and a sense of urgency fills your heart. What do you do?",
        'choices': {
            'Head into the woods': 'wood_path',
            'Head to the mountains': 'mount_path'
        }
    },
    'wood_path': {
        'text': "As you venture into the woods, you hear rustling nearby. A figure emerges from the shadows.",
        'choices': {
            'Approach the figure': 'encounter_stranger',
            'Continue deeper into the woods': 'wood_deeper'
        }
    },
    'encounter_stranger': {
        'text': "The figure reveals itself to be a traveler. They seem wary but not hostile.",
        'choices': {
            'Strike up a conversation': 'conversation_traveler',
            'Prepare for a fight': 'fight_traveler'
        }
    },
    'conversation_traveler': {
        'text': "You engage in conversation and learn about the dangers of the forest. The traveler offers you advice "
                "before parting ways.",
        'choices': {
            'Continue deeper into wood': 'wood_deeper',
            'Slap him': 'fight_traveler'
        }
    },
    'fight_traveler': {
        'text': "The traveler takes a defensive stance. Will you fight or try to diffuse the situation?",
        'choices': {
            'Fight the traveler': 'battle_traveler',
            'Try to calm the situation': 'calm_traveler'
        }
    },
    'battle_traveler': {
        'text': "You engage in a tense battle with the traveler!",
        'choices': {
            'You Won': 'Loot traveler',
            'You lost': 'End',
        }
    },
    'calm_traveler': {
        'text': "You manage to defuse the tension. The traveler nods in appreciation and walks away.",
        'choices': {
            'Part ways and continue exploring': 'wood_deeper'
        }
    },
    'End': {
        'text': "Congratulations, you died",
        'choices': {}
    }
}

# ... add more pages as needed
