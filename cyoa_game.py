# cyoa_game.py

from Database import db, PlayerProgress


class CYOAGame:
    def __init__(self, story):
        self.story = story
        self.reset = 'start'
        self.current_page = 'start'  # Initial page
        self.previous_page = None
        self.vial_power = 0
        self.runes_power = 0
        self.token_power = 0

    def get_current_page_content(self):
        return self.story[self.current_page]

    def make_choice(self, choice_name):
        current_page = self.story[self.current_page]
        if choice_name in current_page['choices']:
            self.previous_page = self.current_page
            self.current_page = current_page['choices'][choice_name]
            if self.current_page == 'drink_liquid':
                self.vial_power = 1
            elif self.current_page == 'embrace_power':
                self.runes_power = 1
            elif self.current_page == 'keep_token':
                self.token_power = 1

            # check for end of game
            if self.current_page in ('Win', 'End'):
                return {
                    'page_text': current_page['text'],
                    'choices': current_page['choices'],
                    'game_ended': True,
                    'collected_items': {
                        'Vial': self.vial_power,
                        'Runes power': self.runes_power,
                        'Token': self.token_power
                    }
                }

            return self.get_current_page_content()
        else:
            return None

    def save_progress(self, player_id):
        progress = PlayerProgress.query.filter_by(player_id=player_id).first()
        if not progress:
            progress = PlayerProgress(player_id=player_id)
        progress.current_page = self.current_page
        progress.vial_power = self.vial_power
        progress.runes_power = self.runes_power
        progress.token_power = self.token_power
        db.session.add(progress)
        db.session.commit()

    def load_progress(self, player_id):
        progress = PlayerProgress.query.filter_by(player_id=player_id).first()
        if progress:
            self.current_page = progress.current_page
            self.vial_power = progress.vial_power
            self.runes_power = progress.runes_power
            self.token_power = progress.token_power
            return self.get_current_page_content()

    def reset_game(self):
        self.current_page = self.reset  # Set current_page back to the starting page
        self.previous_page = None
        self.vial_power = 0  # Reset acquired flags
        self.runes_power = 0
        self.token_power = 0
        return self.get_current_page_content()
        # Reset previous_page to None


