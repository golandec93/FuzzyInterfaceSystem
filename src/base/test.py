from src.base.model.fuzzyset import LingVariable
from src.base.model.fuzzyset import MembershipFunctions
from src.base.model.fuzzyset import Term
from src.base.model.rulebase import RuleBase
from src.base.model.rulebase import Rule
from src.base.model.rulebase import Statement
from src.base.model.rulebase import LogicalOperator
from src.base.fis import FuzzyInterfaceSystem
from src.base.fis import Activators
from src.base.fis import Accumulators
from src.base.fis import Defuzzificators


def test_decorator(test):
    def decorated():
        res1 = "STARTING " + test.__name__
        stars = "*" * round(((72 - len(res1)) / 2))
        print(stars + res1 + stars)
        test()
        res1 = test.__name__ + " HAS BEEN SUCCESSFULLY EXECUTED"
        stars = "*" * round(((72 - len(res1)) / 2))
        print(stars + res1 + stars + "\n\n")

    return decorated


@test_decorator
def initialization_test():
    term1 = Term("test_term_1", MembershipFunctions.triangle, (0, 20, 30))
    term2 = Term("test_term_2", MembershipFunctions.triangle, (0, 20, 30))
    term3 = Term("test_term_3", MembershipFunctions.triangle, (0, 20, 30))
    print("terms created successfully")

    ling_var_1 = LingVariable("linguistic_1", [0, 30], term1)
    ling_var_2 = LingVariable("linguistic_2", [0, 30], term2)
    ling_out_var = LingVariable("linguistic_out", [0, 30], term3)
    print("linguistic variables created successfully")

    statement1 = Statement(ling_var_1, term1)
    statement2 = Statement(ling_var_2, term2, LogicalOperator.MIN, statement1)
    statement3 = Statement(ling_out_var, term3)
    print("statements created successfully")

    rule = Rule(statement2, statement3)
    print("rule created successfully")

    rule_base = RuleBase()
    rule_base.add(rule)
    print("rule has been successfully added to RuleBase")

    if MembershipFunctions.triangle(2.5, 2, 3, 4) == 0.5:
        print("MembershipFunctions.triangle and MembershipFunctions.trapeze works well")
    else:
        raise Exception("MembershipFunctions.triangle and MembershipFunctions.trapeze works bad")


