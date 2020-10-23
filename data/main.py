from data.state_machine import StateMachine
from data.states import intro_screen, game


def main():
    state_dict = {'INTRO': intro_screen.IntroScreen(),
                  'GAME': game.Game()}
    sm = StateMachine(state_dict, 'INTRO')
    sm.main_loop()
