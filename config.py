from __future__ import annotations

from core.db.base_module_tables import BaseModuleTables

MODULE_NAME = "melodi_taxation"
PREFIX_TABLE = "ml_base_"


class TaxTables(BaseModuleTables):
    TAX_ZONES = f"{PREFIX_TABLE}tax_zones"
    TAXES = f"{PREFIX_TABLE}taxes"
    TAX_RULES = f"{PREFIX_TABLE}tax_rules"
