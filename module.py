from __future__ import annotations

from core.module import ApplicationModule
from modules.melodi_taxation.controllers.api import TaxAPIController


class TaxationModule(ApplicationModule):
    def __init__(self):
        super().__init__(name="melodi_taxation", router_name="melodi_taxation")

    async def load(self):
        # Routes API
        self.api_router.add_route("/taxes", TaxAPIController.list_taxes, methods=["GET"])
        self.api_admin_router.add_route("/taxes", TaxAPIController.list_taxes, methods=["GET"])
        self.api_admin_router.add_route("/taxes", TaxAPIController.save_tax, methods=["POST"])
        self.api_admin_router.add_route("/taxes/delete", TaxAPIController.delete_tax, methods=["POST"])


module = TaxationModule()
