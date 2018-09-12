import logging
import configparser
import os

from bool_query import bool_query

class BreakRule(object):
    def __init__(self):
        self.settings = configparser.ConfigParser()
        self.settings.read("{}/tms/settings.ini".format(os.getcwd()))

        self.breakrules = configparser.ConfigParser()
        self.breakrules.read("{}/tms/breakrules.ini".format(os.getcwd()))

        self.rules = []
        for rule_section in self.breakrules.sections():
            self.rules.append(Rule(rule_section, self.breakrules))

    def get_break_rules(self):
        logging.info("Break Rules: ")
        for rule in self.rules:
            logging.info('  [{}] {}'.format(rule.rule_id, rule.description))

    def get_break_rule(self, desired_rule_id=None):
        if not desired_rule_id: desired_rule_id = self.settings.get("Settings", "BreakRule")
        for rule in self.rules:
            if rule.rule_id == desired_rule_id:
                logging.info('  [{}] {}'.format(rule.rule_id, rule.description))
            else:
                logging.info("Rule doesn't exist")

    def update_break_rule(self):
        self.get_break_rules()

        selection_query = None
        while selection_query is None:
            logging.info('Please enter the ID of the rule to be used...')
            selection = input()
            try:
                selection_query = bool_query('Select Rule "{}" for use?'.format(self.rules[int(selection) - 1].rule_id), default="y")
            except IndexError:
                logging.warning('WARNING: Select rule ID has no rule associated with it. Select again.')
            except ValueError:
                logging.warning('WARNING: Please enter a numeric value corresponding to a rule ID.')

        self.settings.set("Settings", "BreakRule", selection)
        logging.info("Break rule changed to rule {}".format(self.settings.get("Settings", "BreakRule")))


class Rule(object):
    def __init__(self, rule_section, breakrules):
        self.rule_section = rule_section
        self.rule_id = breakrules.get(rule_section, "RuleID")
        self.description = breakrules.get(rule_section, "Description")
