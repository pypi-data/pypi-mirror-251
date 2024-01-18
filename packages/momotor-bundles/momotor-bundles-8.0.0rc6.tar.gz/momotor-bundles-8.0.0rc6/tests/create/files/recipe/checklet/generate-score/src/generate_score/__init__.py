import json
from collections import defaultdict
from textwrap import dedent

from mtrchk.org.momotor.base.checklet import Checklet
from mtrchk.org.momotor.base.checklet.meta import OptionDefinition
from mtrchk.org.momotor.base.checklet.result import CheckletResult, Outcome

STAT_SECTIONS = ('code_execution', 'code_outputs', 'sources')

STATS_FILE_CLASS_OPTION = 'stats-file-class'
FAIL_SCORE_OPTION = 'fail-score'
PASS_SCORE_OPTION = 'pass-score'


class GenerateScore(Checklet):
    class Meta:
        options = (
            OptionDefinition(
                STATS_FILE_CLASS_OPTION,
                doc=dedent("""\n
                    The file containing the statistics: <resultid>:(<class>)(#name) 
                        
                        <resultid> is the id of the step producing the statistics file
                        <class> can be empty indicating all files, regardless of class
                        <name> can be empty, indicating all files
                        
                    If multiple files match, their statistics are combined
                """),
            ),
            OptionDefinition(
                FAIL_SCORE_OPTION,
                doc="Fail score",
                type='int',
                default=0,
            ),
            OptionDefinition(
                PASS_SCORE_OPTION,
                doc="Pass score",
                type='int',
                default=1,
            ),
        )

    def run(self) -> CheckletResult:
        stats_file_class = self.resolve_option(STATS_FILE_CLASS_OPTION)
        stats_files = self.find_files(stats_file_class)

        file_count = 0
        stats = {
            section: defaultdict(int) for section in STAT_SECTIONS
        }

        for sf in stats_files:
            file_count += 1
            file_stats = json.loads(sf.read())

            for section in STAT_SECTIONS:
                section_stats = file_stats[1].get(section, {})
                for key, value in section_stats.items():
                    stats[section][key] += value

        passed = False
        report = []
        if file_count == 0:
            report.append('No files')

        else:
            not_executed_in_linear_order = stats['code_execution']['not executed in linear order']
            if not_executed_in_linear_order > 0:
                report.append('Warning: {} cell(s) not executed in linear order'.format(not_executed_in_linear_order))

            not_executed = stats['code_execution']['not executed'] - stats['sources']['Empty sources']
            error = stats['code_outputs']['error']
            if not_executed > 0 or error > 0:
                if not_executed > 0:
                    report.append('Rejected: {} cell(s) in submitted notebook not executed'.format(not_executed))

                if error > 0:
                    report.append('Rejected: {} cell(s) in submitted notebook contain errors'.format(error))

            else:
                passed = True
                report.append('Accepted: All cells in submitted notebook executed without errors')

        properties = {
            'report': '\n'.join(report),
        }

        score = self.resolve_option(PASS_SCORE_OPTION if passed else FAIL_SCORE_OPTION)
        if score > 0:
            properties['score'] = score
        else:
            properties['reason'] = 'Rejected'

        return CheckletResult(
            outcome=Outcome.condition(score > 0),
            properties=properties
        )
