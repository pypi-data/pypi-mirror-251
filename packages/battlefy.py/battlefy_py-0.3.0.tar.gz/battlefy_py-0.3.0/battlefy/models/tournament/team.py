from typing import Optional, List, Any
from datetime import datetime


class Player:
    id: str
    on_team: bool
    is_free_agent: bool
    be_captain: bool
    in_game_name: str
    persistent_player_id: Optional[str]
    user_id: Optional[str]
    owner_id: str
    created_at: datetime
    updated_at: datetime
    user_slug: Optional[str]
    username: Optional[str]
    avatar_url: Optional[str]
    discord_id: Optional[str]

    def __init__(self, data: dict) -> None:
        self.id = data.get("_id")
        self.on_team = data.get("onTeam")
        self.is_free_agent = data.get("isFreeAgent")
        self.be_captain = data.get("beCaptain")
        self.in_game_name = data.get("inGameName")
        self.persistent_player_id = data.get("persistentPlayerID")
        self.user_id = data.get("userID")
        self.owner_id = data.get("ownerID")
        self.created_at = datetime.fromisoformat(data.get("createdAt"))
        self.updated_at = datetime.fromisoformat(data.get("updatedAt"))
        self.user_slug = data.get("userSlug")
        self.username = data.get("username")
        self.avatar_url = data.get("avatarUrl")
        self.discord_id = None

    def __repr__(self) -> str:
        return f"<Player id={self.id} in_game_name={self.in_game_name}>"


class CustomField:
    id: str
    value: str

    def __init__(self, data: dict) -> None:
        self.id = data.get("_id")
        self.value = data.get("value")


class PersistentTeam:
    id: str
    name: str
    logo_url: str
    short_description: str
    banner_url: str
    sponsor_banner_url: str
    created_at: datetime
    updated_at: datetime
    persistent_player_ids: List[str]
    persistent_captain_id: str
    pending_player_ids: List[Any]
    owner_id: str
    deleted_at: Optional[datetime]

    def __init__(self, data: dict) -> None:
        self.id = data.get("_id")
        self.name = data.get("name")
        self.logo_url = data.get("logoUrl")
        self.short_description = data.get("shortDescription")
        self.banner_url = data.get("bannerUrl")
        self.sponsor_banner_url = data.get("sponsorBannerUrl")
        self.created_at = datetime.fromisoformat(data.get("createdAt"))
        self.updated_at = datetime.fromisoformat(data.get("updatedAt"))
        self.persistent_player_ids = data.get("persistentPlayerIDs")
        self.persistent_captain_id = data.get("persistentCaptainID")
        self.pending_player_ids = data.get("pendingPlayerIDs")
        self.owner_id = data.get("ownerID")
        if data.get("deletedAt"):
            self.deleted_at = datetime.fromisoformat(data.get("deletedAt"))


class Team:
    id: str
    name: str
    pending_team_id: str
    persistent_team_id: str
    tournament_id: str
    user_id: str
    custom_fields: List[CustomField]
    owner_id: str
    created_at: datetime
    player_ids: List[str]
    captain_id: str
    checked_in_at: Optional[datetime]
    captain: Player
    players: List[Player]
    persistent_team: PersistentTeam

    def __init__(self, data: dict) -> None:
        self.id = data.get("_id")
        self.name = data.get("name")
        self.pending_team_id = data.get("pendingTeamID")
        self.persistent_team_id = data.get("persistentTeamID")
        self.tournament_id = data.get("tournamentID")
        self.user_id = data.get("userID")
        self.custom_fields = [CustomField(c) for c in data.get("customFields", [])]
        self.owner_id = data.get("ownerID")
        self.created_at = datetime.fromisoformat(data.get("createdAt"))
        self.player_ids = data.get("playerIDs")
        self.captain_id = data.get("captainID")
        if "checkedInAt" in data:
            self.checked_in_at = datetime.fromisoformat(data.get("checkedInAt"))
        self.captain = Player(data.get("captain"))
        self.players = [Player(p) for p in data.get("players", [])]
        self.persistent_team = PersistentTeam(data.get("persistentTeam", {}))

    def __repr__(self) -> str:
        return f"<Team id={self.id} name={self.name}>"
