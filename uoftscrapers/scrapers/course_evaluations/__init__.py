from ..utils import Scraper
from .utsg import UTSGCourseEvaluations
from .utm import UTMCourseEvaluations
from .utsc import UTSCCourseEvaluations

from collections import OrderedDict


class CourseEvaluations:
    """A scraper for course evaluations across various faculties."""

    @staticmethod
    def scrape(location='.'):
        """Update the local JSON files for this scraper."""
        Scraper.logger.info('CourseEvaluations initialized.')

        docs = OrderedDict()

        for campus in UTSGCourseEvaluations, UTMCourseEvaluations, UTSCCourseEvaluations:
            evals = campus.scrape(location, save=False)

            if not evals:
                continue

            for course, data in evals.items():
                if course not in docs:
                    docs[course] = OrderedDict([
                        ('course', course),
                        ('entries', [])
                    ])
                docs[course]['entries'].extend(data['entries'])

        for course, doc in docs.items():
            Scraper.save_json(doc, location, course)

        Scraper.logger.info('CourseEvaluations completed.')
