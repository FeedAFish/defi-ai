# SPDX-FileCopyrightText: 2022-present Vo Van Nghia <vanvnghia@gmail.com>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import os

import pandas as pd
from defi_ai.type import SQLSession
from sqlalchemy.sql.selectable import Select


def execute_to_df(session: SQLSession, statement: Select, columns: list[str] = None):
    rows = session.execute(statement).all()
    df = pd.DataFrame(
        [row._mapping for row in rows],
        columns=[c.name for c in statement.selected_columns]
        if not is_kaggle
        else columns,
    )
    return df


# TODO(vnghia): fix sqlalchemy while running on Kaggle
is_kaggle = "KAGGLE_URL_BASE" in os.environ