# Your story dictionary containing pages and choices
story = {
    'start': {
        'text': "You wake up in a clearing, surrounded by dense forest. The air is thick with an unknown scent, "
                "and a sense of urgency fills your heart. What do you do?",
        'choices': {
            'Head into the woods': 'wood_path',
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
            'lured into a false sense of safety, you attack': 'fight_traveler'
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
            'after a long fight you defeat the traveler': 'loot_traveler',
        }
    },
    'calm_traveler': {
        'text': "You manage to defuse the tension. The traveler nods in appreciation and walks away.",
        'choices': {
            'Part ways and continue exploring': 'wood_deeper'
        }
    },
    'loot_traveler': {
        'text': "you search the traveler's belongings. you a vial of shimmering liquid, What do you do?",
        'choices': {
            'You dont trust the shimmering liquid leave quickly': 'wood_deeper',
            'Inspect the vial': 'inspect_vial'
        }
    },
    'inspect_vial': {
        'text': "The vial emits a faint glow, Do you drink it or keep it for trade?",
        'choices': {
            'Drink the liquid': 'drink_liquid',
            'Keep it for trade': 'keep_vial'
        }
    },
    'drink_liquid': {
        'text': "A surge of energy courses through you, heightening your senses and granting you temporary agility.",
        'choices': {
            'Continue exploring': 'wood_deeper'
        }
    },
    'keep_vial': {
        'text': "You stash the vial safely, deciding to keep it for a more opportune moment.",
        'choices': {
            'Continue exploring': 'wood_deeper'
        }
    },
    'wood_deeper': {
        'text': "As you continue deeper into the woods, "
                "you sense a change in the atmosphere. The foliage becomes thicker, "
                "and an eerie silence settles around you. Suddenly, you stumble upon an ancient-looking altar covered "
                "in glowing runes.",
        'choices': {
            'Inspect the altar closely': 'inspect_altar',
            'Bypass the altar and move forward': 'move_forward'
        }
    },
    'inspect_altar': {
        'text': "The runes on the altar seem to pulse with a faint light. What action will you take?",
        'choices': {
            'Attempt to decipher the runes': 'decipher_runes',
            'Touch the runes': 'touch_runes'
        }
    },
    'touch_runes': {
        'text': "The runes are cold to the touch, nothing happened.",
        'choices': {
            'Attempt to decipher the runes': 'decipher_runes',
            'continue on': 'move_forward'
        }
    },
    'decipher_runes': {
        'text': "As you concentrate on deciphering the runes,"
                " their meaning slowly becomes clear. They speak of an ancient "
                "ritual that could grant great power but at a cost. What will you do?",
        'choices': {
            'Perform the ritual': 'perform_ritual',
            'Move away from the altar': 'move_away'
        }
    },
    'move_away': {
        'text': "not trusting these old runes, you move on quickly",
        'choices': {
            'continue on': 'move_forward'
        }
    },
    'perform_ritual': {
        'text': "You decide to perform the ritual. "
                "The runes glow brighter as you feel a surge of power coursing through "
                "you. However, a chilling sensation hints at an unforeseen consequence.",
        'choices': {
            'Embrace the power': 'embrace_power',
            'Resist and move away': 'resist_power'
        }
    },
    'embrace_power': {
        'text': "You embrace the newfound power completely. "
                "Your abilities amplify, but an unsettling darkness lingers within you.",
        'choices': {
            'Continue journey with newfound power': 'follow_melody'
        }
    },
    'resist_power': {
        'text': "You resist the temptation of the power offered by the ritual. But the runes don't let you"
                "upset you tried to refute their power, the runes break apart,"
                "sending a rock directly into your skull",
        'choices': {
            'You died': 'End'
        }
    },
    'move_forward': {
        'text': "You decide to bypass the altar and continue forward."
                " The woods grow denser, and the path becomes narrower. "
                "A faint, otherworldly melody fills the air, drawing you toward it.",
        'choices': {
            'Follow the melody': 'follow_melody',
            'Stay cautious, dangers may be around': 'continue_journey'
        }
    },
    'follow_melody': {
        'text': "As you follow the mesmerizing melody, you stumble upon a hidden grove. Ethereal beings dance in a "
                "luminescent circle. They seem unaware of your presence.",
        'choices': {
            'Observe quietly': 'observe_quietly',
            'Join the dance': 'join_dance'
        }
    },
    'observe_quietly': {
        'text': "You silently observe the ethereal beings, mesmerized by their graceful movements. After a while, "
                "they vanish into thin air, leaving behind a faint, lingering energy.",
        'choices': {
            'Proceed with newfound energy': 'proceed_energy'
        }
    },
    'join_dance': {
        'text': "You join the dance, matching their steps. The beings welcome you, and for a fleeting moment, "
                "you feel connected to something ancient and mystical. As they fade away, they leave you with "
                "a sense of rejuvenation and a mysterious token.",
        'choices': {
            'Inspect the token': 'inspect_token'
        }
    },
    'inspect_token': {
        'text': "The token radiates an otherworldly aura. What will you do with it?",
        'choices': {
            'Keep it close': 'keep_token',
            'Leave it behind': 'leave_token'
        }
    },
    'keep_token': {
        'text': "You decide to keep the token, feeling its mystical energy resonate with your own. It might prove "
                "useful on your journey.",
        'choices': {
            'Continue exploring': 'continue_journey'
        }
    },
    'leave_token': {
        'text': "You leave the token behind, unsure of its purpose or significance. The mystical energy fades away "
                "as you continue your journey.",
        'choices': {
            'Continue exploring': 'continue_journey'
        }
    },
    'proceed_energy': {
        'text': "Empowered by the energy of the grove, you feel invigorated as you continue your journey deeper into "
                "the mysterious woods.",
        'choices': {
            'Continue exploring': 'continue_journey'
        }
    },
    'continue_journey': {
        'text': "With your decisions made, you carry on with your journey, the mysteries of the forest unfolding "
                "before you. Suddenly, you encounter a massive ogre blocking the path ahead.",
        'choices': {
            'Attempt to sneak past the ogre': 'sneak_past',
            'Confront the ogre': 'confront_ogre'
        }
    },
    'sneak_past': {
        'text': "You cautiously try to sneak past the ogre, but its keen senses detect your presence. "
                "It roars and charges toward you, forcing a confrontation!",
        'choices': {
            'Prepare to fight': 'prepare_fight'
        }
    },
    'confront_ogre': {
        'text': "You decide to confront the ogre directly. It snarls, readying its massive club for an attack.",
        'choices': {
            'Initiate the fight': 'initiate_fight'
        }
    },
    'prepare_fight': {
        'text': "The ogre charges at you, leaving no choice but to prepare for a fight!",
        'choices': {
            'Fight the ogre': 'initiate_fight'
        }
    },
    'initiate_fight': {
        'text': "The confrontation escalates into a fierce battle between you and the ogre!"
                "The ogre tried to strike but your movement outmatches him",
        'choices': {
            'Your sword strikes through his neck': 'Win'
        }
    },
    'Win': {
        'text': "Congratulations, you defeated the ogre",
        'choices': {},
    },
    'End': {
        'text': "Congratulations, you died",
        'choices': {}
    }
}
