from random import randint
from random import random


class Grammar:

    # init
    #
    # Initializes a grammar. If specified, 'start' is used as 
    # the start string for a derivation performed by the
    # 'generate' method below.
    #
    # This is called when the instructor is invoked, for example
    # in the code
    #
    #   Gr = Grammar('<sentence>')
    #
    def __init__(self, start_string=None):
        # attributes
        self.start = start_string
        # begin with self.rules as an empty dictionary
        self.rules = {}

    # read
    #
    # Reads a grammar from a file with the given name.
    #
    def read(self, filename):
        # Reads each line and sets self.rules[lhs] to rhs
        file = open(filename,'r')
        line = file.readline()[:-1]
        while line != '':
            # make a list out of the string by splitting at every space
            syms = line.split(' ')
            # call the key lhs
            lhs = syms[0]
            # call everything else rhs, and make it into a string again
            rhs = ' '.join(syms[2:])
            # 'setitem' lhs as rhs
            self[lhs] = rhs
            line = file.readline()[:-1]

    # setitem
    #
    # Adds a production to the grammar, one of the form:
    #
    #    var ::= rhs
    #
    # var should be a variable string
    # rhs should be a string of variables and terminals
    #
    # This method is invoked when a 'component assignment'
    # is used in code, for example
    #
    #   Gr['<sentence>'] = '<noun_phrase> <verb_phrase>'
    #
    def __setitem__(self,var,rhs):
        # if var is already a key within our grammar
        if var in self.rules:
            # attach rhs as another possibility for what var can derive to
            self.rules[var].append(rhs)
        # otherwise, create a new key
        else:
            # and make rhs its list of possible derivations
            self.rules[var] = [rhs]

    # getitem
    #
    # Returns the right-hand side of a production for the variable.
    # If there are several productions whose LHS is var, then one
    # is chosen at random.
    #
    # var should be a variable string
    #
    # This method is invoked when a 'component access' is expressed
    # in code, for example
    #
    #   Gr['<sentence>']
    #
    # might return the string '<noun_phrase> <verb_phrase>'
    #
    def __getitem__(self,var):
        # if var is a key within our grammar (i.e., a nonterminal)
        if var in self.rules:
            # access the list of stuff var can be
            rsides = self.rules[var]
            # find out how many possibilities there are
            rlen = len(rsides)
            # get a random integer that is between 0 and the length-1
            r = int(random() * rlen)
            # and grab a random index of rsides
            return rsides[r]
        else:
            # if this isn't a key, just return the same string
            # because it's a terminal (already derived as much as it can be)
            return var
    # generate
    #
    # (a Grammar method)
    #
    # Derives a string from the grammar's derivation start string.
    #
    def generate(self):
        # to check whether a string is further derivable or not...
        def isExpandable(deriv=None):
            # make a list from a given string, splitting at every space
            makelist = deriv.split(' ')
            length = len(makelist)
            # check every one of those items
            for i in range(length):
                # if any one of them is a key...
                if makelist[i] in self.rules:
                    # this will return true
                    return True
            # only if NO item has returned true, will this return false
            return False
        # start with your grammar's start string (e.g., <sentence>)
        derivstring = self.start
        # as long as the string is derivable, keep deriving
        while isExpandable(derivstring) == True:
            # at every step, change the derivstring so that it equals
            # the derived (one step further) version of that string
            derivstring = self.applyTo(derivstring)
        # return this string only when derivstring can be derived no further
        return derivstring

    # applyTo
    #
    # Give back a string that results from applying some grammar
    # production to each of the variables that occur in the 
    # string.
    #
    def applyTo(self,deriv=None):
        # create a list of elements by splitting deriv at every space
        segments = deriv.split(' ')
        # find the length of that list
        seglength = len(segments)
        # For every element in the list...
        for i in range(seglength):
            # replace that element with a randomly generated rhs with which
                # this key is associated, if it is a key
                    # ("get item" is written in such a way that it will just
                    # give back the same string, if it's not a key)
            segments[i] = self[segments[i]]
        # once this has been performed for every element, put
        # the list back together to form a single string
        exstring = ' '.join(segments)
        # ...and give back the (now expanded) string
        return exstring
