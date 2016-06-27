from src.base.model.fuzzyset import LingVariable


class Statement:
    def __init__(self, ling_var, term, logical_operator=None, next_st=None):
        assert type(ling_var) is LingVariable, "type of ling_var must be src.base.model.fuzzyset.LingVariable"
        self.ling_var = ling_var
        self.term = term
        if next_st is not None:
            assert type(next_st) is Statement, "type of next_st must be src.base.model.fuzzyset.Statement"
            assert isinstance(logical_operator, (type(LogicalOperator.MAX), type(max))), \
                "logical_operator must be a function from src.base.model.rulebase"
        self.next_st = next_st
        self.logical_operator = logical_operator
        self.cur = None

    def __str__(self):
        if self.next_st is not None:
            return "{0} is {1}".format(self.ling_var, self.term) \
                   + " " + LogicalOperator.operator_str(self.logical_operator) \
                   + " " + str(self.next_st)
        return "{0} is {1}".format(self.ling_var, self.term)

    def __repr__(self):
        return str(self)

    def __next__(self):
        if not self.cur:
            self.cur = self
        elif self.cur.next_st is None:
            self.cur = None
            raise StopIteration
        else:
            self.cur = self.cur.next_st
        return self.cur

    def __iter__(self):
        return self

    def get_single_str(self):
        return "{0} is {1}".format(self.ling_var, self.term)

    def get_full_statement_string(self):
        return str(self)

    def get_variety(self, x):
        return self.term.membership_degree(x)

    def append_statement(self, logical_operator, statement):
        current = self
        while current.next_st is not None:
            current = current.next_st
        current.next_st = statement
        current.logical_operator = logical_operator
        return self


class Rule:
    def __init__(self, if_st, then_st):
        assert type(if_st) is Statement
        assert type(then_st) is Statement
        self.if_st = if_st
        self.then_st = then_st

    def __str__(self):
        return "IF {0} THEN {1}".format(self.if_st.get_full_statement_string(),
                                        self.then_st.get_full_statement_string())


class RuleBase:
    def __init__(self):
        self.rules = []

    def add(self, rule):
        self.rules.append(rule)

    def remove(self, rule):
        self.rules.remove(rule)

    def __len__(self):
        return len(self.rules)

    def __iter__(self):
        return iter(self.rules)

    def __getitem__(self, item):
        return self.rules[item]

    def __str__(self):
        result = ""
        for rule in self.rules:
            result += str(rule) + "\n"
        return result

    def __repr__(self):
        return str(self)


class LogicalOperator:
    @staticmethod
    def MIN(a, b):
        return min(a, b)

    @staticmethod
    def MAX(a, b):
        return max(a, b)

    @staticmethod
    def NOT(x):
        return 1 - x

    @staticmethod
    def operator_str(op):
        and_names = LogicalOperator.get_and_operators_names()
        or_names = LogicalOperator.get_or_operators_names()

        if op.__name__ in and_names:
            return "AND"
        elif op.__name__ in or_names:
            return "OR"
        return ""

    @staticmethod
    def get_and_operators_names():
        names = [LogicalOperator.MIN.__name__]
        return names

    @staticmethod
    def get_or_operators_names():
        names = [LogicalOperator.MAX.__name__]
        return names

    and_operators = {MIN}
    or_operators = {MAX}
    not_operators = {NOT}
