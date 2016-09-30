from ..utils import Scraper
from .course_evaluations_helpers import *
from bs4 import BeautifulSoup
from collections import OrderedDict
import json


class UTSGCourseEvaluations:
    """A scraper for UTSG's course evaluations."""

    @staticmethod
    def scrape(location='.', save=True):
        """Update the local JSON files for this scraper."""

        Scraper.logger.info('UTSGCourseEvaluations initialized.')

        docs = OrderedDict()

        for faculty in ArtSciCourseEvaluations, EngCourseEvaluations:
            evals = faculty.scrape(location=location, save=False)

            if evals is None:
                continue

            for course, data in evals.items():
                if course not in docs:
                    docs[course] = OrderedDict([
                        ('course', course),
                        ('entries', [])
                    ])
                docs[course]['entries'].extend(data['entries'])

        if save:
            for id_, doc in evals.items():
                Scraper.save_json(doc, location, id_)

        Scraper.logger.info('UTSGCourseEvaluations completed.')

        if not save:
            return docs


class ArtSciCourseEvaluations:
    """A scraper for UofT's Arts & Science course evaluations."""

    # request parameters for this scraper
    datasource_id, block_id, col_id, str_order = '4850', '900', '9', \
        ['col_9', 'asc']

    @staticmethod
    def scrape(location='.', save=True):
        """Update the local JSON files for this scraper."""

        Scraper.logger.info('ArtSciCourseEvaluations initialized.')

        docs = OrderedDict()

        courses = get_course_list(payload={
            'datasourceId': ArtSciCourseEvaluations.datasource_id,
            'intBlocId': ArtSciCourseEvaluations.block_id,
            'colId': ArtSciCourseEvaluations.col_id
        })

        for course in courses:
            print('Scraping course:', course)
            evals = get_evaluations(course_code=course, payload={
                'datasourceId': ArtSciCourseEvaluations.datasource_id,
                'blockId': ArtSciCourseEvaluations.block_id,
                'subjectColId': ArtSciCourseEvaluations.col_id,
                'strOrderBy': ArtSciCourseEvaluations.str_order
            })

            evals.update({
                'faculty': 'Arts & Science'
            })

            docs[evals['course_code']] = evals

        if save:
            for course_id, doc in docs.items():
                Scraper.save_json(doc, location, course_id)

        Scraper.logger.info('ArtSciCourseEvaluations completed.')

        if not save:
            return docs


class EngCourseEvaluations:
    """A scraper for UofT's Applied Science & Engineering
    course evaluations."""

    # request parameters for this scraper
    datasource_id, block_id, col_id, str_order = '3860', '720', '33', \
        ['col_33', 'asc']

    @staticmethod
    def scrape(location='.', save=True):
        """Update the local JSON files for this scraper."""

        Scraper.logger.info('EngCourseEvaluations initialized.')

        docs = OrderedDict()

        courses = get_course_list(payload={
            'datasourceId': EngCourseEvaluations.datasource_id,
            'intBlocId': EngCourseEvaluations.block_id,
            'colId': EngCourseEvaluations.col_id
        })

        for course in courses:
            print('Scraping course:', course)
            evals = get_evaluations(course_code=course, payload={
                'datasourceId': EngCourseEvaluations.datasource_id,
                'blockId': EngCourseEvaluations.block_id,
                'subjectColId': EngCourseEvaluations.col_id,
                'strOrderBy': EngCourseEvaluations.str_order
            })

            evals.update({
                'faculty': 'Applied Science & Engineering'
            })

            docs[evals['course_code']] = evals

        if save:
            for course_id, doc in docs.items():
                Scraper.save_json(doc, location, course_id)

        Scraper.logger.info('EngCourseEvaluations completed.')

        if not save:
            return docs
