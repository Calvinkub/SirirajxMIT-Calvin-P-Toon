"""Patient-entered context. These inputs never grant clinical approval."""
from datetime import date, datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class InputModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class Username(InputModel):
    username: str = Field(min_length=3, max_length=32, pattern=r"^[A-Za-z0-9_.-]+$")

    @field_validator("username")
    @classmethod
    def normalize(cls, value):
        return value.lower()


class PatientDetails(InputModel):
    name: str = Field(min_length=1, max_length=80)
    age: int = Field(ge=18, le=110)
    sex: Literal["female", "male", "other", "prefer_not_to_say"] = "prefer_not_to_say"
    medicalRecordNumber: str = Field(default="", max_length=80)
    hospital: str = Field(default="", max_length=120)
    history: str = Field(default="", max_length=1500)
    allergies: str = Field(default="", max_length=500)
    goal: str = Field(min_length=1, max_length=250)


class Diagnosis(InputModel):
    name: str = Field(min_length=1, max_length=120)
    code: str = Field(default="", max_length=40)
    diagnosedOn: date | None = None
    notes: str = Field(default="", max_length=500)


class Medication(InputModel):
    name: str = Field(min_length=1, max_length=120)
    dose: str = Field(default="", max_length=80)
    frequency: str = Field(default="", max_length=120)
    notes: str = Field(default="", max_length=500)


class Measurement(InputModel):
    kind: Literal["heart_rate", "systolic_bp", "diastolic_bp", "weight", "height", "spo2", "glucose"]
    value: float = Field(gt=0, le=1000, allow_inf_nan=False)
    measuredAt: datetime
    notes: str = Field(default="", max_length=300)

    @field_validator("measuredAt")
    @classmethod
    def timezone_required(cls, value):
        if value.tzinfo is None:
            raise ValueError("Measurement time must include a timezone")
        return value


class CPET(InputModel):
    testDate: date
    doctorName: str = Field(min_length=1, max_length=120)
    vo2Peak: float | None = Field(default=None, gt=0, le=150, allow_inf_nan=False)
    heartRateVT1: float | None = Field(default=None, gt=0, le=300, allow_inf_nan=False)
    peakHeartRate: float | None = Field(default=None, gt=0, le=300, allow_inf_nan=False)
    reportNotes: str = Field(default="", max_length=1500)

    @model_validator(mode="after")
    def has_result(self):
        if all(v is None for v in (self.vo2Peak, self.heartRateVT1, self.peakHeartRate)) and not self.reportNotes:
            raise ValueError("Enter a CPET result or report notes, or skip CPET")
        return self


class Registration(Username):
    patient: PatientDetails
    diagnoses: list[Diagnosis] = Field(default_factory=list, max_length=30)
    medications: list[Medication] = Field(default_factory=list, max_length=30)
    medicationStatus: Literal["listed", "none", "unknown"] = "unknown"
    measurements: list[Measurement] = Field(default_factory=list, max_length=50)
    cpet: CPET | None = None

    @model_validator(mode="after")
    def medication_consistency(self):
        if self.medications and self.medicationStatus != "listed":
            raise ValueError("Medication status must be listed when medications are supplied")
        if not self.medications and self.medicationStatus == "listed":
            raise ValueError("Add a medication or select none/unknown")
        return self
