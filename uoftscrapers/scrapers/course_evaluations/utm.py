from ..utils import Scraper
from .course_evaluations_helpers import *
from bs4 import BeautifulSoup
from collections import OrderedDict
import json


class UTMCourseEvaluations:
    """A scraper for UTM's course evaluations."""

    # request parameters for this scraper
    datasource_id, block_id, col_id, str_order = '4520', '750', '1', \
        ['col_1', 'asc']

    @staticmethod
    def scrape(location='.', save=True):
        """Update the local JSON files for this scraper."""

        Scraper.logger.info('UTMCourseEvaluations initialized.')

        docs = OrderedDict()

        courses = get_course_list(payload={
            'datasourceId': UTMCourseEvaluations.datasource_id,
            'intBlocId': UTMCourseEvaluations.block_id,
            'colId': UTMCourseEvaluations.col_id
        })

        for course in courses:
            print('Scraping course:', course)
            evals = get_evaluations(course_code=course, payload={
                'datasourceId': UTMCourseEvaluations.datasource_id,
                'blockId': UTMCourseEvaluations.block_id,
                'subjectColId': UTMCourseEvaluations.col_id,
                'strOrderBy': UTMCourseEvaluations.str_order
            })

            evals.update({
                'faculty': 'UTM'
            })

            docs[evals['course_code']] = evals

        if save:
            for course_id, doc in docs.items():
                Scraper.save_json(doc, location, course_id)

        Scraper.logger.info('UTMCourseEvaluations completed.')

        if not save:
            return docs
