import asyncio
import aiohttp
from typing import Optional, List, Union

from .models import Tournament, Stage, Match, SwissStanding, LadderStanding, BracketStanding, RoundRobinStanding


class TournamentClient:
    def __init__(self, headers: dict = None):
        self.headers = headers or {}

    @staticmethod
    def get_bracket_rankings(no_teams: int, is_double_elim: bool, third_place: Union[bool, None] = None) -> List[int]:
        """
        Get the rankings for a bracket
        :param third_place: If there's a third place match (for single elimination)
        :param is_double_elim: if bracket is double elimination
        :param no_teams: number of teams in bracket
        :return: the ranking boundaries for the bracket
        """
        rank = (2 ** (no_teams - 1).bit_length())
        return_list = []
        if not is_double_elim:
            if third_place:
                return_list = return_list + [4, 3, 2, 1]
            else:
                return_list = return_list + [2, 1]
            while rank > return_list[0]:
                rank = int(rank // 2)
                return_list.append(rank + 1)
        else:
            return_list = return_list + [4, 3, 2, 1]
            subtractor = int(rank // 4)
            while subtractor >= 2:
                rank = rank - subtractor
                return_list.append(rank + 1)
                rank = rank - subtractor
                return_list.append(rank + 1)
                subtractor = int(subtractor // 2)
        return_list.sort(reverse=True)
        return return_list

    async def __fallback_get_elimination_standing(self, stage_data: Stage, tournament_data: Tournament) -> Stage:
        team_standings = {}
        placement_data = {}
        for team in tournament_data.teams:
            team_standings[team.persistent_team_id] = BracketStanding({}, team)
        for match in stage_data.raw_matches:
            try:
                if ("team" in match.get("top", {})) and "team" in match.get("bottom", {}):
                    top_winner = match.get("top", {}).get("winner", False)
                    bottom_winner = match.get("bottom", {}).get("winner", False)
                    if top_winner:
                        team_standings[match["bottom"]["team"]["persistentTeamID"]].set_losses += 1
                        team_standings[match["top"]["team"]["persistentTeamID"]].set_wins += 1
                    elif bottom_winner:
                        team_standings[match["top"]["team"]["persistentTeamID"]].set_losses += 1
                        team_standings[match["bottom"]["team"]["persistentTeamID"]].set_wins += 1
                    else:
                        team_standings[match["top"]["team"]["persistentTeamID"]].set_ties += 1
                        team_standings[match["bottom"]["team"]["persistentTeamID"]].set_ties += 1
            except Exception:
                continue
        if stage_data.bracket.style == "double":
            # Double elimination
            rankings = self.get_bracket_rankings(stage_data.bracket.teams_count, True)
            for r in range(len(rankings)):
                placement_data[r + 1] = []
            for match in stage_data.raw_matches:
                try:
                    if match.get("inConsolationBracket", False):
                        if match["top"]["winner"]:
                            placement_data[match["roundNumber"]].append(match["bottom"]["team"]["persistentTeamID"])
                        elif match["bottom"]["winner"]:
                            placement_data[match["roundNumber"]].append(match["top"]["team"]["persistentTeamID"])
                        else:
                            placement_data[match["roundNumber"]].append(match["top"]["team"]["persistentTeamID"])
                            placement_data[match["roundNumber"]].append(match["bottom"]["team"]["persistentTeamID"])
                except Exception:
                    continue
            match = stage_data.raw_matches[-1]
            if match.get('top', {}).get('team', {}) and match.get('bottom', {}).get('team', {}):
                top_index = len(rankings)
                if match["top"]["winner"]:
                    placement_data[top_index].append(match["top"]["team"]["persistentTeamID"])
                    placement_data[top_index - 1].append(match["bottom"]["team"]["persistentTeamID"])
                elif match["bottom"]["winner"]:
                    placement_data[top_index].append(match["bottom"]["team"]["persistentTeamID"])
                    placement_data[top_index - 1].append(match["top"]["team"]["persistentTeamID"])
                else:
                    placement_data[top_index - 1].append(match["top"]["team"]["persistentTeamID"])
                    placement_data[top_index - 1].append(match["bottom"]["team"]["persistentTeamID"])
        elif stage_data.bracket.style == "single":
            rankings = self.get_bracket_rankings(stage_data.bracket.teams_count, False,
                                                 stage_data.bracket.has_third_place_match)
            for r in range(len(rankings)):
                placement_data[r + 1] = []
            for match in stage_data.raw_matches:
                try:
                    if ("team" in match.get("top", {})) and "team" in match.get("bottom", {}):
                        if not match.get("matchType", "") == "loser":
                            if match.get("roundNumber", 0) == stage_data.bracket.rounds_count:
                                first = len(rankings)
                                second = len(rankings) - 1
                                if match["top"]["winner"]:
                                    placement_data[first].append(match["top"]["team"]["persistentTeamID"])
                                    placement_data[second].append(match["bottom"]["team"]["persistentTeamID"])
                                elif match["bottom"]["winner"]:
                                    placement_data[second].append(match["top"]["team"]["persistentTeamID"])
                                    placement_data[first].append(match["bottom"]["team"]["persistentTeamID"])
                                else:
                                    placement_data[second].append(match["top"]["team"]["persistentTeamID"])
                                    placement_data[second].append(match["bottom"]["team"]["persistentTeamID"])
                            else:
                                # Skip round 2 if we have a third place match
                                if stage_data.bracket.has_third_place_match:
                                    if match.get("roundNumber", 0) == stage_data.bracket.rounds_count - 1:
                                        continue
                                placement_number = match.get("roundNumber", 0)
                                if match["top"]["winner"]:
                                    placement_data[placement_number].append(match["bottom"]["team"]["persistentTeamID"])
                                elif match["bottom"]["winner"]:
                                    placement_data[placement_number].append(match["top"]["team"]["persistentTeamID"])
                                else:
                                    placement_data[placement_number].append(match["top"]["team"]["persistentTeamID"])
                                    placement_data[placement_number].append(match["bottom"]["team"]["persistentTeamID"])
                        else:  # In a 3rd place match
                            third = len(rankings)-2
                            fourth = len(rankings)-3
                            if match["top"]["winner"]:
                                placement_data[third].append(match["top"]["team"]["persistentTeamID"])
                                placement_data[fourth].append(match["bottom"]["team"]["persistentTeamID"])
                            elif match["bottom"]["winner"]:
                                placement_data[third].append(match["bottom"]["team"]["persistentTeamID"])
                                placement_data[fourth].append(match["top"]["team"]["persistentTeamID"])
                            else:
                                placement_data[fourth].append(match["top"]["team"]["persistentTeamID"])
                                placement_data[fourth].append(match["bottom"]["team"]["persistentTeamID"])
                except Exception:
                    continue
        else:
            raise ValueError(f"Invalid bracket style {stage_data.bracket.style}")
        for key, value in placement_data.items():
            set_value = list(set(value))  # Remove duplicate teams in a round
            for team_id in set_value:
                team_standings[team_id].set_place(rankings[key - 1])
                stage_data.add_standing(team_standings[team_id])
        return stage_data

    async def __get_elimination_standing(self, stage_data: Stage, tournament_data: Tournament) -> Stage:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"https://dtmwra1jsgyb0.cloudfront.net/stages/{stage_data.id}/standings",
                    headers=self.headers) as resp:
                if resp.status != 200:
                    raise ValueError(f"Invalid ID {stage_data.id}")
                standing_data = await resp.json()
                if (not standing_data) or ("wins" not in standing_data[0]):
                    return await self.__fallback_get_elimination_standing(stage_data, tournament_data)
                for standing in standing_data:
                    stage_data.add_standing(
                        BracketStanding(standing, tournament_data.get_team_from_team_id(standing["teamID"])))
        return stage_data

    async def __get_ladder_standing(self, stage_data: Stage, tournament_data: Tournament) -> Stage:
        # Get placements data
        placement = {}
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"https://dtmwra1jsgyb0.cloudfront.net/stages/{stage_data.id}/ladder-standings",
                    headers=self.headers) as resp:
                if resp.status != 200:
                    raise ValueError(f"Invalid ID {stage_data.id}")
                initial_data = await resp.json()
                pages = initial_data["total"] // 10 + 1
                for x in range(len(initial_data["standings"])):
                    placement[initial_data["standings"][x]["teamID"]] = x + 1
                for page in range(1, pages + 1):
                    skip = page * 10
                    async with session.get(
                            f"https://dtmwra1jsgyb0.cloudfront.net/stages/{stage_data.id}/ladder-standings?filter=all&skip={skip}&limit=10",
                            headers=self.headers) as resp:
                        if resp.status != 200:
                            raise ValueError(f"Invalid ID {stage_data.id}")
                        data = await resp.json()
                        for x in range(len(data["standings"])):
                            placement[data["standings"][x]["teamID"]] = x + 1 + skip
            # Get standing data
            async with session.get(
                    f"https://dtmwra1jsgyb0.cloudfront.net/stages/{stage_data.id}/latest-round-standings",
                    headers=self.headers) as resp:
                if resp.status != 200:
                    raise ValueError(f"Invalid ID {stage_data.id}")
                standing_data = await resp.json()
                for standing in standing_data:
                    stage_data.add_standing(
                        LadderStanding(standing, tournament_data.get_team_from_team_id(standing["teamID"]),
                                       placement.get(standing["teamID"], None)))
        return stage_data

    async def __get_swiss_standings(self, stage_data: Stage, tournament_data: Tournament) -> Stage:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"https://dtmwra1jsgyb0.cloudfront.net/stages/{stage_data.id}/latest-round-standings",
                    headers=self.headers) as resp:
                if resp.status != 200:
                    raise ValueError(f"Invalid ID {stage_data.id}")
                standing_data = await resp.json()
                # Sort placement for completed and DNF
                completed = []
                dnf = []
                for standing in standing_data:
                    if standing["disqualified"]:
                        dnf.append(standing)
                    else:
                        completed.append(standing)
                standing_data = completed + dnf
                for n in range(len(standing_data)):
                    standing = standing_data[n]
                    if "teamID" in standing:
                        stage_data.add_standing(
                            SwissStanding(standing, tournament_data.get_team_from_team_id(standing["teamID"]), n + 1))
        return stage_data

    async def __get_round_robin_standings(self, stage_data: Stage, tournament_data: Tournament) -> Stage:
        async with aiohttp.ClientSession() as session:
            team_standings: dict = {}
            # Load standings data into players
            async with session.get(
                    f"https://dtmwra1jsgyb0.cloudfront.net/stages/{stage_data.id}/standings",
                    headers=self.headers) as resp:
                if resp.status != 200:
                    raise ValueError(f"Invalid ID {stage_data.id}")
                standing_data = await resp.json()
                for standing in standing_data:
                    standing = RoundRobinStanding(standing, tournament_data.get_team_from_team_id(standing["teamID"]))
                    stage_data.add_standing(standing)
                    team_standings[standing.team.id] = standing
            # Get RR groups
            groups: List[List[RoundRobinStanding]] = []
            async with session.get(
                    f"https://api.battlefy.com/stages/{stage_data.id}?extend%5Bgroups%5D%5Bteams%5D=true",
                    headers=self.headers) as resp:
                if resp.status != 200:
                    raise ValueError(f"Invalid ID {stage_data.id}")
                group_request = await resp.json()
                for group in group_request[0]["groups"]:
                    working_group = []
                    for team in group["teamIDs"]:
                        working_group.append(team_standings[team])
                    groups.append(working_group)
        #  Calculate RR standings
        for rr_group in groups:
            sorted_group = sorted(rr_group, key=lambda x: (x.points, x.set_wins, x.match_win_amongst_tied,
                                                           x.game_win_lose_difference, x.total_win_lose_difference),
                                  reverse=True)
            for n in range(len(sorted_group)):
                sorted_group[n].place = n + 1
                if n > 0:
                    if sorted_group[n].set_wins == sorted_group[n - 1].set_wins and \
                            sorted_group[n].match_win_amongst_tied == sorted_group[n - 1].match_win_amongst_tied and \
                            sorted_group[n].game_win_lose_difference == sorted_group[n - 1].game_win_lose_difference and \
                            sorted_group[n].total_win_lose_difference == sorted_group[n - 1].total_win_lose_difference:
                        sorted_group[n].place = sorted_group[n - 1].place
        return stage_data

    async def __get_standings(self, stage_data: Stage, tournament_data: Tournament) -> Stage:
        if stage_data.bracket.type == "elimination":
            return await self.__get_elimination_standing(stage_data, tournament_data)
        elif stage_data.bracket.type == "swiss":
            return await self.__get_swiss_standings(stage_data, tournament_data)
        elif stage_data.bracket.type == "ladder":
            return await self.__get_ladder_standing(stage_data, tournament_data)
        elif stage_data.bracket.type == "roundrobin":
            return await self.__get_round_robin_standings(stage_data, tournament_data)
        else:
            raise ValueError(f"Invalid stage type {stage_data.bracket.type}")

    async def __get_additional_data(self, stage_data: Stage, tournament_data: Tournament) -> Stage:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"https://api.battlefy.com/stages/{stage_data.id}?extend[matches][top.team][players][user]=true&extend[matches][top.team][persistentTeam]=true&extend[matches][bottom.team][players][user]=true&extend[matches][bottom.team][persistentTeam]=true&extend[groups][teams]=true&extend[groups][matches][top.team][players][user]=true&extend[groups][matches][top.team][persistentTeam]=true&extend[groups][matches][bottom.team][players][user]=true&extend[groups][matches][bottom.team][persistentTeam]=true",
                    headers=self.headers) as resp:
                if resp.status != 200:
                    raise ValueError(f"Invalid ID {stage_data.id}")
                stage_request = await resp.json()
                stage_request = stage_request[0]
                for match in stage_request.get("matches", []):
                    for side in ["top", "bottom"]:
                        if side in match:
                            if "team" in match[side]:
                                for player in match[side]["team"]["players"]:
                                    if ("user" in player) and ("persistentPlayerID" in player):
                                        if ("accounts" in player["user"]) and ("discord" in player["user"]["accounts"]):
                                            player_entry = tournament_data.get_player_from_persistent_player_id(
                                                player.get("persistentPlayerID", None)
                                            )
                                            if player_entry:
                                                player_entry.discord_id = player["user"]["accounts"]["discord"].get(
                                                    "accountID",
                                                    "")
        return stage_data

    async def __get_stage(self, stage_data: Stage, tournament_data: Tournament) -> Stage:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"https://api.battlefy.com/stages/{stage_data.id}?extend[matches][top.team][players][user]=true&extend[matches][top.team][persistentTeam]=true&extend[matches][bottom.team][players][user]=true&extend[matches][bottom.team][persistentTeam]=true&extend[groups][teams]=true&extend[groups][matches][top.team][players][user]=true&extend[groups][matches][top.team][persistentTeam]=true&extend[groups][matches][bottom.team][players][user]=true&extend[groups][matches][bottom.team][persistentTeam]=true",
                    headers=self.headers) as resp:
                if resp.status != 200:
                    raise ValueError(f"Invalid ID {stage_data.id}")
                stage_request = await resp.json()
                stage_request = stage_request[0]
                stage_data.raw_matches = stage_request.get("matches", [])
                for match in stage_data.raw_matches:
                    top_team_id = match.get("top", {}).get("team", {}).get("persistentTeamID", None)
                    bottom_team_id = match.get("bottom", {}).get("team", {}).get("persistentTeamID", None)
                    if top_team_id and bottom_team_id:
                        top_team = tournament_data.get_team_from_persistent_team_id(top_team_id)
                        bottom_team = tournament_data.get_team_from_persistent_team_id(bottom_team_id)
                        if top_team and bottom_team:
                            stage_data.add_match(Match(match_data=match, top=top_team, bottom=bottom_team))
        await self.__get_standings(stage_data, tournament_data)
        return stage_data

    async def get_tournament(self, tournament_id: str) -> Optional[Tournament]:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"https://api.battlefy.com/tournaments/{tournament_id}?extend%5Bstages%5D%5Bmatches%5D=true&extend%5Bstages.matches.top.team.persistentTeam%5D=1&extend%5Bstages.matches.bottom.team.persistentTeam%5D=1&extend%5Bstages.matches.top.team.players%5D=1&extend%5Bstages.matches.bottom.team.players%5D=1&extend%5Bstages.matches.top.team%5D=1&extend%5Bstages.matches.bottom.team%5D=1",
                    headers=self.headers
            ) as resp:
                if resp.status != 200:
                    raise ValueError("Invalid ID")
                tournament_data = await resp.json()
                tournament = Tournament(data=tournament_data[0])
            async with session.get(f"https://dtmwra1jsgyb0.cloudfront.net/tournaments/{tournament_id}/teams") as resp:
                if resp.status != 200:
                    raise ValueError("Invalid ID")
                team_data = await resp.json()
                tournament.add_teams(team_data)
        async with asyncio.TaskGroup() as g:
            for stage in tournament.stages:
                g.create_task(self.__get_stage(stage, tournament))
        async with asyncio.TaskGroup() as g:
            for stage in tournament.stages:
                g.create_task(self.__get_additional_data(stage, tournament))
        return tournament
