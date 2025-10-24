"""
LIMITATIONS
- 各サンプルは常に「異なる2変数」を用います（random.sample(..., k=2)）。
  したがって同一サンプル内で両変数が同じ真偽値になることはありません（2つ目は1つ目の否定に固定）。必要に応じて変更してください。
- 'imply'（→）は内部で '>>' に置換して sympify に渡していますが、含意の扱いが意図どおりでない可能性があります。
  必要なら sympy.Implies を明示的に使うことを検討してください。
- depthを大きくすると再帰的に長大な式が生成され、sympifyや評価に時間・メモリがかかります。
- malformedな式や重複が続くと早期終了する仕組みがあるため、要求した総数を満たせないことがあります。
- 使用可能な演算子は最大4種類までです。
"""

import random
from sympy import *
from sympy.logic import SOPform, POSform
import json
import argparse
import sys

variables = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
             'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

# operator name -> symbol mapping
OP_NAME_TO_SYMBOL = {
    'and': '∧',
    'or': '∨',
    'not': '¬',
    'imply': '→'
}

def parse_operators_list(op_arg):
    # accepts list (from argparse nargs='+') or comma/space separated operator names
    if not op_arg:
        return ['∧', '∨']  # default
    if isinstance(op_arg, list):
        parts = [p.strip() for p in op_arg if p.strip()]
    else:
        parts = [p.strip() for p in op_arg.replace(',', ' ').split() if p.strip()]
    symbols = []
    for p in parts:
        key = p.lower()
        if key not in OP_NAME_TO_SYMBOL:
            raise ValueError(f"Unknown operator '{p}'. Allowed: and, or, not, imply")
        symbols.append(OP_NAME_TO_SYMBOL[key])
    if len(symbols) == 0 or len(symbols) > 4:
        raise ValueError("Specify between 1 and 4 operators.")
    return symbols

class PropositionGenerator:
    def __init__(self, operators):
        # per-instance state to avoid global TF/used_variables
        self.variables = variables
        self.operators = operators
        self.TF_dict = {}
        self.used_variables = []
        self.variables_ = random.sample(self.variables, k=2)

    def generate_proposition(self, depth):
        # assign TF for the chosen two variables so they are different
        self.TF_dict[self.variables_[0]] = random.choice([True, False])
        self.TF_dict[self.variables_[1]] = not self.TF_dict[self.variables_[0]]

        if depth == 0:
            # ensure both variables used at least once across samples logic
            if len(self.used_variables) == 1:
                if self.variables_[0] != self.used_variables[0]:
                    variable = self.variables_[0]
                else:
                    variable = self.variables_[1]
            else:
                variable = random.choice(self.variables_)
            self.used_variables.append(variable)
            return variable

        operator = random.choice(self.operators)
        if operator == '¬':
            return f'¬ ({self.generate_proposition(depth - 1)})'
        else:
            left_subexpression = self.generate_proposition(depth - 1)
            right_subexpression = self.generate_proposition(depth - 1)
            return f'({left_subexpression} {operator} {right_subexpression})'

def evaluate_proposition_str(proposition_str, TF_dict):
    # prepare sympy symbols
    symbols_dict = {v: symbols(v) for v in variables}
    # convert to sympy-friendly string
    sympy_expr_str = proposition_str.replace('¬', '~').replace('∨', '|').replace('∧', '&').replace('→', '>>')
    try:
        proposition = sympify(sympy_expr_str, locals=symbols_dict)
    except Exception as e:
        # If sympify fails, treat as invalid (should rarely happen)
        raise
    substitutions = {symbols_dict[v]: TF_dict[v] for v in TF_dict}
    answer = proposition.subs(substitutions)
    # Convert sympy BooleanTrue/False to Python bool reliably
    return bool(answer)

def readable_text_from_sample(tf_dict, used_vars, proposition):
    # similar to original create_text_for_json's textual format
    text_list = []
    text = ""
    for variable in used_vars:
        if variable in tf_dict:
            tmp = f"{variable} is {tf_dict[variable]}, "
            text_list.append(tmp)
    # unique items and stable ordering by sorting to normalize
    text_set = sorted(set(text_list))
    for item in text_set:
        text = ''.join([text, item])
    text = ''.join([text, proposition])
    return text

