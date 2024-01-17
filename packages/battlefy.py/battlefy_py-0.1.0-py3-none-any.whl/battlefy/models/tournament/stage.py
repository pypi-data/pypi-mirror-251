from datetime import datetime
from .standing import Standing
from .match import Match
from typing import List, Dict, Any


class Bracket:
    type: str
    series_style: str
    style: str
    teams_count: int
    has_third_place_match: bool
    rounds_count: int

    def __init__(self, data: dict) -> None:
        self.type = data.get("type")
        self.series_style = data.get("seriesStyle")
        self.style = data.get("style")
        self.teams_count = data.get("teamsCount")
        self.has_third_place_match = data.get("hasThirdPlaceMatch")
        self.rounds_count = data.get("roundsCount")


class Stage:
    id: str
    name: str
    start_time: datetime
    has_match_checkin: bool
    has_checkin_timer: bool
    has_confirm_score: bool
    bracket: Bracket
    created_at: datetime
    updated_at: datetime
    has_started: bool
    started_at: datetime

    standings: List[Standing]
    matches: List[Match]

    raw_matches: List[dict]
    raw_data = Dict[str, Any]

    def __init__(self, data: dict) -> None:
        self.id = data.get("_id")
        self.name = data.get("name")
        self.start_time = datetime.fromisoformat(data.get("startTime"))
        self.has_match_checkin = data.get("hasMatchCheckin")
        self.has_checkin_timer = data.get("hasCheckinTimer")
        self.has_confirm_score = data.get("hasConfirmScore")
        self.bracket = Bracket(data.get("bracket"))
        self.created_at = datetime.fromisoformat(data.get("createdAt"))
        self.updated_at = datetime.fromisoformat(data.get("updatedAt"))
        self.has_started = data.get("hasStarted")
        if "startedAt" in data:
            self.started_at = datetime.fromisoformat(data.get("startedAt"))
        self.standings = []
        self.matches = []
        self.raw_matches = []
        self.raw_data = data

    def add_standing(self, standing: Standing):
        self.standings.append(standing)

    def add_match(self, match: Match):
        self.matches.append(match)

