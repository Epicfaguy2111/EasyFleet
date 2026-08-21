
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
    """Legal maximum overall dimensions (in metres) for a vehicle type."""
    vehicle_type: VehicleType
    max_length_m: float
    max_width_m: float
    max_height_m: float

    def check(self, length_m: float, width_m: float, height_m: float) -> dict:
        return {
            "length_ok": length_m <= self.max_length_m,
            "width_ok": width_m <= self.max_width_m,
            "height_ok": height_m <= self.max_height_m,
        }

    def is_compliant(self, length_m: float, width_m: float, height_m: float) -> bool:
        return all(self.check(length_m, width_m, height_m).values())


LEGAL_LIMITS: dict[VehicleType, LegalDimensionalLimits] = {
    VehicleType.SINGLE_RIGID: LegalDimensionalLimits(
        vehicle_type=VehicleType.SINGLE_RIGID,
        max_length_m=12.5,
        max_width_m=2.6,
        max_height_m=4.3,
    ),
    VehicleType.ARTICULATED: LegalDimensionalLimits(
        vehicle_type=VehicleType.ARTICULATED,
        max_length_m=18.5,
        max_width_m=2.6,
        max_height_m=4.3,
    ),
    VehicleType.OTHER_COMBINATION: LegalDimensionalLimits(
        vehicle_type=VehicleType.OTHER_COMBINATION,
        max_length_m=22.0,
        max_width_m=2.6,
        max_height_m=4.3,
    ),
}
@dataclass
class Truck:
    vin: str
    fleet_number: str
    make: str
    model: str
    year: int


    fuel_type: FuelType = FuelType.DIESEL
    gross_vehicle_weight_kg: float = 0.0     
    payload_capacity_kg: float = 0.0
    engine_power_kw: float = 0.0
    fuel_tank_capacity_l: float = 0.0
    axle_count: int = 2

    vehicle_type: VehicleType = VehicleType.SINGLE_RIGID
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



    def log_distance(self, km_driven: float) -> None:
        """Add distance travelled to the odometer."""
        if km_driven < 0:
            raise ValueError("km_driven cannot be negative")
        self.odometer_km += km_driven

    def assign_driver(self, driver_name: str) -> None:
        self.assigned_driver = driver_name

    def service_completed(self, on: date, next_due_km: float) -> None:
        """Record a completed service and set the next service threshold."""
        self.last_service_date = on
        self.next_service_due_km = next_due_km
        self.status = TruckStatus.ACTIVE

    def set_status(self, status: TruckStatus) -> None:
        self.status = status
    @property
    def legal_limits(self) -> LegalDimensionalLimits:
        """The legal dimensional limits that apply to this truck's vehicle type."""
        return LEGAL_LIMITS[self.vehicle_type]
    
    @property
    def is_dimensionally_compliant(self) -> bool:
        """Whether the truck's current length/width/height are within legal limits."""
        return self.legal_limits.is_compliant(self.length_m, self.width_m, self.height_m)
    
    def dimension_check(self) -> dict:
        """Detailed pass/fail breakdown per dimension against the legal limits."""
        return self.legal_limits.check(self.length_m, self.width_m, self.height_m)

    def to_dict(self) -> dict:
        """Flatten to a plain dict, e.g. for saving to CSV/DB/JSON."""
        data = self.__dict__.copy()
        data["fuel_type"] = self.fuel_type.value
        data["status"] = self.status.value
        if self.last_service_date:
            data["last_service_date"] = self.last_service_date.isoformat()
        return data

    def __str__(self) -> str:
        return (
            f"[{self.fleet_number}] {self.year} {self.make} {self.model} "
            f"({self.fuel_type.value}, {self.status.value}) - "
            f"{self.odometer_km:,.0f} km"
        )
    
    def report(self) -> str:
        due_flag = " (DUE)" if self.is_service_due else ""
        next_due = (
            f"{self.next_service_due_km:,.0f} km{due_flag}"
            if self.next_service_due_km is not None else "-"
        )
        last_service = (
            self.last_service_date.isoformat() if self.last_service_date else "-"
        )
        driver = self.assigned_driver or "Unassigned"
 
        limits = self.legal_limits
        compliance = "PASS" if self.is_dimensionally_compliant else "FAIL - over limit"
 
        rows = [
            ("Fleet Number",    self.fleet_number),
            ("VIN",             self.vin),
            ("Vehicle",         f"{self.year} {self.make} {self.model}"),
            ("Status",          self.status.value.replace("_", " ").title()),
            ("Fuel Type",       self.fuel_type.value.title()),
            ("Odometer",        f"{self.odometer_km:,.0f} km"),
            ("GVWR",            f"{self.gross_vehicle_weight_kg:,.0f} kg"),
            ("Payload Capacity",f"{self.payload_capacity_kg:,.0f} kg"),
            ("Engine Power",    f"{self.engine_power_kw:,.0f} kW"),
            ("Fuel Tank",       f"{self.fuel_tank_capacity_l:,.0f} L"),
            ("Axles",           str(self.axle_count)),
            ("Vehicle Type",    self.vehicle_type.value.replace("_", " ").title()),
            ("Length",          f"{self.length_m:.1f} m (limit {limits.max_length_m:.1f} m)"),
            ("Width",           f"{self.width_m:.1f} m (limit {limits.max_width_m:.1f} m)"),
            ("Height",          f"{self.height_m:.1f} m (limit {limits.max_height_m:.1f} m)"),
            ("Dimension Check", compliance),
            ("Driver",          driver),
            ("Last Service",    last_service),
            ("Next Service Due",next_due),
            ("Vehicle Age",     f"{self.age_years} yr"),
        ]
 
        label_width = max(len(label) for label, _ in rows)
        width = label_width + 3 + max(len(value) for _, value in rows)
        width = max(width, 40)
 
        lines = ["=" * width, " TRUCK SPEC SHEET".ljust(width), "=" * width]
        for label, value in rows:
            lines.append(f"{label:<{label_width}} : {value}")
        lines.append("=" * width)
 
        return "\n".join(lines)

if __name__ == "__main__":

    truck = Truck(
        vin="1HGCM82633A004352",
        fleet_number="FLT-001",
        make="Isuzu",
        model="FVZ 1400",
        year=2021,
        fuel_type=FuelType.DIESEL,
        gross_vehicle_weight_kg=16000,
        payload_capacity_kg=9500,
        engine_power_kw=210,
        fuel_tank_capacity_l=200,
        axle_count=2,
        odometer_km=85000,
        vehicle_type=VehicleType.ARTICULATED,
        length_m=17.2,
        width_m=2.6,
        height_m=4.1,
    )


truck.assign_driver("T. Nkosi")
truck.log_distance(320)
truck.service_completed(on=date(2026, 6, 1), next_due_km=95000)


print(truck.report())