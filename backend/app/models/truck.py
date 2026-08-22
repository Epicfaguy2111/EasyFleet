from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Optional


class FuelType(Enum):
    DIESEL = "diesel"
    PETROL = "petrol"
    ELECTRIC = "electric"
    HYBRID = "hybrid"
    CNG = "cng"


class TruckStatus(Enum):
    ACTIVE = "active"
    IN_MAINTENANCE = "in_maintenance"
    OUT_OF_SERVICE = "out_of_service"
    RETIRED = "retired"


class VehicleType(Enum):
    SINGLE_RIGID = "single_rigid"
    ARTICULATED = "articulated"
    OTHER_COMBINATION = "other_combination"


@dataclass(frozen=True)
class LegalDimensionalLimits:
    vehicle_type: VehicleType
    max_length_m: float
    max_width_m: float
    max_height_m: float
    turning_radius_typical_m: float

    def check(self, length_m: float, width_m: float, height_m: float) -> dict:
        return {
            "length_ok": length_m <= self.max_length_m,
            "width_ok": width_m <= self.max_width_m,
            "height_ok": height_m <= self.max_height_m,
        }

    def is_compliant(
        self, length_m: float, width_m: float, height_m: float
    ) -> bool:
        return all(self.check(length_m, width_m, height_m).values())


LEGAL_LIMITS: dict[VehicleType, LegalDimensionalLimits] = {
    VehicleType.SINGLE_RIGID: LegalDimensionalLimits(
        vehicle_type=VehicleType.SINGLE_RIGID,
        max_length_m=12.5,
        max_width_m=2.6,
        max_height_m=4.3,
        turning_radius_typical_m=8.7,
    ),
    VehicleType.ARTICULATED: LegalDimensionalLimits(
        vehicle_type=VehicleType.ARTICULATED,
        max_length_m=18.5,
        max_width_m=2.6,
        max_height_m=4.3,
        turning_radius_typical_m=12.5,
    ),
    VehicleType.OTHER_COMBINATION: LegalDimensionalLimits(
        vehicle_type=VehicleType.OTHER_COMBINATION,
        max_length_m=22.0,
        max_width_m=2.6,
        max_height_m=4.3,
        turning_radius_typical_m=16.5,
    ),
}


@dataclass
class Truck:
    vin: str
    fleet_number: str
    registration: str
    make: str
    model: str
    year: int
    name: str = ""
    fuel_type: FuelType = FuelType.DIESEL
    vehicle_type: VehicleType = VehicleType.SINGLE_RIGID
    axle_count: int = 2
    engine_power_kw: float = 0.0
    gross_vehicle_weight_kg: float = 0.0
    payload_capacity_kg: float = 0.0
    fuel_tank_capacity_l: float = 0.0
    length_m: float = 0.0
    width_m: float = 0.0
    height_m: float = 0.0
    odometer_km: float = 0.0
    status: TruckStatus = TruckStatus.ACTIVE
    last_service_date: Optional[date] = None
    next_service_due_km: Optional[float] = None
    assigned_driver: Optional[str] = None
    notes: dict = field(default_factory=dict)

    @property
    def age_years(self) -> int:
        return date.today().year - self.year

    @property
    def is_service_due(self) -> bool:
        if self.next_service_due_km is None:
            return False
        return self.odometer_km >= self.next_service_due_km

    @property
    def legal_limits(self) -> LegalDimensionalLimits:
        return LEGAL_LIMITS[self.vehicle_type]

    @property
    def is_dimensionally_compliant(self) -> bool:
        return self.legal_limits.is_compliant(
            self.length_m, self.width_m, self.height_m
        )