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

import sys
import pyexpat
from subprocess import Popen, PIPE


show = sys.argv[1]
dateonly = (len(sys.argv) > 2) and (sys.argv[2] == 'date-only')
episode, part = None, None
lines_added = 0
lines = None


class WikiParse:
    '''
    Parser for most shows
    '''
    in_body = False
    in_quote_area = False
    in_bad_area = False
    wiki = None
    AmericanDadSeasons = 11
    SupernaturalSeasons = 10
    Tags = ['h3', 'h4', 'dd', 'dl', 'hr']
    text = ''
    def CommandLineArg(self, CMLargs):
        show_ = CMLargs.replace(' ','_')
        command = ['wget', 'http://en.wikiquote.org/wiki/%s' % show_, '-O', '-']
        
        proc = Popen(command, stdout = PIPE, stderr = sys.stderr)
        self.wiki = proc.communicate()[0]
        # print(wiki)
        if proc.poll() is None:
            proc.wait()
        if not proc.returncode == 0:
            sys.exit(1)
        
        def start_element(self, name, attrs):
            if name == 'body':
                self.in_body = True
            elif self.in_body and (name in self.Tags):
                if (name not in self.Tags[:2] or (len(attrs) == 0)):
                    if name == 'h3':
                        self.text += '\t'
                    if name == 'h4':
                        self.text += '\t\t'
                    self.in_quote_area = True
                #elif (sname not in self.Tags or (len(attrs) == 0)):
                #    if name == 'h3':
                #        self.text += '\t'
                #    if name == 'h4':
                #        self.text += '\t\t'
                #    if name == 'li':
                #        self.text += '\t\t\n'
                #    self.in_quote_area = True
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
        
        def char_data(self, data):
            if self.in_quote_area and not self.in_bad_area:
                data = data.strip('\t\n').replace(' ', ' ') # the first space is a nbsp
                while '  ' in data:
                    data = data.replace('  ', ' ')
                if not data == '':
                    self.text += data
        
        def WikiScraper(self, wiki1):
            parser = pyexpat.ParserCreate()
            parser.StartElementHandler = self.start_element
            parser.EndElementHandler = self.end_element
            parser.CharacterDataHandler = self.char_data
            parser.Parse(wiki1, 1)
        
        def WikiFormater(self, text1):
            global show, episode, part, lines_added, lines
            self.text = text1.replace('[edit]', '')
            self.text = self.text.rstrip(' \n\t')
            lines = self.text.split('\n')
            self.text = ''
            
            for line in lines:
                if line.startswith('\t\t'):
                    part = line[2:]
                elif line.startswith('\t'):
                    if lines_added > 0:
                        lines_added = 0
                        episode_ = episode if part is None else ('%s - %s' % (episode, part))
                        self.text += '\n\t-- %s - %s\n%%\n' % (show, episode_)
                    if not line == '\t-----':
                        episode, part = line[1:], None
                else:
                    lines_added += 1
                    self.text += line + '\n'
                
                if lines_added > 0:
                    episode_ = episode if part is None else ('%s - %s' % (episode, part))
                    self.text += '\n\t-- %s - %s\n%%\n' % (show, episode_)

class Versioner(object):
    '''
    Class to handle history and versioning
    
    Currently not working
    '''
    history_url = None
    on_mw_changeslist_date = False
    last_modified = None
    def start_element(self, name, attrs):
        if name == 'a':
            if 'href' in attrs:
                val = attrs['href']
                val_ = val.replace('?', '&') + '&'
                if 'action=history' in val_.split('&'):
                    if not val.startswith('/'):
                        sys.exit(1)
                    self.history_url = 'http:' if val.startswith('//') else 'http://en.wikiquote.org'
                    self.history_url += val
    
    def historyCheck(self, wikiData):
        parser = pyexpat.ParserCreate()
        parser.StartElementHandler = self.start_element
        
        parser.Parse(wikiData, 1)
        
        if self.history_url is None:
            sys.exit(1)
        
        command = ['wget', history_url, '-O', '-']
        proc = Popen(command, stdout = PIPE, stderr = sys.stderr)
        self.history = proc.communicate()[0]
        if proc.poll() is None:
            proc.wait()
        if not proc.returncode == 0:
            sys.exit(1)
    
    def start_element(self,name, attrs):
        self.on_mw_changeslist_date = False
        if name == 'a':
            if ('class' in attrs) and (attrs['class'] == 'mw-changeslist-date'):
                self.on_mw_changeslist_date = True
    
    def end_element(name):
        self.on_mw_changeslist_date = False
    
    def char_data(data):
        if self.on_mw_changeslist_date and (self.last_modified is None):
            self.last_modified = data
    
    def historyParser(self):
        parser = pyexpat.ParserCreate()
        parser.StartElementHandler = self.start_element
        parser.EndElementHandler = self.end_element
        parser.CharacterDataHandler = self.char_data
        parser.Parse(self.history, 1)

