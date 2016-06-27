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
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

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

# fuzzy interface system initializtion
# also available: Difuzzificator.right_most_maximum
#                 Difuzzificator.left_most_maximum
#
fis = FuzzyInterfaceSystem(rule_base, AND, OR,
                           Activators.min_activator,
                           Accumulators.max_accumulator,
                           Defuzzificators.center_of_gravity,
                           0.05)
x_array = range(170, 237, 6)
y_array = range(0, 101, 5)
Z = []

print("start grid culculating")

for y in y_array:
    res = []
    for x in x_array:
        processed = fis.process({height: x, technique: y})
        # actually there is 1 key, but hi is in set
        for key in processed.keys():
            res.append(processed[key])
    # dirty hack of empty result bug
    if len(res) == 0:
        res = [0 for i in range(0, len(x_array))]
    Z.append(res)
    print(res)

new_Z = np.array(Z)

print("grid calculating completed")

X, Y = np.meshgrid(x_array, y_array)
print("x:\n", X)
print("y:\n", Y)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(Y, X, new_Z,  rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
plt.show()