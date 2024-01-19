import asyncio
import aiohttp
from typing import Optional, List
from .models import Organization, organization_from_dict, SearchTournament, tournaments_from_org_search


class OrganizationClient:
    def __init__(self, headers: dict = None):
        self.headers = headers or {}

    async def get_org(self, org_slug: str) -> Optional[Organization]:
        """
        Get data on a Battlefy Org
        :param org_slug:
        :return: Organisation
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f'https://dtmwra1jsgyb0.cloudfront.net/organizations?slug={org_slug}&extend%5Badmins%5D=true&extend%5Bmoderators%5D=true&extend%5Bowner%5D=true&extend%5Brunners%5D=true',
                    headers=self.headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    orgs = organization_from_dict(data)
                    if len(orgs) > 0:
                        return orgs[0]
                else:
                    return None

    async def __get_page_data(self, org_id: str, page_no: int, tour_list: list):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"https://search.battlefy.com/tournament/organization/{org_id}/past?page={page_no}&size=10",
                    headers=self.headers) as resp:
                if resp.status == 200:
                    page_data = await resp.json()
                    if "tournaments" in page_data:
                        tour_list += tournaments_from_org_search(page_data["tournaments"])
        return tour_list

    async def search_orgs(self, org_id: str) -> List[SearchTournament]:
        tournaments = []
        pages = 0
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://search.battlefy.com/tournament/organization/{org_id}/past?page=1&size=10"
                    ,headers=self.headers) as resp:
                if resp.status == 200:
                    page_one_data = await resp.json()
                    if "total" in page_one_data:
                        pages = int(page_one_data["total"] / 10)
                        if pages > 0:
                            pages = pages + 1
                        if (page_one_data["total"] % 10) != 0:
                            pages = pages + 1
                    if "tournaments" in page_one_data:
                        tournaments += tournaments_from_org_search(page_one_data["tournaments"])
                else:
                    return []
        async with asyncio.TaskGroup() as g:
            for x in range(2, pages):
                g.create_task(self.__get_page_data(org_id, x, tournaments))
        return tournaments
