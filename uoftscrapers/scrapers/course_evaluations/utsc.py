from ..utils import Scraper
from .course_evaluations_helpers import *
from bs4 import BeautifulSoup
from collections import OrderedDict
import json


class UTSCCourseEvaluations:
    """A scraper for UTSC's course evaluations."""

    # request parameters for this scraper
    datasource_id, block_id, col_id, str_order = '5070', '1140', '4', \
        ['col_4', 'asc']

    @staticmethod
    def scrape(location='.', save=True):
        """Update the local JSON files for this scraper."""

        Scraper.logger.info('UTSCCourseEvaluations initialized.')

        docs = OrderedDict()

        courses = get_course_list(payload={
            'datasourceId': UTSCCourseEvaluations.datasource_id,
            'intBlocId': UTSCCourseEvaluations.block_id,
            'colId': UTSCCourseEvaluations.col_id
        })

        for course in courses:
            print('Scraping course:', course)
            evals = get_evaluations(course_code=course, payload={
                'datasourceId': UTSCCourseEvaluations.datasource_id,
                'blockId': UTSCCourseEvaluations.block_id,
                'subjectColId': UTSCCourseEvaluations.col_id,
                'strOrderBy': UTSCCourseEvaluations.str_order
            })

            evals.update({
                'faculty': 'UTSC'
            })

            docs[evals['course_code']] = evals

        if save:
            for course_id, doc in docs.items():
                Scraper.save_json(doc, location, course_id)

        Scraper.logger.info('UTSCCourseEvaluations completed.')

        if not save:
            return docs
