"""Financial Model KPI calculation library.
Claude combines these functions to generate analysis scripts on the fly."""

def ltv(arpu, gross_margin, monthly_churn):
    return arpu * gross_margin / monthly_churn

def cac(total_marketing, new_paid_users):
    return total_marketing / new_paid_users

def ltv_cac_ratio(arpu, gross_margin, monthly_churn, total_marketing, new_paid_users):
    return ltv(arpu, gross_margin, monthly_churn) / cac(total_marketing, new_paid_users)

def cac_payback_months(cac_val, arpu, gross_margin):
    return cac_val / (arpu * gross_margin)

def burn_multiple(net_burn, net_new_arr):
    return net_burn / net_new_arr if net_new_arr else float('inf')

def rule_of_40(revenue_growth_pct, ebitda_margin_pct):
    return revenue_growth_pct + ebitda_margin_pct

def runway_months(cash_balance, monthly_net_burn):
    return cash_balance / monthly_net_burn if monthly_net_burn > 0 else float('inf')

def arr_waterfall(new_mrr, expansion_mrr, contraction_mrr, churn_mrr):
    net_new = new_mrr + expansion_mrr - contraction_mrr - churn_mrr
    return {"net_new_mrr": net_new, "net_new_arr": net_new * 12}

def quick_ratio(new_mrr, expansion_mrr, contraction_mrr, churn_mrr):
    return (new_mrr + expansion_mrr) / (contraction_mrr + churn_mrr)

def nrr(beginning_mrr, expansion, contraction, churn):
    return (beginning_mrr + expansion - contraction - churn) / beginning_mrr
