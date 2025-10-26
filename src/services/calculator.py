

def calculate_cost(team_roles, coefficients):
    base_cost = 0
    total_coefficient = 1
    total_cost = 0

    for role in team_roles:
        base_cost += role["count"] * role["rate"]

    for coef in coefficients:
        total_coefficient *= coef

    total_cost = base_cost * total_coefficient
    return total_cost