#! /usr/bin/python
"""Module with base class parser and parser for iperf measurement output"""

import re
from collections import OrderedDict


class BaseParser(object):
    """class to find in shell output needed results and combine it in dict"""
    def __init__(self, string):
        self.string = string

    def to_parse(self):
        """method to return the same string"""
        return self.string


class IperfParser(BaseParser):
    """class to find in iperf client output needed
    results and combine it in dict"""
    def __init__(self, string):
        super(IperfParser, self).__init__(string)
        self.string = string
        self.output_dict = OrderedDict()
        self.column_names = ['Interval', 'Transfer', 'Bandwidth']
        self.template = (r'(?P<first>\S+-\s*\S+ \w+)\s*'
                         r'(?P<second>\S+ \w+)\s*'
                         r'(?P<third>\S+ \w+/\w+)')

    def to_parse(self):
        """method to find bandwidth and transfer for each
        interval and add to output dict"""
        data = re.compile(self.template)
        matched_data = re.findall(data, self.string)
        j = 1
        for single_match in matched_data:
            i = 0
            dict_to_insert = dict()
            for name in self.column_names:
                dict_to_insert[name] = single_match[i]
                i += 1
            if j < len(matched_data):
                interval_key = "Time interval {}: {}"\
                    .format(j, single_match[0])
            else:
                interval_key = "Total result:"
            j += 1
            self.output_dict[interval_key] = dict_to_insert
        return self.output_dict
