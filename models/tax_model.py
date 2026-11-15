from datetime import datetime
from typing import Optional
from decimal import Decimal
from core.orm import func
from core.orm.model import BaseModel, Mapped, mapped_column, relationship, String, Boolean, DateTime, Numeric, ForeignKey
from modules.melodi_taxation.config import TaxTables as BaseTables

class TaxModel(BaseModel):
    __tablename__ = BaseTables.TAXES

    tax_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    rate: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    account_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    rules = relationship("TaxRuleModel", back_populates="tax", cascade="all, delete-orphan")


class TaxRuleModel(BaseModel):
    __tablename__ = BaseTables.TAX_RULES

    tax_rule_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    tax_zone_id: Mapped[str] = mapped_column(String(100), ForeignKey(f"{BaseTables.TAX_ZONES}.tax_zone_id", ondelete="CASCADE"), nullable=False)
    product_tax_category: Mapped[str] = mapped_column(String(100), default="STANDARD", index=True, nullable=False)
    tax_id: Mapped[str] = mapped_column(String(100), ForeignKey(f"{BaseTables.TAXES}.tax_id", ondelete="CASCADE"), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    created_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Relationships
    tax = relationship(
        "TaxModel",
        back_populates="rules",
        lazy="selectin"
    )
    
    tax_zone = relationship(
        "TaxZoneModel",
        lazy="selectin"
    )


class TaxZoneModel(BaseModel):
    __tablename__ = BaseTables.TAX_ZONES

    tax_zone_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    country_code: Mapped[str] = mapped_column(String(2), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    
    # Compliance & Invoicing Rules
    invoice_immutable_on_validation: Mapped[bool] = mapped_column(Boolean, default=True)
    cash_rounding: Mapped[bool] = mapped_column(Boolean, default=False)
    legal_mentions: Mapped[Optional[str]] = mapped_column(String(2000), nullable=True)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
    created_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
