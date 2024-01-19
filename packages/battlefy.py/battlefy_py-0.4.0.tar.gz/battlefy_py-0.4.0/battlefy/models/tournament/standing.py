from dataclasses import dataclass, InitVar, field
from typing import Union
from .team import Team


@dataclass
class Standing:
    standing_data: InitVar[dict]
    team: Team
    set_wins: int = field(init=False, default=0)
    set_losses: int = field(init=False, default=0)
    set_ties: int = field(init=False, default=0)

    def __post_init__(self, standing_data: dict):
        self.set_wins = standing_data.get("wins", 0)
        self.set_losses = standing_data.get("losses", 0)
        self.set_ties = standing_data.get("ties", 0)


@dataclass
class LadderStanding(Standing):
    points: int = field(init=False, default=0)
    game_win_percentage: float = field(init=False, default=0.0)
    match_win_percentage: float = field(init=False, default=0.0)
    disqualified: bool = field(init=False, default=False)
    place: Union[int, None]

    def __post_init__(self, standing_data: dict):
        super().__post_init__(standing_data)
        self.points = standing_data.get("points", 0)
        self.match_win_percentage = standing_data.get("matchWinPercentage", 0)
        self.game_win_percentage = standing_data.get("gameWinPercentage", 0)


@dataclass
class SwissStanding(Standing):
    points: int = field(init=False, default=0)
    opponents_win_percentage: float = field(init=False, default=0.0)
    game_win_percentage: float = field(init=False, default=0.0)
    disqualified: bool = field(init=False, default=False)
    place: Union[int, None]

    def __post_init__(self, standing_data: dict):
        super().__post_init__(standing_data)
        self.points = standing_data.get("points", 0)
        self.opponents_win_percentage = standing_data.get("opponentsMatchWinPercentage", 0)
        self.game_win_percentage = standing_data.get("gameWinPercentage", 0)
        self.disqualified = standing_data.get("disqualified", False)
        if self.disqualified:
            self.place = None


@dataclass
class BracketStanding(Standing):
    place: int = field(init=False, default=0)

    def __post_init__(self, standing_data: dict):
        super().__post_init__(standing_data)
        self.place = standing_data.get("place", 0)

    def set_place(self, place: int):
        self.place = place

    def __repr__(self):
        return f"{self.team.name} - {self.place}"


@dataclass
class RoundRobinStanding(Standing):
    points: int = field(init=False, default=0)
    # Tiebreakers
    match_win_amongst_tied: int = field(init=False, default=0)  # rrt2
    game_win_lose_difference: int = field(init=False, default=0)  # rrt3
    total_win_lose_difference: int = field(init=False, default=0)  # rrt4

    place: Union[int, None] = field(init=False, default=0)

    def __post_init__(self, standing_data: dict):
        super().__post_init__(standing_data)
        self.points = standing_data.get("points", 0)
        self.match_win_amongst_tied = standing_data.get("rrt2", 0)
        self.game_win_lose_difference = standing_data.get("rrt3", 0)
        self.total_win_lose_difference = standing_data.get("rrt4", 0)

