
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
    )


truck.assign_driver("T. Nkosi")
truck.log_distance(320)
truck.service_completed(on=date(2026, 6, 1), next_due_km=95000)


print(truck.report())