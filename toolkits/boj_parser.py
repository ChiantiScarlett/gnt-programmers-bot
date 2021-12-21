from bs4 import BeautifulSoup as Soup
import requests
from time import sleep
from dotenv import load_dotenv
import os


class BOJParser():
    """
    BOJ Parser.
    """

    def __init__(self):
        load_dotenv()

    def parse_workbook(self, workbook_id: str) -> list:
        """
        [Parameters]
            workbook_id: [str] Workbook ID. If it belongs to a group,
                               use slash('/') e.g. "11916/39858"      

        [Description]
            Get list of problem IDs from workbook ID.

        [Return]
            List of problem IDs
        """
        id_list = []

        # 1. if workbook_id contains '/', use different URL prefix.
        if '/' in str(workbook_id):
            url = f'https://www.acmicpc.net/group/workbook/view/{workbook_id}'
        else:
            url = f'https://www.acmicpc.net/workbook/view/{workbook_id}'

        # 2. fetch data.
        response = self._make_request_with_headers(url=url)
        html = response.text
        html = Soup(html, 'html.parser')

        try:
            trs = html.find('div', {'class': 'table-responsive'}
                            ).find('tbody').find_all('tr')
        except AttributeError:
            return self._print_attribute_error()

        if len(trs):
            for tr in trs:
                td_list = tr.find_all('td')
                problem_id = td_list[0].text.strip()
                id_list.append(problem_id)

        return id_list

    def parse_tiers(self, page_from: int = 1, page_to: int = 240,
                    delay_per_fetch: float = 1.8) -> list:
        """
        [Parameters]
            page_from: [int] c.f. footer of acmicpc.net/problemset
            page_to:   [int] c.f. footer of acmicpc.net/problemset
            delay_per_fetch: [float] Add delays per fetch. Make sure to give
                                     sufficient delays in order to prevent 
                                     from heavy server traffic.

        [Description]
            Fetch all problem data, including titles, tiers(provided by
            solved.ac), and problem ID.

        [Return]
            List of dictionaries. e.g. [{'id':..., 'tier':..., 'title:'...}]
        """

        tier_map = ['?', 'B5', 'B4', 'B3', 'B2', 'B1', 'S5', 'S4', 'S3', 'S2',
                    'S1', 'G5', 'G4', 'G3', 'G2', 'G1', 'P5', 'P4', 'P3',
                    'P2', 'P1', 'D5', 'D4', 'D3', 'D2', 'D1', 'R5', 'R4',
                    'R3', 'R2', 'R1', 'M']

        problem_list = []
        for page in range(page_from, page_to+1):
            response = self._make_request_with_headers(
                url=f"https://www.acmicpc.net/problemset/{page}")
            html = response.text
            html = Soup(html, 'html.parser')

            try:
                trs = html.find('table', {'id': 'problemset'}
                                ).find('tbody').find_all('tr')
            except AttributeError:
                return self._print_attribute_error()

            if not len(trs):
                break

            for tr in trs:
                td_list = tr.find_all('td')
                problem_id = td_list[0].text
                tier = tier_map[int(td_list[1].find(
                    'img')['src'].split('/')[-1][:-4])]
                title = td_list[1].text

                problem_list.append({"id": problem_id.strip(),
                                     'tier': tier,
                                     'title': title.strip()})
            sleep(delay_per_fetch)

        return problem_list

    def _make_request_with_headers(self, url: str) -> requests.Response:
        """
        [Parameters]
            url:  [str] URL to fetch.

        [Description]
            Make request with headers, since some of the BOJ data requires
            user authentication. This method relies on the environment variable
            `HEADERS_COOKIE`. Make sure to set appropriate value in .env file.

        [Return]
            requests.Response
        """
        headers = {}
        headers["cookie"] = os.getenv('HEADERS__COOKIE')

        return requests.get(url, headers=headers)

    def _print_attribute_error(self):
        print('[*] Failed to parse data. Check your parameters and .env data.')


if __name__ == "__main__":

    """
    :: Test Code Example ::
    """

    parser = BOJParser()
    print(parser.parse_workbook('11916/39850'))
