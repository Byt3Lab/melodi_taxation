from core.db import Repository
from modules.melodi_taxation.models.tax_model import TaxZoneModel, TaxModel, TaxRuleModel
from core.orm import select

class TaxRepository(Repository):
    # --- Tax Zones ---
    async def get_all_tax_zones(self):
        async with self.get_session() as session:
            stmt = select(TaxZoneModel).order_by(TaxZoneModel.name)
            res = await session.execute(stmt)
            return list(res.scalars().all())

    async def get_tax_zone_by_id(self, tax_zone_id: str):
        async with self.get_session() as session:
            stmt = select(TaxZoneModel).filter_by(tax_zone_id=tax_zone_id)
            res = await session.execute(stmt)
            return res.scalars().first()

    async def create_tax_zone(self, data: dict):
        async with self.get_session() as session:
            zone = TaxZoneModel(**data)
            session.add(zone)
            await session.commit()
            return zone

    async def update_tax_zone(self, tax_zone_id: str, data: dict):
        async with self.get_session() as session:
            stmt = select(TaxZoneModel).filter_by(tax_zone_id=tax_zone_id)
            res = await session.execute(stmt)
            zone = res.scalars().first()
            if zone:
                for k, v in data.items():
                    setattr(zone, k, v)
                await session.commit()
                return zone
            return None

    async def delete_tax_zone(self, tax_zone_id: str):
        async with self.get_session() as session:
            stmt = select(TaxZoneModel).filter_by(tax_zone_id=tax_zone_id)
            res = await session.execute(stmt)
            zone = res.scalars().first()
            if zone:
                await session.delete(zone)
                await session.commit()
                return True
            return False

    # --- Taxes ---
    async def get_all_taxes(self):
        async with self.get_session() as session:
            stmt = select(TaxModel).order_by(TaxModel.name)
            res = await session.execute(stmt)
            return list(res.scalars().all())

    async def get_tax_by_id(self, tax_id: str):
        async with self.get_session() as session:
            stmt = select(TaxModel).filter_by(tax_id=tax_id)
            res = await session.execute(stmt)
            return res.scalars().first()

    async def create_tax(self, data: dict):
        async with self.get_session() as session:
            tax = TaxModel(**data)
            session.add(tax)
            await session.commit()
            return tax

    async def update_tax(self, tax_id: str, data: dict):
        async with self.get_session() as session:
            stmt = select(TaxModel).filter_by(tax_id=tax_id)
            res = await session.execute(stmt)
            tax = res.scalars().first()
            if tax:
                for k, v in data.items():
                    setattr(tax, k, v)
                await session.commit()
                return tax
            return None

    async def delete_tax(self, tax_id: str):
        async with self.get_session() as session:
            stmt = select(TaxModel).filter_by(tax_id=tax_id)
            res = await session.execute(stmt)
            tax = res.scalars().first()
            if tax:
                await session.delete(tax)
                await session.commit()
                return True
            return False

    # --- Tax Rules ---
    async def get_all_tax_rules(self):
        from sqlalchemy.orm import joinedload
        async with self.get_session() as session:
            stmt = select(TaxRuleModel).options(
                joinedload(TaxRuleModel.tax),
                joinedload(TaxRuleModel.tax_zone)
            ).order_by(TaxRuleModel.product_tax_category)
            res = await session.execute(stmt)
            return list(res.unique().scalars().all())

    async def get_tax_rule_by_id(self, tax_rule_id: str):
        from sqlalchemy.orm import joinedload
        async with self.get_session() as session:
            stmt = select(TaxRuleModel).options(
                joinedload(TaxRuleModel.tax),
                joinedload(TaxRuleModel.tax_zone)
            ).filter_by(tax_rule_id=tax_rule_id)
            res = await session.execute(stmt)
            return res.unique().scalars().first()

    async def create_tax_rule(self, data: dict):
        async with self.get_session() as session:
            rule = TaxRuleModel(**data)
            session.add(rule)
            await session.commit()
            return rule

    async def update_tax_rule(self, tax_rule_id: str, data: dict):
        async with self.get_session() as session:
            stmt = select(TaxRuleModel).filter_by(tax_rule_id=tax_rule_id)
            res = await session.execute(stmt)
            rule = res.scalars().first()
            if rule:
                for k, v in data.items():
                    setattr(rule, k, v)
                await session.commit()
                return rule
            return None

    async def delete_tax_rule(self, tax_rule_id: str):
        async with self.get_session() as session:
            stmt = select(TaxRuleModel).filter_by(tax_rule_id=tax_rule_id)
            res = await session.execute(stmt)
            rule = res.scalars().first()
            if rule:
                await session.delete(rule)
                await session.commit()
                return True
            return False
