import logging

from md_utils import html
from st_types.st_basic import Step, StepType

logger = logging.getLogger('deploy_scripts')


class StepSkip(Step):
    """ Этот степ не нужно апдетить, его руками делают на степике!
    """
    def __init__(self):
        super().__init__()
        self.step_type = StepType.SKIP
        self.name = 'skip it'

    @staticmethod
    def str_from_md(md_lines):
        st = StepSkip()
        return st