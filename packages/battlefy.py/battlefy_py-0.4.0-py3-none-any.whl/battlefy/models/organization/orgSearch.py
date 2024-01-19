from enum import Enum
from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Type, cast, Callable
from datetime import datetime
import dateutil.parser


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


@dataclass
class Game:
    id: Optional[str] = None
    name: Optional[str] = None
    icon_url: Optional[str] = None
    image_url: Optional[str] = None
    background_url: Optional[str] = None
    slug: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Game':
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("_id"))
        name = from_union([from_str, from_none], obj.get("name"))
        icon_url = from_union([from_str, from_none], obj.get("iconUrl"))
        image_url = from_union([from_str, from_none], obj.get("imageUrl"))
        background_url = from_union([from_str, from_none], obj.get("backgroundUrl"))
        slug = from_union([from_str, from_none], obj.get("slug"))
        return Game(id, name, icon_url, image_url, background_url, slug)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([from_str, from_none], self.id)
        result["name"] = from_union([from_str, from_none], self.name)
        result["iconUrl"] = from_union([from_str, from_none], self.icon_url)
        result["imageUrl"] = from_union([from_str, from_none], self.image_url)
        result["backgroundUrl"] = from_union([from_str, from_none], self.background_url)
        result["slug"] = from_union([from_str, from_none], self.slug)
        return result


class Status(Enum):
    REGISTRATION_CLOSED = "registration-closed"


class TypeEnum(Enum):
    TEAM = "team"


@dataclass
class Tournament:
    id: Optional[str] = None
    start_time: Optional[datetime] = None
    players_per_team: Optional[int] = None
    name: Optional[str] = None
    banner_url: Optional[str] = None
    is_published: Optional[bool] = None
    is_public: Optional[bool] = None
    registration_enabled: Optional[bool] = None
    slug: Optional[str] = None
    game_id: Optional[str] = None
    game: Optional[Game] = None
    teams_count: Optional[int] = None
    status: Optional[Status] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Tournament':
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("_id"))
        start_time = from_union([from_datetime, from_none], obj.get("startTime"))
        players_per_team = from_union([from_int, from_none], obj.get("playersPerTeam"))
        name = from_union([from_str, from_none], obj.get("name"))
        banner_url = from_union([from_str, from_none], obj.get("bannerUrl"))
        is_published = from_union([from_bool, from_none], obj.get("isPublished"))
        is_public = from_union([from_bool, from_none], obj.get("isPublic"))
        registration_enabled = from_union([from_bool, from_none], obj.get("registrationEnabled"))
        slug = from_union([from_str, from_none], obj.get("slug"))
        game_id = from_union([from_str, from_none], obj.get("gameID"))
        game = from_union([Game.from_dict, from_none], obj.get("game"))
        teams_count = from_union([from_int, from_none], obj.get("teamsCount"))
        status = from_union([Status, from_none], obj.get("status"))
        return Tournament(id, start_time, players_per_team, name, banner_url, is_published, is_public, registration_enabled, slug, game_id, game, teams_count, status)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([from_str, from_none], self.id)
        result["startTime"] = from_union([lambda x: x.isoformat(), from_none], self.start_time)
        result["playersPerTeam"] = from_union([from_int, from_none], self.players_per_team)
        result["name"] = from_union([from_str, from_none], self.name)
        result["bannerUrl"] = from_union([from_str, from_none], self.banner_url)
        result["isPublished"] = from_union([from_bool, from_none], self.is_published)
        result["isPublic"] = from_union([from_bool, from_none], self.is_public)
        result["registrationEnabled"] = from_union([from_bool, from_none], self.registration_enabled)
        result["slug"] = from_union([from_str, from_none], self.slug)
        result["gameID"] = from_union([from_str, from_none], self.game_id)
        result["game"] = from_union([lambda x: to_class(Game, x), from_none], self.game)
        result["teamsCount"] = from_union([from_int, from_none], self.teams_count)
        result["status"] = from_union([lambda x: to_enum(Status, x), from_none], self.status)
        return result


@dataclass
class OrgSearch:
    total: int
    tournaments: List[Tournament]

    @staticmethod
    def from_dict(obj: Any) -> 'Welcome':
        assert isinstance(obj, dict)
        total = from_int(obj.get("total"))
        tournaments = from_list(Tournament.from_dict, obj.get("tournaments"))
        return OrgSearch(total, tournaments)

    def to_dict(self) -> dict:
        result: dict = {}
        result["total"] = from_int(self.total)
        result["tournaments"] = from_list(lambda x: to_class(Tournament, x), self.tournaments)
        return result


def org_search_from_dict(s: Any) -> OrgSearch:
    return OrgSearch.from_dict(s)


def tournaments_from_org_search(tournaments: List):
    return from_list(Tournament.from_dict, tournaments)
