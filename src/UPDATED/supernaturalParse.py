# -*- python -*-

# wikiquote-fortune – Generate fortune cookies from Wikiquote
# Copyright © 2014, 2016  Mattias Andrée (maandree@member.fsf.org)
# Copyright © 2016        Chuk Ume (chubiyke@gmail.com)
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
# 
# Note that output from this script is derivative work of Wikiquote
# and is therefore under the license used at Wikiquote.

from OPWikiParser import *


class SuperParse(WikiParse):
    '''
    Supernatural parser
    '''
    Tags = ['h3', 'h4','dd', 'dl', 'hr'] # Adding the li tag gets the data on first page but messes up
                                         #the parsing of the rest of the pages
    
    def start_element(self, name, attrs):
        if name == 'body':
            self.in_body = True
        elif self.in_body and (name in self.Tags):
            if (name not in (self.Tags[:2])) or (len(attrs) == 0):
                if name == 'h3':
                    self.text += '\t'
                if name == 'h4':
                    self.text += '\t\t';
                # if name == 'li':
                #     self.text += '\t\t\n'
                self.in_quote_area = True
        elif name == 'label':
            self.in_bad_area = True
        if self.in_quote_area and not self.in_bad_area:
            if (name == 'hr') and (len(self.text) > 0):
                if not self.text.endswith('\n'):
                    self.text += '\n'
                self.text += '\t-----\n'
    
    def end_element(self, name):
        if name == 'body':
            self.in_body = False
        elif self.in_body and name in self.Tags:
            self.in_quote_area = False
            if name in self.Tags[:3]:
                self.text += '\n'
        elif name == 'label':
            self.in_bad_area = False

