from __future__ import annotations

from decimal import Decimal
from core.routing import Request, Response
from core.utils.generate import gen_id_by_uuid4
from sqlalchemy import select, delete
from modules.melodi_taxation.models.tax_model import TaxModel, TaxZoneModel, TaxRuleModel


class TaxAPIController:
    @staticmethod
    async def list_taxes(request: Request, response: Response):
        async with request.module.app.db.get_session() as session:
            stmt_zones = select(TaxZoneModel).order_by(TaxZoneModel.name)
            res_zones = await session.execute(stmt_zones)
            zones = [
                {
                    "tax_zone_id": z.tax_zone_id,
                    "name": z.name,
                    "code": z.code,
                    "country_code": z.country_code,
                    "is_active": z.is_active,
                    "invoice_immutable_on_validation": z.invoice_immutable_on_validation,
                    "cash_rounding": z.cash_rounding
                }
                for z in res_zones.scalars().all()
            ]

            stmt_taxes = select(TaxModel).order_by(TaxModel.name)
            res_taxes = await session.execute(stmt_taxes)
            taxes = [
                {
                    "tax_id": t.tax_id,
                    "name": t.name,
                    "code": t.code,
                    "rate": float(t.rate),
                    "account_id": t.account_id,
                    "is_active": t.is_active
                }
                for t in res_taxes.scalars().all()
            ]

            stmt_rules = select(TaxRuleModel)
            res_rules = await session.execute(stmt_rules)
            rules = [
                {
                    "tax_rule_id": r.tax_rule_id,
                    "tax_zone_id": r.tax_zone_id,
                    "tax_id": r.tax_id,
                    "product_tax_category": r.product_tax_category
                }
                for r in res_rules.scalars().all()
            ]

            return response.send_json({
                "success": True,
                "data": {
                    "zones": zones,
                    "taxes": taxes,
                    "rules": rules
                }
            })

    @staticmethod
    async def save_tax(request: Request, response: Response):
        data = await request.json()
        tax_id = data.get("tax_id") or gen_id_by_uuid4(prefix="tax_")
        name = (data.get("name") or "").strip()
        code = (data.get("code") or "").strip()
        rate = Decimal(str(data.get("rate") or 0.0))

        if not name or not code:
            return response.send_json({"success": False, "error": "Nom et code de taxe requis"}, status=400)

        async with request.module.app.db.get_session() as session:
            stmt = select(TaxModel).filter_by(tax_id=tax_id)
            res = await session.execute(stmt)
            tax = res.scalar_one_or_none()
            if not tax:
                tax = TaxModel(tax_id=tax_id, name=name, code=code, rate=rate, is_active=data.get("is_active", True))
                session.add(tax)
            else:
                tax.name = name
                tax.code = code
                tax.rate = rate
                tax.is_active = data.get("is_active", True)
            await session.commit()

        return response.send_json({"success": True, "data": {"tax_id": tax_id, "name": name, "rate": float(rate)}})

    @staticmethod
    async def delete_tax(request: Request, response: Response):
        tax_id = (request.args.get("tax_id") or (await request.json()).get("tax_id") or "").strip()
        if not tax_id:
            return response.send_json({"success": False, "error": "Identifiant de taxe requis"}, status=400)

        async with request.module.app.db.get_session() as session:
            stmt = delete(TaxModel).where(TaxModel.tax_id == tax_id)
            await session.execute(stmt)
            await session.commit()

        return response.send_json({"success": True, "message": f"Taxe {tax_id} supprimée"})
