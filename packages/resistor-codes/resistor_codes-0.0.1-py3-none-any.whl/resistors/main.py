'''
    Resistors codes is a program to convert resistor codes to resistance in Ohm-s.
    Copyright (C) 2024  Nikolay Rovinskiy

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
import argparse
import csv
import os
import re
from typing import Callable, Optional
from math import pow
import math
import sys

RE_DECIMAL = re.compile("^\\d+R\\d+$")
RE_NUMBER = re.compile("^\\d{3,4}$")
RE_EIA_96 = re.compile("^\\d{2}\\w$")

EIA_96_CODE = 'EIA_96_codes.csv'
EIA_96_MUL = 'EIA_96_mul.csv'

def parse_numbers(code: str) -> float:
    """
    Parse four letter code.

    :param code: The code written on the SMD resistor.
    :return: The resistance as an integer.
    """
    return int(code[:-1]) * pow(10, int(code[-1]))
    

def parse_decimal(code: str) -> float:
    """
    Parse three letter code.

    :param code: The code written on the SMD resistor.
    :return: The resistance as an integer.
    """
    return float(code.replace('R', '.'))
    
def parse_eia_96(code: str) -> float:
    """
    Parse EIA-96 code.

    :param code: The code written on the SMD resistor.
    :return: The resistance as an integer. If the code is invalid -1 will be returned.
    """
    # read resource tables
    resources_dir = os.path.join(os.path.dirname(__file__), 'resources')
    if not os.path.isdir(resources_dir):
        raise ValueError("The resource directory was not found. Please place it to the script directory.")
    codes = os.path.join(resources_dir, EIA_96_CODE)
    if not os.path.isfile(codes):
        raise ValueError(f"The {codes} file not found.")
    multipliers = os.path.join(resources_dir, EIA_96_MUL)
    if not os.path.isfile(multipliers):
        raise ValueError(f"The {multipliers} file not found.")
    dt_codes = {}
    with open(codes, newline='') as code_fh:
        reader = csv.DictReader(code_fh)
        for row in reader:
            if len(row['Code']) == 1:
                dt_codes['0' + row['Code']] = int(row['Value'])
            else:
                dt_codes[row['Code']] = int(row['Value'])
    dt_mul = {}
    with open(multipliers, newline='') as mul_fh:
        reader = csv.DictReader(mul_fh)
        for row in reader:
            dt_mul[row['Code']] = float(row['Multiplication'])
    cd = code[:2]
    mul = code[-1]
    if cd not in dt_codes:
        return -1
    if mul not in dt_mul:
        return -1
    return dt_codes[cd] * dt_mul[mul]

def select_code(code: str) -> Optional[Callable[[str], float]]:
    """
    Select the appropriate parser function.

    :param code: The code written on the SMD resistor.
    :return: The resistance as an integer.
    """
    if RE_NUMBER.match(code):
        return parse_numbers
    if RE_DECIMAL.match(code):
        return parse_decimal
    if RE_EIA_96.match(code):
        return parse_eia_96
    return None


def get_result(code: str) -> str:
    """
    Get the results string.

    :param code: The code written on the SMD resistor.
    """
    code = code.upper().strip()
    decode_fn = select_code(code)
    if decode_fn:
        resistance = decode_fn(code)
        if resistance == -1:
            return f'The EIA-96 code {code} cannot be recognized please check code and multiplier.'
        if resistance < 1E3:
            if math.ceil(resistance) == resistance:
                resistance = math.ceil(resistance)
            return f'{resistance} Ohm'
        elif resistance >= 1E3 and resistance < 1E6:
            return '{:.2f} kOhm'.format(resistance/1E3)
        return '{:.2f} MOhm'.format(resistance/1E6)
    return "The code can not be recognized as neither of three or four digits or EIA-96."

def main() -> None:
    """
    Main method.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("code", help="The code written on SMD resistor.")
    args = parser.parse_args()
    print(get_result(args.code))

if __name__ == '__main__':
    main()
