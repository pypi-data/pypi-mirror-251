from dataclasses import dataclass
from typing import Any, Optional, List, TypeVar, Type, cast, Callable
from enum import Enum
from datetime import datetime
import dateutil.parser


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


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


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def is_type(t: Type[T], x: Any) -> T:
    assert isinstance(x, t)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


@dataclass
class AdminEmailSubscriptions:
    pass

    @staticmethod
    def from_dict(obj: Any) -> 'AdminEmailSubscriptions':
        assert isinstance(obj, dict)
        return AdminEmailSubscriptions()

    def to_dict(self) -> dict:
        result: dict = {}
        return result


@dataclass
class AdminEquipment:
    face: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'AdminEquipment':
        assert isinstance(obj, dict)
        face = from_union([from_str, from_none], obj.get("face"))
        return AdminEquipment(face)

    def to_dict(self) -> dict:
        result: dict = {}
        result["face"] = from_union([from_str, from_none], self.face)
        return result


@dataclass
class AdminFeatures:
    onboarded_store: Optional[bool] = None
    open_store: Optional[bool] = None
    completed_store_exit_survey: Optional[bool] = None
    new_join_info_bar: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> 'AdminFeatures':
        assert isinstance(obj, dict)
        onboarded_store = from_union([from_bool, from_none], obj.get("onboarded-store"))
        open_store = from_union([from_bool, from_none], obj.get("open-store"))
        completed_store_exit_survey = from_union([from_bool, from_none], obj.get("completed-store-exit-survey"))
        new_join_info_bar = from_union([from_bool, from_none], obj.get("new-join-info-bar"))
        return AdminFeatures(onboarded_store, open_store, completed_store_exit_survey, new_join_info_bar)

    def to_dict(self) -> dict:
        result: dict = {}
        result["onboarded-store"] = from_union([from_bool, from_none], self.onboarded_store)
        result["open-store"] = from_union([from_bool, from_none], self.open_store)
        result["completed-store-exit-survey"] = from_union([from_bool, from_none], self.completed_store_exit_survey)
        result["new-join-info-bar"] = from_union([from_bool, from_none], self.new_join_info_bar)
        return result


class Source(Enum):
    EMAIL_REGISTRATION = "email registration"
    GOOGLE_REGISTRATION = "google registration"
    REGISTRATION = "registration"
    TWITTER_REGISTRATION = "twitter registration"