def create_json_file_from_mapping(final_list, operators_symbols, depth):
    # final_list is list of tuples (text, cls)
    filename = ''.join(operators_symbols) + str(depth) + '.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump([{"text": t, "cls": cls} for t, cls in final_list], f, ensure_ascii=False, indent=4)
    print(f"Wrote {len(final_list)} samples to {filename}")

def main():
    parser = argparse.ArgumentParser(description="Generate propositional logic dataset.")
    parser.add_argument('--n', type=int, required=True, help="Total number of samples to generate (must be even).")
    parser.add_argument('--depth', type=int, required=True, help="Max depth for generated propositions (non-negative int).")
    parser.add_argument('--ops', required=True, help="Operators to use (names): and, or, not, imply. Up to 4, space/comma separated.", nargs='+')
    args = parser.parse_args()

    total = args.n
    if total % 2 != 0:
        print("Error: --n must be even to have equal True/False counts.")
        sys.exit(1)
    depth_arg = args.depth
    if depth_arg < 0:
        print("Error: --depth must be >= 0")
        sys.exit(1)

    try:
        ops_symbols = parse_operators_list(args.ops)
    except ValueError as e:
        print("Error parsing operators:", e)
        sys.exit(1)

    # Warning (non-blocking) for potentially infeasible settings
    if len(ops_symbols) == 1 and depth_arg <= 2:
        print(f"WARNING: Only 1 operator with depth={depth_arg} may not generate enough unique samples.")
        print(f"Estimated unique samples may be less than {total}. Consider:")
        print("  - Increasing --depth (e.g., 3 or higher)")
        print("  - Adding more operators (e.g., --ops and or)")
        # do not block; continue automatically

    half = total // 2
    true_count = 0
    false_count = 0
    final_list = []
    seen_keys = set()
    attempts = 0

    # Safer max attempts (proportional to requested size) to avoid indefinite runs
    max_attempts = max(100000, total * 2000)

    # Track consecutive attempts that made no progress; helps terminate when stuck
    consecutive_no_progress = 0
    max_no_progress = max(5000, total * 50)

    while (true_count < half or false_count < half) and attempts < max_attempts:
        attempts += 1
        gen = PropositionGenerator(ops_symbols)
        prop = gen.generate_proposition(depth_arg)
        tf = gen.TF_dict.copy()
        used_vars = gen.used_variables.copy()
        try:
            ans = evaluate_proposition_str(prop, tf)
        except Exception:
            # skip malformed propositions
            consecutive_no_progress += 1
            if consecutive_no_progress >= max_no_progress:
                print("Stalled: many consecutive malformed/duplicate/no-progress attempts. Aborting early.")
                break
            continue

        # canonical uniqueness key: json of assignments + proposition sorted
        key = json.dumps({"assign": {k: tf[k] for k in sorted(tf.keys())}, "prop": prop}, sort_keys=True)
        if key in seen_keys:
            consecutive_no_progress += 1
            if consecutive_no_progress >= max_no_progress:
                print("Stalled: many consecutive duplicate/no-progress attempts. Aborting early.")
                break
            continue

        if ans and true_count >= half:
            consecutive_no_progress += 1
            if consecutive_no_progress >= max_no_progress:
                print("Stalled: unable to find more True samples. Aborting early.")
                break
            continue
        if (not ans) and false_count >= half:
            consecutive_no_progress += 1
            if consecutive_no_progress >= max_no_progress:
                print("Stalled: unable to find more False samples. Aborting early.")
                break
            continue

        # accept sample -> reset no-progress counter
        consecutive_no_progress = 0
        seen_keys.add(key)
        text = readable_text_from_sample(tf, used_vars, prop)
        cls = '1' if ans else '0'
        final_list.append((text, cls))
        if ans:
            true_count += 1
        else:
            false_count += 1

    if attempts >= max_attempts:
        print("Max attempts reached before filling dataset. Produced:", len(final_list))
    else:
        print(f"Generated {len(final_list)} samples (True: {true_count}, False: {false_count}) in {attempts} attempts.")

    create_json_file_from_mapping(final_list, ops_symbols, depth_arg)

if __name__ == "__main__":
    main()
