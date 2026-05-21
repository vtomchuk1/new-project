# SPDX-FileCopyrightText: 2025 Marco Mambelli
# SPDX-License-Identifier: Apache-2.0

import numpy as np

OUNCE_TO_GRAM = 28.3495
POUND_TO_GRAM = 453.592
OZ_NAMES = ("oz", "ounce", "ounces")
LB_NAMES = ("lb", "pound", "pounds")
GR_NAMES = ("gr", "g", "gram", "grams")


def convert_imperial(measure: str) -> str:
    """Converts a string "value imperial_unit" to the equivalent "value metric_unit"

    Works for lb/pounds and oz/ounce/ounces.
    Value must be a valid float number.

    Args:
        measure(str): "value imperial_unit" string

    Returns:
        str: converted value followed by the metric unit
    """
    measure_el = measure.split()
    value = float(measure_el[0])
    unit = "grams"
    if measure_el[1] in OZ_NAMES:
        value *= OUNCE_TO_GRAM
    elif measure_el[1] in LB_NAMES:
        value *= POUND_TO_GRAM
    else:
        unit = measure_el[1]
    return f"{value} {unit}"


def convert_lines(recipe_lines: list) -> list:
    """Convert units on all lines of a recipe.

    If the second word of a line (the third if the first is an itemization element)
    is an imperial unit, convert the value and unit to the corresponding grams.

    Args:
        recipe_lines(list): text lines of a recipe

    Returns:
        list: same recipe lines with units converted
    """

    new_lines = []
    for line in recipe_lines:
        i = line.split(maxsplit=4)
        if len(i) < 2:
            new_lines.append(line)
        pre = ""
        end = ""
        measure = f"{i[0]} {i[1]}"
        if len(i) > 2:
            if i[0] in ("*", "#", "-"):
                measure = f"{i[1]} {i[2]}"
                pre = f"{i[0]} "
                if len(i) > 3:
                    end = f" {i[3]}"
            else:
                end = " " + " ".join(i[2:])
        measure = convert_imperial(measure)
        new_lines.append(f"{pre}{measure}{end}")
    return new_lines


# The pipe operator for types requires Python 3.10 - uncomment when available:
# def multiconvert_units(values: list, unit: str, new_unit: str) -> list | None:
def multiconvert_units(values: list, unit: str, new_unit: str):
    """Convert a set of values from the current unit to the new one.

    Args:
        values(list): list of values
        unit(str): current unit of the values
        new_unit(str): new unit of the values

    Returns:
        list: converted values in the new unit
    """
    conv_dict = {"oz": OUNCE_TO_GRAM, "lb": POUND_TO_GRAM}
    for units in (OZ_NAMES, LB_NAMES, GR_NAMES):
        if unit in units:
            unit = units[0]
            break
    else:
        print(f"Invalid unit of the values '{unit}'. Returning None")
        return None
    for units in (OZ_NAMES, LB_NAMES, GR_NAMES):
        if new_unit in units:
            new_unit = units[0]
            break
    else:
        print(f"Invalid new unit '{new_unit}'. Returning None")
        return None
    if unit == new_unit:
        conversion = 1.0
    elif new_unit == "gr":
        conversion = conv_dict[unit]
    elif unit == "gr":
        conversion = 1.0 / conv_dict[new_unit]
    elif unit == "oz":
        # oz to lb
        conversion = 1.0 / 16
    else:
        # Only lb to oz left
        conversion = 16.0
    value_array = np.array(values)
    res_array = value_array * conversion
    return res_array.tolist()
