import json

def load_policies():
    with open("policies.json", "r") as file:
        return json.load(file)

def check_compliance(data, policies):
    violations = []
    for policy, requirement in policies.items():
        if not requirement(data):
            violations.append(policy)
    return violations

def generate_report(violations):
    report = "Compliance Report\n\n"
    if violations:
        report += "The following compliance violations were found:\n"
        for violation in violations:
            report += f"- {violation}\n"
    else:
        report += "No compliance violations found."
    return report