@dataclass
class Admin:
    id: Optional[str] = None
    valid_email: Optional[bool] = None
    username: Optional[str] = None
    bg_url: Optional[str] = None
    auth0_user_id: Optional[str] = None
    source: Optional[Source] = None
    is_verified: Optional[bool] = None
    timezone: Optional[str] = None
    created_at: Optional[datetime] = None
    email_subscriptions: Optional[AdminEmailSubscriptions] = None
    updated_at: Optional[datetime] = None
    slug: Optional[str] = None
    equipment: Optional[AdminEquipment] = None
    features: Optional[AdminFeatures] = None
    experience_points: Optional[int] = None
    notification_sounds_enabled: Optional[bool] = None
    country_code: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Admin':
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("_id"))
        valid_email = from_union([from_bool, from_none], obj.get("validEmail"))
        username = from_union([from_str, from_none], obj.get("username"))
        bg_url = from_union([from_str, from_none], obj.get("bgUrl"))
        auth0_user_id = from_union([from_str, from_none], obj.get("auth0UserID"))
        source = from_union([Source, from_none], obj.get("source"))
        is_verified = from_union([from_bool, from_none], obj.get("isVerified"))
        timezone = from_union([from_str, from_none], obj.get("timezone"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        email_subscriptions = from_union([AdminEmailSubscriptions.from_dict, from_none], obj.get("emailSubscriptions"))
        updated_at = from_union([from_datetime, from_none], obj.get("updatedAt"))
        slug = from_union([from_str, from_none], obj.get("slug"))
        equipment = from_union([AdminEquipment.from_dict, from_none], obj.get("equipment"))
        features = from_union([AdminFeatures.from_dict, from_none], obj.get("features"))
        experience_points = from_union([from_int, from_none], obj.get("experiencePoints"))
        notification_sounds_enabled = from_union([from_bool, from_none], obj.get("notificationSoundsEnabled"))
        country_code = from_union([from_str, from_none], obj.get("countryCode"))
        return Admin(id, valid_email, username, bg_url, auth0_user_id, source, is_verified, timezone, created_at, email_subscriptions, updated_at, slug, equipment, features, experience_points, notification_sounds_enabled, country_code)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([from_str, from_none], self.id)
        result["validEmail"] = from_union([from_bool, from_none], self.valid_email)
        result["username"] = from_union([from_str, from_none], self.username)
        result["bgUrl"] = from_union([from_str, from_none], self.bg_url)
        result["auth0UserID"] = from_union([from_str, from_none], self.auth0_user_id)
        result["source"] = from_union([lambda x: to_enum(Source, x), from_none], self.source)
        result["isVerified"] = from_union([from_bool, from_none], self.is_verified)
        result["timezone"] = from_union([from_str, from_none], self.timezone)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["emailSubscriptions"] = from_union([lambda x: to_class(AdminEmailSubscriptions, x), from_none], self.email_subscriptions)
        result["updatedAt"] = from_union([lambda x: x.isoformat(), from_none], self.updated_at)
        result["slug"] = from_union([from_str, from_none], self.slug)
        result["equipment"] = from_union([lambda x: to_class(AdminEquipment, x), from_none], self.equipment)
        result["features"] = from_union([lambda x: to_class(AdminFeatures, x), from_none], self.features)
        result["experiencePoints"] = from_union([from_int, from_none], self.experience_points)
        result["notificationSoundsEnabled"] = from_union([from_bool, from_none], self.notification_sounds_enabled)
        result["countryCode"] = from_union([from_str, from_none], self.country_code)
        return result


@dataclass
class WelcomeFeatures:
    ladder: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> 'WelcomeFeatures':
        assert isinstance(obj, dict)
        ladder = from_union([from_bool, from_none], obj.get("ladder"))
        return WelcomeFeatures(ladder)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ladder"] = from_union([from_bool, from_none], self.ladder)
        return result


@dataclass
class Battlenet:
    account_id: Optional[int] = None
    battletag: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Battlenet':
        assert isinstance(obj, dict)
        account_id = from_union([from_none, lambda x: int(from_str(x))], obj.get("accountID"))
        battletag = from_union([from_str, from_none], obj.get("battletag"))
        return Battlenet(account_id, battletag)

    def to_dict(self) -> dict:
        result: dict = {}
        result["accountID"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.account_id)
        result["battletag"] = from_union([from_str, from_none], self.battletag)
        return result


@dataclass
class Discord:
    name: Optional[str] = None
    account_id: Optional[str] = None
    username: Optional[str] = None
    discriminator: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Discord':
        assert isinstance(obj, dict)
        name = from_union([from_str, from_none], obj.get("name"))
        account_id = from_union([from_str, from_none], obj.get("accountID"))
        username = from_union([from_str, from_none], obj.get("username"))
        discriminator = from_union([from_str, from_none], obj.get("discriminator"))
        return Discord(name, account_id, username, discriminator)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_union([from_str, from_none], self.name)
        result["accountID"] = from_union([from_str, from_none], self.account_id)
        result["username"] = from_union([from_str, from_none], self.username)
        result["discriminator"] = from_union([from_str, from_none], self.discriminator)
        return result


@dataclass
class RANKEDSOLO5X5:
    tier: Optional[str] = None
    division: Optional[str] = None
    last_updated_at: Optional[datetime] = None

    @staticmethod
    def from_dict(obj: Any) -> 'RANKEDSOLO5X5':
        assert isinstance(obj, dict)
        tier = from_union([from_str, from_none], obj.get("tier"))
        division = from_union([from_str, from_none], obj.get("division"))
        last_updated_at = from_union([from_datetime, from_none], obj.get("lastUpdatedAt"))
        return RANKEDSOLO5X5(tier, division, last_updated_at)

    def to_dict(self) -> dict:
        result: dict = {}
        result["tier"] = from_union([from_str, from_none], self.tier)
        result["division"] = from_union([from_str, from_none], self.division)
        result["lastUpdatedAt"] = from_union([lambda x: x.isoformat(), from_none], self.last_updated_at)
        return result


@dataclass
class LeagueOfLegends:
    region: Optional[str] = None
    encrypted_summoner_id: Optional[str] = None
    encrypted_account_id: Optional[str] = None
    summoner_name: Optional[str] = None
    last_updated_at: Optional[datetime] = None
    ranked_solo_5_x5: Optional[RANKEDSOLO5X5] = None

    @staticmethod
    def from_dict(obj: Any) -> 'LeagueOfLegends':
        assert isinstance(obj, dict)
        region = from_union([from_str, from_none], obj.get("region"))
        encrypted_summoner_id = from_union([from_str, from_none], obj.get("encryptedSummonerID"))
        encrypted_account_id = from_union([from_str, from_none], obj.get("encryptedAccountID"))
        summoner_name = from_union([from_str, from_none], obj.get("summonerName"))
        last_updated_at = from_union([from_datetime, from_none], obj.get("lastUpdatedAt"))
        ranked_solo_5_x5 = from_union([RANKEDSOLO5X5.from_dict, from_none], obj.get("RANKED_SOLO_5x5"))
        return LeagueOfLegends(region, encrypted_summoner_id, encrypted_account_id, summoner_name, last_updated_at, ranked_solo_5_x5)

    def to_dict(self) -> dict:
        result: dict = {}
        result["region"] = from_union([from_str, from_none], self.region)
        result["encryptedSummonerID"] = from_union([from_str, from_none], self.encrypted_summoner_id)
        result["encryptedAccountID"] = from_union([from_str, from_none], self.encrypted_account_id)
        result["summonerName"] = from_union([from_str, from_none], self.summoner_name)
        result["lastUpdatedAt"] = from_union([lambda x: x.isoformat(), from_none], self.last_updated_at)
        result["RANKED_SOLO_5x5"] = from_union([lambda x: to_class(RANKEDSOLO5X5, x), from_none], self.ranked_solo_5_x5)
        return result


@dataclass
class Twitter:
    screen_name: Optional[str] = None
    account_id: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Twitter':
        assert isinstance(obj, dict)
        screen_name = from_union([from_str, from_none], obj.get("screen_name"))
        account_id = from_union([from_str, from_none], obj.get("accountID"))
        return Twitter(screen_name, account_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["screen_name"] = from_union([from_str, from_none], self.screen_name)
        result["accountID"] = from_union([from_str, from_none], self.account_id)
        return result


@dataclass
class Accounts:
    twitch: Optional[str] = None
    twitter: Optional[Twitter] = None
    discord: Optional[Discord] = None
    battlenet: Optional[Battlenet] = None
    league_of_legends: Optional[LeagueOfLegends] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Accounts':
        assert isinstance(obj, dict)
        twitch = from_union([from_str, from_none], obj.get("twitch"))
        twitter = from_union([Twitter.from_dict, from_none], obj.get("twitter"))
        discord = from_union([Discord.from_dict, from_none], obj.get("discord"))
        battlenet = from_union([Battlenet.from_dict, from_none], obj.get("battlenet"))
        league_of_legends = from_union([LeagueOfLegends.from_dict, from_none], obj.get("league-of-legends"))
        return Accounts(twitch, twitter, discord, battlenet, league_of_legends)

    def to_dict(self) -> dict:
        result: dict = {}
        result["twitch"] = from_union([from_str, from_none], self.twitch)
        result["twitter"] = from_union([lambda x: to_class(Twitter, x), from_none], self.twitter)
        result["discord"] = from_union([lambda x: to_class(Discord, x), from_none], self.discord)
        result["battlenet"] = from_union([lambda x: to_class(Battlenet, x), from_none], self.battlenet)
        result["league-of-legends"] = from_union([lambda x: to_class(LeagueOfLegends, x), from_none], self.league_of_legends)
        return result


@dataclass
class ModeratorEmailSubscriptions:
    weekly_recommendations: Optional[bool] = None
    check_ins: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ModeratorEmailSubscriptions':
        assert isinstance(obj, dict)
        weekly_recommendations = from_union([from_bool, from_none], obj.get("weeklyRecommendations"))
        check_ins = from_union([from_bool, from_none], obj.get("checkIns"))
        return ModeratorEmailSubscriptions(weekly_recommendations, check_ins)

    def to_dict(self) -> dict:
        result: dict = {}
        result["weeklyRecommendations"] = from_union([from_bool, from_none], self.weekly_recommendations)
        result["checkIns"] = from_union([from_bool, from_none], self.check_ins)
        return result


@dataclass
class ModeratorEquipment:
    face: Optional[str] = None
    head: Optional[str] = None
    body: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ModeratorEquipment':
        assert isinstance(obj, dict)
        face = from_union([from_str, from_none], obj.get("face"))
        head = from_union([from_str, from_none], obj.get("head"))
        body = from_union([from_str, from_none], obj.get("body"))
        return ModeratorEquipment(face, head, body)

    def to_dict(self) -> dict:
        result: dict = {}
        result["face"] = from_union([from_str, from_none], self.face)
        result["head"] = from_union([from_str, from_none], self.head)
        result["body"] = from_union([from_str, from_none], self.body)
        return result


@dataclass
class Moderator:
    id: Optional[str] = None
    valid_email: Optional[bool] = None
    username: Optional[str] = None
    bg_url: Optional[str] = None
    auth0_user_id: Optional[str] = None
    source: Optional[Source] = None
    is_verified: Optional[bool] = None
    timezone: Optional[str] = None
    created_at: Optional[datetime] = None
    email_subscriptions: Optional[ModeratorEmailSubscriptions] = None
    updated_at: Optional[datetime] = None
    slug: Optional[str] = None
    equipment: Optional[ModeratorEquipment] = None
    features: Optional[AdminFeatures] = None
    experience_points: Optional[int] = None
    notification_sounds_enabled: Optional[bool] = None
    country_code: Optional[str] = None
    accounts: Optional[Accounts] = None
    normalized_username: Optional[str] = None
    has_seen_vgl_ad_at: Optional[datetime] = None
    has_seen_ncsa_ad_at: Optional[datetime] = None
    avatar_url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Moderator':
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("_id"))
        valid_email = from_union([from_bool, from_none], obj.get("validEmail"))
        username = from_union([from_str, from_none], obj.get("username"))
        bg_url = from_union([from_str, from_none], obj.get("bgUrl"))
        auth0_user_id = from_union([from_str, from_none], obj.get("auth0UserID"))
        source = from_union([Source, from_none], obj.get("source"))
        is_verified = from_union([from_bool, from_none], obj.get("isVerified"))
        timezone = from_union([from_str, from_none], obj.get("timezone"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        email_subscriptions = from_union([ModeratorEmailSubscriptions.from_dict, from_none], obj.get("emailSubscriptions"))
        updated_at = from_union([from_datetime, from_none], obj.get("updatedAt"))
        slug = from_union([from_str, from_none], obj.get("slug"))
        equipment = from_union([ModeratorEquipment.from_dict, from_none], obj.get("equipment"))
        features = from_union([AdminFeatures.from_dict, from_none], obj.get("features"))
        experience_points = from_union([from_int, from_none], obj.get("experiencePoints"))
        notification_sounds_enabled = from_union([from_bool, from_none], obj.get("notificationSoundsEnabled"))
        country_code = from_union([from_str, from_none], obj.get("countryCode"))
        accounts = from_union([Accounts.from_dict, from_none], obj.get("accounts"))
        normalized_username = from_union([from_str, from_none], obj.get("normalizedUsername"))
        has_seen_vgl_ad_at = from_union([from_datetime, from_none], obj.get("hasSeenVGLAdAt"))
        has_seen_ncsa_ad_at = from_union([from_datetime, from_none], obj.get("hasSeenNCSAAdAt"))
        avatar_url = from_union([from_str, from_none], obj.get("avatarUrl"))
        return Moderator(id, valid_email, username, bg_url, auth0_user_id, source, is_verified, timezone, created_at, email_subscriptions, updated_at, slug, equipment, features, experience_points, notification_sounds_enabled, country_code, accounts, normalized_username, has_seen_vgl_ad_at, has_seen_ncsa_ad_at, avatar_url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([from_str, from_none], self.id)
        result["validEmail"] = from_union([from_bool, from_none], self.valid_email)
        result["username"] = from_union([from_str, from_none], self.username)
        result["bgUrl"] = from_union([from_str, from_none], self.bg_url)
        result["auth0UserID"] = from_union([from_str, from_none], self.auth0_user_id)
        result["source"] = from_union([lambda x: to_enum(Source, x), from_none], self.source)
        result["isVerified"] = from_union([from_bool, from_none], self.is_verified)
        result["timezone"] = from_union([from_str, from_none], self.timezone)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["emailSubscriptions"] = from_union([lambda x: to_class(ModeratorEmailSubscriptions, x), from_none], self.email_subscriptions)
        result["updatedAt"] = from_union([lambda x: x.isoformat(), from_none], self.updated_at)
        result["slug"] = from_union([from_str, from_none], self.slug)
        result["equipment"] = from_union([lambda x: to_class(ModeratorEquipment, x), from_none], self.equipment)
        result["features"] = from_union([lambda x: to_class(AdminFeatures, x), from_none], self.features)
        result["experiencePoints"] = from_union([from_int, from_none], self.experience_points)
        result["notificationSoundsEnabled"] = from_union([from_bool, from_none], self.notification_sounds_enabled)
        result["countryCode"] = from_union([from_str, from_none], self.country_code)
        result["accounts"] = from_union([lambda x: to_class(Accounts, x), from_none], self.accounts)
        result["normalizedUsername"] = from_union([from_str, from_none], self.normalized_username)
        result["hasSeenVGLAdAt"] = from_union([lambda x: x.isoformat(), from_none], self.has_seen_vgl_ad_at)
        result["hasSeenNCSAAdAt"] = from_union([lambda x: x.isoformat(), from_none], self.has_seen_ncsa_ad_at)
        result["avatarUrl"] = from_union([from_str, from_none], self.avatar_url)
        return result


@dataclass
class Owner:
    id: Optional[str] = None
    valid_email: Optional[bool] = None
    username: Optional[str] = None
    bg_url: Optional[str] = None
    auth0_user_id: Optional[str] = None
    source: Optional[Source] = None
    is_verified: Optional[bool] = None
    timezone: Optional[str] = None
    created_at: Optional[datetime] = None
    email_subscriptions: Optional[AdminEmailSubscriptions] = None
    updated_at: Optional[datetime] = None
    slug: Optional[str] = None
    equipment: Optional[ModeratorEquipment] = None
    features: Optional[AdminFeatures] = None
    experience_points: Optional[int] = None
    notification_sounds_enabled: Optional[bool] = None
    country_code: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Owner':
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("_id"))
        valid_email = from_union([from_bool, from_none], obj.get("validEmail"))
        username = from_union([from_str, from_none], obj.get("username"))
        bg_url = from_union([from_str, from_none], obj.get("bgUrl"))
        auth0_user_id = from_union([from_str, from_none], obj.get("auth0UserID"))
        source = from_union([Source, from_none], obj.get("source"))
        is_verified = from_union([from_bool, from_none], obj.get("isVerified"))
        timezone = from_union([from_str, from_none], obj.get("timezone"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        email_subscriptions = from_union([AdminEmailSubscriptions.from_dict, from_none], obj.get("emailSubscriptions"))
        updated_at = from_union([from_datetime, from_none], obj.get("updatedAt"))
        slug = from_union([from_str, from_none], obj.get("slug"))
        equipment = from_union([ModeratorEquipment.from_dict, from_none], obj.get("equipment"))
        features = from_union([AdminFeatures.from_dict, from_none], obj.get("features"))
        experience_points = from_union([from_int, from_none], obj.get("experiencePoints"))
        notification_sounds_enabled = from_union([from_bool, from_none], obj.get("notificationSoundsEnabled"))
        country_code = from_union([from_str, from_none], obj.get("countryCode"))
        return Owner(id, valid_email, username, bg_url, auth0_user_id, source, is_verified, timezone, created_at, email_subscriptions, updated_at, slug, equipment, features, experience_points, notification_sounds_enabled, country_code)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([from_str, from_none], self.id)
        result["validEmail"] = from_union([from_bool, from_none], self.valid_email)
        result["username"] = from_union([from_str, from_none], self.username)
        result["bgUrl"] = from_union([from_str, from_none], self.bg_url)
        result["auth0UserID"] = from_union([from_str, from_none], self.auth0_user_id)
        result["source"] = from_union([lambda x: to_enum(Source, x), from_none], self.source)
        result["isVerified"] = from_union([from_bool, from_none], self.is_verified)
        result["timezone"] = from_union([from_str, from_none], self.timezone)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["emailSubscriptions"] = from_union([lambda x: to_class(AdminEmailSubscriptions, x), from_none], self.email_subscriptions)
        result["updatedAt"] = from_union([lambda x: x.isoformat(), from_none], self.updated_at)
        result["slug"] = from_union([from_str, from_none], self.slug)
        result["equipment"] = from_union([lambda x: to_class(ModeratorEquipment, x), from_none], self.equipment)
        result["features"] = from_union([lambda x: to_class(AdminFeatures, x), from_none], self.features)
        result["experiencePoints"] = from_union([from_int, from_none], self.experience_points)
        result["notificationSoundsEnabled"] = from_union([from_bool, from_none], self.notification_sounds_enabled)
        result["countryCode"] = from_union([from_str, from_none], self.country_code)
        return result


@dataclass
class Social:
    website_url: Optional[str] = None
    twitchtv_url: Optional[str] = None
    youtube_url: Optional[str] = None
    twitter_url: Optional[str] = None
    discord_url: Optional[str] = None
    facebook_url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Social':
        assert isinstance(obj, dict)
        website_url = from_union([from_str, from_none], obj.get("websiteUrl"))
        twitchtv_url = from_union([from_str, from_none], obj.get("twitchtvUrl"))
        youtube_url = from_union([from_str, from_none], obj.get("youtubeUrl"))
        twitter_url = from_union([from_str, from_none], obj.get("twitterUrl"))
        discord_url = from_union([from_str, from_none], obj.get("discordUrl"))
        facebook_url = from_union([from_str, from_none], obj.get("facebookUrl"))
        return Social(website_url, twitchtv_url, youtube_url, twitter_url, discord_url, facebook_url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["websiteUrl"] = from_union([from_str, from_none], self.website_url)
        result["twitchtvUrl"] = from_union([from_str, from_none], self.twitchtv_url)
        result["youtubeUrl"] = from_union([from_str, from_none], self.youtube_url)
        result["twitterUrl"] = from_union([from_str, from_none], self.twitter_url)
        result["discordUrl"] = from_union([from_str, from_none], self.discord_url)
        result["facebookUrl"] = from_union([from_str, from_none], self.facebook_url)
        return result


@dataclass
class Organization:
    id: Optional[str] = None
    name: Optional[str] = None
    owner_id: Optional[str] = None
    admin_i_ds: Optional[List[str]] = None
    moderator_i_ds: Optional[List[str]] = None
    runner_i_ds: Optional[List[Any]] = None
    features: Optional[WelcomeFeatures] = None
    created_at: Optional[datetime] = None
    service_fee_percent: Optional[int] = None
    slug: Optional[str] = None
    social: Optional[Social] = None
    logo_url: Optional[str] = None
    short_description: Optional[str] = None
    followers: Optional[int] = None
    q_score: Optional[float] = None
    banner_url: Optional[str] = None
    type: Optional[str] = None
    cloud_search_document_hash: Optional[str] = None
    cloud_search_document_last_generated: Optional[datetime] = None
    visible_tournaments: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'WelcomeElement':
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("_id"))
        name = from_union([from_str, from_none], obj.get("name"))
        owner_id = from_union([from_str, from_none], obj.get("ownerID"))
        admin_i_ds = from_union([lambda x: from_list(from_str, x), from_none], obj.get("adminIDs"))
        moderator_i_ds = from_union([lambda x: from_list(from_str, x), from_none], obj.get("moderatorIDs"))
        runner_i_ds = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("runnerIDs"))
        features = from_union([WelcomeFeatures.from_dict, from_none], obj.get("features"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        service_fee_percent = from_union([from_int, from_none], obj.get("serviceFeePercent"))
        slug = from_union([from_str, from_none], obj.get("slug"))
        social = from_union([Social.from_dict, from_none], obj.get("social"))
        logo_url = from_union([from_str, from_none], obj.get("logoUrl"))
        short_description = from_union([from_str, from_none], obj.get("shortDescription"))
        followers = from_union([from_int, from_none], obj.get("followers"))
        q_score = from_union([from_float, from_none], obj.get("qScore"))
        banner_url = from_union([from_str, from_none], obj.get("bannerUrl"))
        type = from_union([from_str, from_none], obj.get("type"))
        cloud_search_document_hash = from_union([from_str, from_none], obj.get("cloudSearchDocumentHash"))
        cloud_search_document_last_generated = from_union([from_datetime, from_none], obj.get("cloudSearchDocumentLastGenerated"))
        visible_tournaments = from_union([from_int, from_none], obj.get("visibleTournaments"))
        return Organization(id, name, owner_id, admin_i_ds, moderator_i_ds, runner_i_ds, features, created_at, service_fee_percent, slug, social, logo_url, short_description, followers, q_score, banner_url, type, cloud_search_document_hash, cloud_search_document_last_generated, visible_tournaments)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([from_str, from_none], self.id)
        result["name"] = from_union([from_str, from_none], self.name)
        result["ownerID"] = from_union([from_str, from_none], self.owner_id)
        result["adminIDs"] = from_union([lambda x: from_list(from_str, x), from_none], self.admin_i_ds)
        result["moderatorIDs"] = from_union([lambda x: from_list(from_str, x), from_none], self.moderator_i_ds)
        result["runnerIDs"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.runner_i_ds)
        result["features"] = from_union([lambda x: to_class(WelcomeFeatures, x), from_none], self.features)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["serviceFeePercent"] = from_union([from_int, from_none], self.service_fee_percent)
        result["slug"] = from_union([from_str, from_none], self.slug)
        result["social"] = from_union([lambda x: to_class(Social, x), from_none], self.social)
        result["logoUrl"] = from_union([from_str, from_none], self.logo_url)
        result["shortDescription"] = from_union([from_str, from_none], self.short_description)
        result["followers"] = from_union([from_int, from_none], self.followers)
        result["qScore"] = from_union([to_float, from_none], self.q_score)
        result["bannerUrl"] = from_union([from_str, from_none], self.banner_url)
        result["type"] = from_union([from_str, from_none], self.type)
        result["cloudSearchDocumentHash"] = from_union([from_str, from_none], self.cloud_search_document_hash)
        result["cloudSearchDocumentLastGenerated"] = from_union([lambda x: x.isoformat(), from_none], self.cloud_search_document_last_generated)
        result["visibleTournaments"] = from_union([from_int, from_none], self.visible_tournaments)
        return result


def organization_from_dict(s: Any) -> List[Organization]:
    return from_list(Organization.from_dict, s)
