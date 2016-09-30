from bs4 import BeautifulSoup
from collections import OrderedDict
import json
import requests


HOST = 'https://course-evals.utoronto.ca/BPI/fbview-WebService.asmx'


def post(url, **kwargs):
    payload = {}

    if 'payload' in kwargs:
        payload.update(kwargs['payload'])

    headers = {
        'Connection': 'keep-alive',
        'Content-Type': 'application/json; charset=utf-8',
        'Host': 'course-evals.utoronto.ca',
        'Origin': 'https://course-evals.utoronto.ca',
        'Referer': 'https://course-evals.utoronto.ca/BPI/fbview.aspx',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
    }

    if 'headers' in kwargs:
        headers.update(kwargs['headers'])

    return requests.post(url, data=json.dumps(payload), headers=headers)


def get_course_list(url=HOST, endpoint='getSubjectsValues', **kwargs):
    """Fetch and parse the list of course codes."""

    payload = {
        'strUiCulture': 'en-US',
        'datasourceId': '',
        'colId': '',
        'ddlId': 'ddlFbvSubjectsValues',
        'maxItemsParPage': '20000',
        'pageCourante': 1,
        'strFiltre': '',
        'boolPleaseSelect': 'true',
        'boolAll': 'true',
        'intBlocId': '',
        'clearHTML': 'false',
        'userid': ''
    }

    payload.update(kwargs['payload'])

    res = post('%s/%s' % (url, endpoint), payload=payload)

    return [v['value']
            for v in json.loads((res.json()['d']))['valuesList'][2:]]


def get_evaluations(course_code, url=HOST, endpoint='getFbvGrid', **kwargs):
    """Fetch and parse the evaluations for course with code course_code."""

    payload = {
        'strUiCultureIn': 'en-US',
        'datasourceId': '',
        'blockId': '',
        'subjectColId': '',
        'subjectValue': course_code,
        'detailValue': '____[-1]____',
        'gridId': 'fbvGrid',
        'pageActuelle': 1,
        'strOrderBy': [],
        'strFilter': ['', '', 'ddlFbvColumnSelectorLvl1', ''],
        'sortCallbackFunc': '__getFbvGrid',
        'userid': '',
        'pageSize': '100'
    }

    payload.update(kwargs['payload'])

    res = post('%s/%s' % (url, endpoint), payload=payload)

    grid = res.json()['d'][0]
    soup = BeautifulSoup(grid, 'html.parser')

    table = soup.find('table', id='fbvGrid')

    doc = OrderedDict([
        ('course_code', course_code),
        ('entries', [])
    ])

    table_headers = []

    for th in table.find('tr', class_='gHeader').find_all('th'):
        if not th.find('div', class_='tooltip'):
            table_headers.append(th.text)
            continue

        table_headers.append(
            th.find('div', class_='tooltip').text.split('.', 1)[1].strip())

    evaluation_questions = table_headers[6:-2]

    for tr in table.find_all('tr', class_='gData'):
        tds = [td.text.strip() for td in tr.find_all('td')]

        dept = tds[0]
        course_name = tds[1]
        professor = ' '.join(tds[2:4][::-1])
        course_season = ' '.join(tds[4:6])

        evaluations = OrderedDict([
            ('questions', [])
        ])

        evaluation_question_responses = tds[6:-2]

        for i in range(len(evaluation_question_responses)):
            question = evaluation_questions[i]

            try:
                response = float(evaluation_question_responses[i])
            except Exception as e:
                response = None

            evaluations['questions'].append(OrderedDict([
                ('question', question),
                ('response', response)
            ]))

        stats_keys = ['number_invited', 'response_count']
        stats = OrderedDict()

        for i, td in enumerate(tds[-2:]):
            k = stats_keys[i]

            try:
                v = int(tds[-2+i])
            except Exception as e:
                v = None

            stats[k] = v

        doc['entries'].append(OrderedDict([
            ('course_name', course_name),
            ('season', course_season),
            ('professor', professor),
            ('department', dept),
            ('evaluations', evaluations),
            ('statistics', stats)
        ]))

    return doc
