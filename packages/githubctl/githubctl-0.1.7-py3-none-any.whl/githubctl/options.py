from enum import Enum


class OutputOption(str, Enum):
    json = "json"
    csv = "csv"
    table = "table"
