
import plotly.graph_objects as go
# import plotly.express as px

THE_INPUT_AMOUNT = 40000
MAX_BTC_FEE = 10000.0   # this is a fixed value regardless of transaction length
DELTA = 1.0
kI = 70/100.0   # issuer coeficient
kC = 15/100.0   # creditor coeficient
kB = 0.01/100.0   # burn coeficient
MainTransactions = []
GuaranteeTransactions = []
CheatingTransactions = []


class Transaction:
    def __init__(self, creditor, issuerChangeBack, burn=0, BTCFee=MAX_BTC_FEE, input=THE_INPUT_AMOUNT):
        self.creditor = creditor
        self.issuerChangeBack = issuerChangeBack
        self.burn = burn
        self.BTCFee = BTCFee
        self.input = input


credit_as_x = []
issuer_outputs_in_MT_as_y = []
issuer_outputs_in_GT_as_y = []
issuer_outputs_in_CT_as_y = []
issuer_cheating_benefit_as_y = []
GT_burn_as_y = []
CT_BTC_fee_as_y = []
crossPointX = 0
for creditor_amount in range(1, THE_INPUT_AMOUNT):

    # main transaction
    MT_creditor_output = creditor_amount * 1.0
    MT_BTC_fee = MAX_BTC_FEE
    MT_issuer_output = THE_INPUT_AMOUNT - MT_BTC_fee - MT_creditor_output
    credit_as_x.append(MT_creditor_output)
    issuer_outputs_in_MT_as_y.append(MT_issuer_output)

    # guarantee transaction
    GT_issuer_output = MT_issuer_output * kI
    GT_creditor_output = MT_creditor_output * kC
    issuer_outputs_in_GT_as_y.append(GT_issuer_output)
    cuttingPart = (MT_issuer_output - GT_issuer_output) + \
        (MT_creditor_output - GT_creditor_output)
    GT_burn = cuttingPart * kB
    GT_burn_as_y.append(GT_burn)
    GT_BTC_fee = MT_BTC_fee + (cuttingPart - GT_burn)

    # cheating transaction
    CT_creditor_output = 0
    CT_burn = 0
    CT_BTC_fee = GT_BTC_fee + DELTA
    CT_issuer_output = THE_INPUT_AMOUNT - CT_BTC_fee
    issuer_outputs_in_CT_as_y.append(CT_issuer_output)
    CT_BTC_fee_as_y.append(CT_BTC_fee)

    # complementry information
    issuer_cheating_benefit_as_y.append(CT_issuer_output-MT_issuer_output)
    if int(MT_issuer_output) == int(CT_issuer_output):
        crossPointX = MT_creditor_output

fig = go.Figure([
    go.Scatter(x=credit_as_x, y=issuer_outputs_in_MT_as_y,
               name='Main Transaction Issuer change back'),
    go.Scatter(x=credit_as_x, y=issuer_outputs_in_GT_as_y,
               name='Guarantee Transaction Issuer change back'),
    go.Scatter(x=credit_as_x, y=issuer_outputs_in_CT_as_y,
               name='Cheating Transaction Issuer change back'),

    go.Scatter(x=credit_as_x, y=issuer_cheating_benefit_as_y,
               name='Issuer cheating benefit'),
    go.Scatter(x=credit_as_x, y=CT_BTC_fee_as_y,
               name='CT BTC Fee'),
    go.Scatter(x=credit_as_x, y=GT_burn_as_y,
               name='Burned Satoshis'),
])

fig.update_layout(
    title="1.0. Security checks (Cheating benefits starts from " +
    "{:,}".format(int(crossPointX)) + " Satoshi debt)",
    xaxis_title="Creditor(s) output amount",
    yaxis_title="Issuer change back amount",
    legend_title="Input:" + "{:,}".format(int(THE_INPUT_AMOUNT))
    + "\n\r" + "BTC fee:" + "{:,}".format(int(MAX_BTC_FEE))
    + "\n" + "kI:" + str(kI)
    + "\n" + "kC:" + str(kC)
    + "\n" + "kB:" + str(kB)
    + "\n" + "Delta:" + "{:,}".format(int(DELTA)),
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
    )
)

fig.show()