@test_decorator
def algorithm_test():
    # linguistic variables and terms initialization
    technique = LingVariable("technique", [0, 100])
    tech_terms = [Term("bad", MembershipFunctions.trapeze, -1, -1, 10, 15),
                  Term("average", MembershipFunctions.trapeze, 10, 15, 30, 35),
                  Term("good", MembershipFunctions.trapeze, 25, 30, 45, 50),
                  Term("very_good", MembershipFunctions.trapeze, 60, 65, 85, 90),
                  Term("perfect", MembershipFunctions.trapeze, 75, 100, 101, 101)]
    technique.set_terms(*tech_terms)

    height = LingVariable("height", [170, 236])
    height_terms = [Term("Low", MembershipFunctions.trapeze, 169, 169, 189, 194),
                    Term("Average", MembershipFunctions.trapeze, 189, 194, 204, 209),
                    Term("High", MembershipFunctions.trapeze, 203, 209, 217, 222),
                    Term("VeryHigh", MembershipFunctions.trapeze, 217, 222, 237, 237)]
    height.append_terms(*height_terms)

    assurance = LingVariable("assurance", [0, 100])
    assurance_terms = [Term("full", MembershipFunctions.trapeze, 80, 85, 101, 101),
                       Term("average", MembershipFunctions.trapeze, 60, 65, 80, 85),
                       Term("small", MembershipFunctions.trapeze, 35, 40, 60, 65),
                       Term("do not take", MembershipFunctions.trapeze, -1, -1, 35, 40)]
    assurance.set_terms(*assurance_terms)

    # next 2 lines just for comfort
    AND = LogicalOperator.MIN
    OR = LogicalOperator.MAX

    # rule base initialization
    rule_base = RuleBase()

    if_sts = [
        Statement(technique, technique.term_by_name("perfect")) \
            .append_statement(AND, Statement(height, height.term_by_name("VeryHigh"))),
        Statement(technique, technique.term_by_name("perfect")) \
            .append_statement(AND, Statement(height, height.term_by_name("High"))),
        Statement(technique, technique.term_by_name("perfect")) \
            .append_statement(AND, Statement(height, height.term_by_name("Average"))),
        Statement(technique, technique.term_by_name("perfect")) \
            .append_statement(AND, Statement(height, height.term_by_name("Low"))),

        Statement(technique, technique.term_by_name("very_good")) \
            .append_statement(AND, Statement(height, height.term_by_name("VeryHigh"))),
        Statement(technique, technique.term_by_name("very_good")) \
            .append_statement(AND, Statement(height, height.term_by_name("High"))),
        Statement(technique, technique.term_by_name("very_good")) \
            .append_statement(AND, Statement(height, height.term_by_name("Average"))),
        Statement(technique, technique.term_by_name("very_good")) \
            .append_statement(AND, Statement(height, height.term_by_name("Low"))),

        Statement(technique, technique.term_by_name("good")) \
            .append_statement(AND, Statement(height, height.term_by_name("VeryHigh"))),
        Statement(technique, technique.term_by_name("good")) \
            .append_statement(AND, Statement(height, height.term_by_name("High"))),
        Statement(technique, technique.term_by_name("good")) \
            .append_statement(AND, Statement(height, height.term_by_name("Average"))),
        Statement(technique, technique.term_by_name("good")) \
            .append_statement(AND, Statement(height, height.term_by_name("Low"))),

        Statement(technique, technique.term_by_name("average")) \
            .append_statement(AND, Statement(height, height.term_by_name("VeryHigh"))),
        Statement(technique, technique.term_by_name("average")) \
            .append_statement(AND, Statement(height, height.term_by_name("High"))),
        Statement(technique, technique.term_by_name("average")) \
            .append_statement(AND, Statement(height, height.term_by_name("Average"))),
        Statement(technique, technique.term_by_name("average")) \
            .append_statement(AND, Statement(height, height.term_by_name("Low"))),

        Statement(technique, technique.term_by_name("bad")) \
            .append_statement(AND, Statement(height, height.term_by_name("VeryHigh"))),
        Statement(technique, technique.term_by_name("bad")) \
            .append_statement(AND, Statement(height, height.term_by_name("High"))),
        Statement(technique, technique.term_by_name("bad")) \
            .append_statement(AND, Statement(height, height.term_by_name("Average"))),
        Statement(technique, technique.term_by_name("bad")) \
            .append_statement(AND, Statement(height, height.term_by_name("Low")))
    ]
    then_sts = [
        Statement(assurance, assurance.term_by_name("full")),
        Statement(assurance, assurance.term_by_name("full")),
        Statement(assurance, assurance.term_by_name("average")),
        Statement(assurance, assurance.term_by_name("average")),

        Statement(assurance, assurance.term_by_name("full")),
        Statement(assurance, assurance.term_by_name("full")),
        Statement(assurance, assurance.term_by_name("average")),
        Statement(assurance, assurance.term_by_name("average")),

        Statement(assurance, assurance.term_by_name("full")),
        Statement(assurance, assurance.term_by_name("full")),
        Statement(assurance, assurance.term_by_name("average")),
        Statement(assurance, assurance.term_by_name("small")),

        Statement(assurance, assurance.term_by_name("average")),
        Statement(assurance, assurance.term_by_name("average")),
        Statement(assurance, assurance.term_by_name("small")),
        Statement(assurance, assurance.term_by_name("do not take")),

        Statement(assurance, assurance.term_by_name("small")),
        Statement(assurance, assurance.term_by_name("small")),
        Statement(assurance, assurance.term_by_name("small")),
        Statement(assurance, assurance.term_by_name("do not take")),
    ]

    for i in range(0, 20):
        rule_base.add(Rule(if_sts[i], then_sts[i]))
    print(rule_base)

    print("............................................start fuzzification............................................")
    fis = FuzzyInterfaceSystem(rule_base, AND, OR,
                               Activators.min_activator,
                               Accumulators.max_accumulator,
                               Defuzzificators.left_most_maximum,
                               0.005)
    signals = {technique: 40,
               height: 203}
    fuz_result = fis.fuzzificate(signals)

    for rule in fuz_result.keys():
        print(rule)
        r_keys = fuz_result[rule].keys()
        for key in r_keys:
            print("    {0}:{1}".format(key.get_single_str(), fuz_result[rule][key]))
    print(".........................................fuzzification completed...........................................")

    print(".............................................start aggregation.............................................")
    aggr_result = fis.aggregate(fuz_result)
    for key in aggr_result:
        print("{0} : {1}".format(key, aggr_result[key]))
    print(".........................................aggregation completed.............................................")

    print("............................................start activation...............................................")
    activation_result = fis.activate(aggr_result)
    print("..........................................activation completed.............................................")

    print("............................................start accumulation.............................................")
    accumulation_result = fis.accumulate(activation_result)
    print("..........................................accumulation completed...........................................")

    print("..........................................start defuzzification............................................")
    defuzzificated = fis.defuzzificate(accumulation_result)
    print("........................................defuzzification completed..........................................")
    for ling_var in defuzzificated:
        print("{0} : {1}".format(ling_var, defuzzificated[ling_var]))

    assert defuzzificated[assurance] == 65, "unexpected result! Check your algorithm"



try:
    initialization_test()
    algorithm_test()
except Exception as e:
    print("test failed\n\n" + str(e))
    raise e
