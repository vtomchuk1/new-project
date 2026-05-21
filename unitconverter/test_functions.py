# SPDX-FileCopyrightText: 2025 Marco Mambelli
# SPDX-License-Identifier: Apache-2.0

from .functions import convert_imperial


def test_convert_imperial():
    assert convert_imperial("34 liters") == "34.0 liters"
    assert convert_imperial("1 lb") == "453.592 grams"
    assert convert_imperial("2 ounces") == "56.699 grams"
