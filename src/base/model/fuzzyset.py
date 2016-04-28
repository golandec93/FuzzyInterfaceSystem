class Term:
    def __init__(self, name, membership_function, *function_parameters):
        self.name = name
        self.membership_function = membership_function
        self.function_parameters = function_parameters

    def membership_degree(self, x):
        return self.membership_function(x, *self.function_parameters)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class LingVariable:
    def __init__(self, name, universum, *terms):
        for term in terms:
            assert type(term) is Term, "type of each term in terms must be src.base.model.fuzzyset.Term"
        self.name = name
        self.terms = list(terms)
        self.universum = universum

    def set_terms(self, *terms):
        self.terms = list(terms)

    def append_terms(self, *terms):
        self.terms.extend(list(terms))

    def term_by_name(self, name):
        for term in self.terms:
            if term.name == name:
                return term
        return None

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


class MembershipFunctions:
    @staticmethod
    def triangle(*parameters):
        """

        :param parameters: tuple with 4 elements: [x, a, b ,c], a <= b <= c
        x - signal
        a - abscissa of left bottom vertex
        b - abscissa of upper vertex
        c - abscissa of right bottom vertex
        :return:
        """
        return MembershipFunctions.trapeze(parameters[0], parameters[1], parameters[2], parameters[2], parameters[3])

    @staticmethod
    def trapeze(*parameters):
        """

        :param parameters:  tuple with 5 elements: [x, a, b ,c, d], a <= b <= c <= d
        x - signal
        a - abscissa of left bottom vertex
        b - abscissa of left upper vertex
        c - abscissa of right upper vertex
        d - abscissa of right bottom vertex
        :return:
        """
        if parameters[0] <= parameters[1] or parameters[0] >= parameters[4]:
            return 0
        elif parameters[2] <= parameters[0] <= parameters[3]:
            return 1
        elif parameters[0] <= parameters[2]:
            return (parameters[0] - parameters[1]) / (parameters[2] - parameters[1])
        return (parameters[0] - parameters[4]) / (parameters[3] - parameters[4])
