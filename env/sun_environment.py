from pettingzoo import AECEnv
from pettingzoo.utils import BaseWrapper

from gymnasium.spaces import Discrete, MultiBinary, Dict

import numpy as np

from .sun import *
from .card import *

ROUND_REWARD_COEFF = 0.1

cards: tuple[Card, ...] = tuple([Card(rank, suit) for rank in ranks for suit in suits])
idx_to_card: dict[int, Card] = dict(zip(range(32), cards))
card_to_idx: dict[Card, int] = dict(zip(cards, range(32)))

class SunEnv(AECEnv):
    game: Sun
    metadata = {
        "name": "sun_environment_v0",
    }
    def __init__(self) -> None:
        super().__init__()

        self.possible_agents = [0, 1, 2, 3]
        self.agents = [0, 1, 2, 3]

        # 4 rows of 32 binary flags
        # 1 row for the agent's current hand
        # 3 rows for the card played by every other player (all 0s if they did not play yet)
        self.observation_spaces = {
            agent:Dict(
                {
                    "observation":MultiBinary((4, 32)),
                    "action_mask":MultiBinary((32,))
                }
            )
            for agent in self.agents
        }

        # which if the 32 cards the agent intends to play
        self.action_spaces = {agent: Discrete(32) for agent in self.agents}

        # defining stuff to pass tests
        self.infos = {agent: {} for agent in self.agents}

    def reset(self, seed: int | None = None, options=None) -> None:
        self.game = Sun(seed=seed)
        self.possible_agents = [0, 1, 2, 3]
        self.agents = [0, 1, 2, 3]

        self.observation_spaces = {
            agent:Dict(
                {
                    "observation":MultiBinary((4, 32)),
                    "action_mask":MultiBinary((32,))
                }
            )
            for agent in self.agents
        }

        # which if the 32 cards the agent intends to play
        self.action_spaces = {agent: Discrete(32) for agent in self.agents}

        # defining stuff to pass tests
        self.infos = {agent: {} for agent in self.agents}
        

        self.agent_selection = self.game.next_player

        self.rewards = {agent: 0 for agent in self.agents}
        self._cumulative_rewards = {agent: 0 for agent in self.agents}
        self.terminations = {agent: False for agent in self.agents}
        self.truncations = {agent: False for agent in self.agents}

    def observe(self, agent: int) -> dict[str, np.ndarray]:
        # if agent != self.game.next_player:
            
        #     raise NotImplementedError(f"Agent {agent} is observing, while agent {self.game.next_player} is playing next. \
        #                               Observing for the player that's not playing next is not supported yet.")

        observation = np.zeros((4, 32), dtype="int8")

        # set the corresponding flag of every card in the agent's hand to 1
        for card in self.game.player_hands[agent]:
            observation[0][card_to_idx[card]] = 1

        # idk how to explain this, it just works
        # it sets the corresponding flag 1
        for i, (_, card) in enumerate(self.game.cards_played[-1::-1]):
            observation[i][card_to_idx[card]] = 1

        action_mask = [0]*32
        for card in self.game.possible_moves():
            action_mask[card_to_idx[card]] = 1

        return {"observation": observation, "action_mask":np.array(action_mask, dtype="int8")}

    def step(self, action: int) -> None:
        # if game is ended or truncated, it's a dead-step
        # this should probably never happen, when training we're most likely going
        # to check if the game has terminated before acting
        # i added a print to check if it ever happens
        if (
            self.terminations[self.agent_selection]
            or self.truncations[self.agent_selection]
        ):
            return self._was_dead_step(action)
        
        self._cumulative_rewards[self.agent_selection] = 0
        
        # check if this is the last play of the round
        end_of_round = len(self.game.cards_played) == 3
        
        if end_of_round:
            # save the prev score for reward calculation
            # this works, 0, and 2 will be the first team, 1 and 3 will be the second team
            prev_score = self.game.score.copy()

        chosen_card = idx_to_card[action]
        assert chosen_card in self.game.possible_moves()
        self.game.play(chosen_card)

        # if this is the last play of the round, reward agents accordingly
        if end_of_round:
            # award the round-winning team their difference in points
            # the losing team will get a reward of 0
            team_0_score = self.game.score[0] - prev_score[0]
            team_1_score = self.game.score[1] - prev_score[1]
            self.rewards[0], self.rewards[2] = team_0_score, team_0_score
            self.rewards[1], self.rewards[3] = team_1_score, team_1_score
        else: # otherwise, the rewards are 0
            for agent in self.agents:
                self.rewards[agent] = 0
        
        self._accumulate_rewards()

        # if the game ended, terminate for all agents
        if self.game.game_ended():
            for agent in self.agents:
                self.terminations[agent] = True

        # switch control to the next player
        self.agent_selection = self.game.next_player

    def observation_space(self, agent):
        return self.observation_spaces[agent]
    
    def action_space(self, agent):
        return self.action_spaces[agent]
    
    def close(self) -> None:
        del self.game

class HistoryWrapper(BaseWrapper):
    """
    Saves the history of a SunEnv game. Useful for rendering.

    `self.history` dict[str, list]: Contains all information about how the game was played:
        - `self.history.rounds` list[list[Card]]: Every card played per round in chronological order
        - `self.history.players` list[int]: Player who starts the round
        - `self.history.player_hands` list[list[Card]]: List containing initial hands of all players
    """
    history: dict[str, list]
    
    def __init__(self, env: SunEnv):
        super().__init__(env)
        self.env = env
    
    def reset(self, seed: int | None = None, options=None) -> None:
        """Resets environment and history dict."""
        self.env.reset(seed=seed, options=options)
        
        self.history = {
            "player_hands": [hand.copy() for hand in self.env.game.player_hands],
            "players": [0],
            "rounds": [],
            "scores": [],
        }

    def step(self, action: int) -> None:
        """
        Steps the environment, and saves the cards played and the 
        next player to the history dict."""
        end_of_round = len(self.game.cards_played) == 3
        # if this is the last play of the round
        if end_of_round:
            # record the 3 cards played in history (before slef.env.game clears it)
            self.history["rounds"].append([card for _, card in self.env.game.cards_played])
            # add the next card played
            self.history["rounds"][-1].append(idx_to_card[action])
        
        # call the original step method
        self.env.step(action)
        
        # if the round ended, add the score after the environment updated it
        if end_of_round:
            self.history["scores"].append(self.env.game.score.copy())

            # if the round ended, add the player who plays next to history["players"]
            # don't add if rounds played is already 8 (the game is over, no next player)
            if self.env.game.rounds_played < 8:
                self.history["players"].append(self.agent_selection)
