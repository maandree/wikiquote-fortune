from OPWikiParser import *

class SuperParse(WikiParse):
    """Supernatural parser"""
    Tags = ['h3', 'h4','dd', 'dl', 'hr'] # Adding the li tag gets the data on first page but messes up
                                         #the parsing of the rest of the pages

    def start_element(self,name, attrs):
        
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
        elif name in ('label',):
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
        elif name in ('label',):
            self.in_bad_area = False
