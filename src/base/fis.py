from src.base.model.rulebase import RuleBase
import sys


class FuzzyInterfaceSystem:
    def __init__(self, rule_base, and_operator, or_operator, activator, accumulator, defuzzificator, accuracy):
        sys.setrecursionlimit(2000)
        assert isinstance(rule_base, RuleBase)
        self.rule_base = rule_base
        self.AND = and_operator
        self.OR = or_operator
        self.accuracy = accuracy
        self.accumulator = accumulator
        self.activator = activator
        self.defuzzificator = defuzzificator
        self.ling_vars = []
        self.output_ling_vars = []
        for rule in rule_base:
            for statement in rule.then_st:
                if statement.ling_var not in self.output_ling_vars:
                    self.output_ling_vars.append(statement.ling_var)
            for if_statement in rule.if_st:
                if if_statement.ling_var not in self.ling_vars:
                    self.ling_vars.append(if_statement.ling_var)

    def process(self, signals):
        fuzzed = self.fuzzificate(signals)
        aggred = self.aggregate(fuzzed)
        activated = self.activate(aggred)
        accumulated = self.accumulate(activated)
        defuzzificated = self.defuzzificate(accumulated)
        return defuzzificated

    def fuzzificate(self, signals):
        result = {}
        for rule in self.rule_base:
            rule_result = {}
            for statement in rule.if_st:
                signal = signals[statement.ling_var]
                rule_result[statement] = statement.get_variety(signal)
            result[rule] = rule_result
        return result

    def aggregate(self, fuzzed):
        result = {}
        for rule in fuzzed.keys():
            varieties = Utils.get_varieties(rule.if_st, fuzzed[rule])
            sts = Utils.get_if_statements(rule)
            assert len(varieties) == len(sts), "number of varieties and number of statements does not match"
            cur = sts[0]
            while len(varieties) != 1:
                if cur.logical_operator is self.AND and cur.logical_operator is not None \
                        or cur.logical_operator is self.OR and not Utils.is_have_operator(sts, self.AND):
                    varieties[sts.index(cur) + 1] = cur.logical_operator(varieties[sts.index(cur)],
                                                                         varieties[sts.index(cur) + 1])
                    new_cur = sts[sts.index(cur) + 1]
                    varieties.pop(sts.index(cur))
                    sts.remove(cur)
                    cur = new_cur
                elif cur.logical_operator is None:
                    cur = sts[0]
            result[rule] = varieties[0]
        return result

    def activate(self, aggregated):
        result = {}
        for rule in aggregated.keys():
            st_result = {}
            for statement in rule.then_st:
                st_result[statement] = lambda x: self.activator(aggregated[rule], statement.get_variety(x))
                # <debug>
                if st_result[statement](70) == 1:
                   print(id(st_result[statement]), st_result[statement](70))
                #</debug>
            result[rule] = st_result
        return result

    def accumulate(self, activated):
        sub_result = {}

        # collect pairs (linguistic_variable, [func1, func2, ...])
        for rule in activated.keys():
            for st in activated[rule].keys():
                print("test of activated: {0}   {1}".format(id(activated[rule][st]), activated[rule][st](70)))
                if st.ling_var not in sub_result.keys():
                    sub_result[st.ling_var] = []
                sub_result[st.ling_var].append(activated[rule][st])

        # for each linguistic variable accumulate [func1, func2, ..] in 1 function (max, for example)
        result = {}
        for key in sub_result:
            def execute(x):
                values = [active(x) for active in sub_result[key]]
                return self.accumulator(values)
            result[key] = execute
            print("[debug] execute(70) = {0}".format(execute(70)))
        return result

    def defuzzificate(self, accumulated):
        result = {}
        for ling_var in accumulated.keys():
            d = self.defuzzificator(ling_var.universum[0], ling_var.universum[1], accumulated[ling_var], self.accuracy)
            result[ling_var] = d
        return result


class Utils:
    @staticmethod
    def get_varieties(statements, fuzzed_rule):
        result = []
        for statement in statements:
            result.append(fuzzed_rule[statement])
        return result

    @staticmethod
    def get_if_statements(rule):
        result = []
        st = rule.if_st
        while st is not None:
            result.append(st)
            st = st.next_st
        return result

    @staticmethod
    def is_have_operator(statements, operator):
        for statement in statements:
            if statement.logical_operator is operator:
                return True
        return False

class Activators:
    @staticmethod
    def min_activator(a, b): return min(a, b)


class Accumulators:
    @staticmethod
    def max_accumulator(*args): return max(*args)


class Defuzzificators:
    @staticmethod
    def center_of_gravity(start, end, function, accuracy):
        step = (end-start)/round((end-start) / accuracy)
        upper_integral = 0
        down_integral = 0
        cur = start
        while cur <= end:
            _ = function(cur)
            upper_integral += cur*_
            down_integral += _
            cur += step
        upper_integral -= (function(start)*start + function(end)*end)/2
        down_integral -= (function(start) + function(end))/2
        return upper_integral/down_integral



    @staticmethod
    def center_of_area(start, end, function, accuracy):
        pass

    @staticmethod
    def left_most_maximum(start, end, function, accuracy):
        result = []
        step = accuracy
        cur = start
        maximum = 0
        while cur < end:
            f = function(cur)
            result.append(f)
            if maximum < f:
                maximum = f
            cur += step
        for x in result:
            if x == maximum:
                return result.index(x) * step
        return None

    @staticmethod
    def right_most_maximum(start, end, function, accuracy):
        result = []
        step = accuracy
        cur = end
        maximum = 0
        while cur > start:
            f = function(cur)
            result.append(f)
            if maximum < f:
                maximum = f
            cur -= step
        for x in result[::-1]:
            if x == maximum:
                return x
        return None
