# ruff: noqa: UP007, D101, E501
"""Defines SQLAlchemy models and tables for everything in dodata.

Please refrain from adding special methods directly to the models. Strive for:
    models.py:
        class MyModel(SQLModel):

    mymodel.py:
        def special_method(obj):
            ...
"""
from datetime import UTC, datetime
from enum import StrEnum
from typing import Optional, TypeAlias, Union

from sqlalchemy import JSON, CheckConstraint
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlmodel import Column, Field, Relationship, SQLModel, UniqueConstraint

CellAttributes: TypeAlias = Union[
    list[int | float | str | bool | bool],
    str,
    int,
    float,
    bool,
    None,
]

Attributes: TypeAlias = dict[str, Union[int, float, str, "Attributes"]]

JSON_VARIANT = JSONB().with_variant(JSON(), "sqlite")  # type: ignore[no-untyped-call]


def _now() -> datetime:
    return datetime.now(UTC)


class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    """Primary key (unique identifier) for the project."""
    name: str = Field(index=True, unique=True)
    """The name of the project."""
    suffix: str = Field(index=True)
    """Filetype extension of the project's EDA file (gds, gds.gz, or oas)."""
    description: Optional[str]
    """Description of the project."""
    timestamp: datetime = Field(default_factory=_now, index=True)
    """The date and time (UTC) when the project was created."""
    cells: list["Cell"] = Relationship(
        back_populates="project", sa_relationship_kwargs={"cascade": "all, delete"}
    )
    """The cells in this project."""
    wafers: list["Wafer"] = Relationship(
        back_populates="project", sa_relationship_kwargs={"cascade": "all, delete"}
    )
    """Wafers manufactured and uploaded for this project."""


class Cell(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("project_id", "name", name="unique_name_and_project_on_cell"),
    )
    id: Optional[int] = Field(default=None, primary_key=True)
    """The primary key (unique identifier) for this cell."""
    name: str = Field(index=True)
    """The cell name."""
    attributes: CellAttributes = Field(sa_column=Column(JSON_VARIANT), default={})
    """Attributes associated with this cell, stored as JSON."""
    project_id: int = Field(foreign_key="project.id")
    """The associated project id."""
    project: Project = Relationship(back_populates="cells")
    """The associated project."""
    timestamp: datetime = Field(default_factory=_now, index=True)
    """The date and time (UTC) when this cell was uploaded."""
    devices: list["Device"] = Relationship(
        back_populates="cell",
        sa_relationship_kwargs={
            "cascade": "all, delete",
            "foreign_keys": "Device.cell_id",
        },
    )
    """Devices associated with this cell."""


class Device(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint(
            "x",
            "y",
            "angle",
            "mirror",
            "parent_cell_id",
            "cell_id",
            name="unique_coord_cells_on_device",
        ),
        UniqueConstraint("cell_id", "name", name="unique_device_names_per_cell"),
        CheckConstraint(
            "parent_cell_id <> cell_id", name="unique_device_cell_references"
        ),
        CheckConstraint(
            "(parent_cell_id IS NULL and x IS NULL and y IS NULL and angle is NULL and mirror is NULL)"
            " OR "
            "(parent_cell_id IS NOT NULL and x IS NOT NULL and y IS NOT NULL and angle IS NOT NULL and mirror IS NOT NULL)",
            name="parent_cell_coordinate_reference_not_null",
        ),
    )
    id: Optional[int] = Field(default=None, primary_key=True)
    """The primary key (unique identifier) for this device."""
    cell: Cell = Relationship(
        back_populates="devices",
        sa_relationship_kwargs={"foreign_keys": "Device.cell_id"},
    )
    """The cell associated with this device."""
    cell_id: int = Field(foreign_key="cell.id")
    """The id of the cell associated with this device."""
    name: str = Field(index=True)
    """The name of this device."""
    attributes: dict = Field(sa_column=Column(JSON_VARIANT), default={})  # type: ignore[type-arg]
    """Attributes associated with this device, stored as JSON."""
    x: Optional[float] = Field(default=None, index=True)
    """The x location of the device (its origin), relative to the parent cell."""
    y: Optional[float] = Field(default=None, index=True)
    """The y location of the device (its origin), relative to the parent cell."""
    angle: Optional[float] = Field(default=None, index=True)
    """The angle of rotation of the device, relative to the parent cell."""
    mirror: Optional[bool] = Field(default=None, index=True)
    """True if the device has been mirrored."""
    parent_cell: Optional[Cell] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "Device.parent_cell_id"}
    )
    """The parent cell and reference frame for the device."""
    parent_cell_id: Optional[int] = Field(
        default=None, foreign_key="cell.id", nullable=True
    )
    """The parent cell id."""
    timestamp: datetime = Field(default_factory=_now, index=True)
    """The date and time (UTC) when the device was uploaded."""
    device_data: list["DeviceData"] = Relationship(
        back_populates="device", sa_relationship_kwargs={"cascade": "all, delete"}
    )
    """Data entries associated with he device."""


class Wafer(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint(
            "project_id",
            "name",
            "lot_name",
            name="unique_wafer_name_lot_name_per_project",
        ),
    )
    id: Optional[int] = Field(default=None, primary_key=True)
    """The primary key (unique identifier) of the wafer."""
    name: str = Field(index=True)
    """The name of the wafer."""
    description: Optional[str]
    """Description of the wafer."""
    lot_name: Optional[str] = Field(default=None, index=True)
    """The name of the lot which this wafer belongs to (optional)."""
    attributes: dict = Field(sa_column=Column(JSON_VARIANT), default={})  # type: ignore[type-arg]
    """Attributes associated with the wafer, in JSON format."""
    timestamp: datetime = Field(default_factory=_now, index=True)
    """The date and time (UTC) when this wafer was uploaded."""
    project_id: int = Field(foreign_key="project.id")
    """The id of the project associated with this wafer."""
    project: Project = Relationship(back_populates="wafers")
    """The project associated with this wafer."""
    dies: list["Die"] = Relationship(
        back_populates="wafer", sa_relationship_kwargs={"cascade": "all, delete"}
    )
    """Dies in this wafer."""
    analysis: list["Analysis"] = Relationship(
        back_populates="wafer", sa_relationship_kwargs={"cascade": "all, delete"}
    )
    """Wafer-level analyses associated with this wafer."""


class Die(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("x", "y", "wafer_id", name="unique_wafer_die"),)
    id: Optional[int] = Field(default=None, primary_key=True)
    x: int = Field(index=True)
    y: int = Field(index=True)
    attributes: dict = Field(sa_column=Column(JSON_VARIANT), default={})  # type: ignore[type-arg]
    wafer_id: int = Field(foreign_key="wafer.id")
    wafer: Wafer = Relationship(back_populates="dies")
    timestamp: datetime = Field(default_factory=_now, index=True)
    device_data: list["DeviceData"] = Relationship(
        back_populates="die", sa_relationship_kwargs={"cascade": "all, delete"}
    )
    analysis: list["Analysis"] = Relationship(
        back_populates="die", sa_relationship_kwargs={"cascade": "all, delete"}
    )


class DeviceDataType(StrEnum):
    simulation = "simulation"
    measurement = "measurement"


class DeviceData(SQLModel, table=True):
    __tablename__ = "device_data"
    id: Optional[int] = Field(default=None, primary_key=True)
    data_type: DeviceDataType = Field(index=True)
    path: str
    thumbnail_path: Optional[str] = Field(default=None)
    attributes: dict = Field(sa_column=Column(JSON_VARIANT), default={})  # type: ignore[type-arg]
    plotting_kwargs: dict = Field(sa_column=Column(JSON_VARIANT), default=None)  # type:ignore[type-arg]
    is_bad: bool = Field(default=False, index=True)
    device: Device = Relationship(back_populates="device_data")
    device_id: int = Field(foreign_key="device.id", nullable=True)
    die_id: Optional[int] = Field(foreign_key="die.id", nullable=True)
    die: Optional[Die] = Relationship(back_populates="device_data")
    timestamp: datetime = Field(default_factory=_now, index=True)
    analysis: list["Analysis"] = Relationship(
        back_populates="device_data", sa_relationship_kwargs={"cascade": "all, delete"}
    )


class AnalysisFunctionTargetModel(StrEnum):
    device_data = "device_data"
    die = "die"
    wafer = "wafer"


class AnalysisFunction(SQLModel, table=True):
    __tablename__ = "analysis_function"
    __table_args__ = (
        UniqueConstraint(
            "name", "version", name="unique_analysis_function_name_version"
        ),
    )
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=_now, index=True)
    name: str = Field(index=True)
    version: int = Field(index=True)
    hash: str = Field(index=True)
    function_path: str
    target_model: AnalysisFunctionTargetModel
    test_target_model_id: int
    analysis: list["Analysis"] = Relationship(
        back_populates="analysis_function",
        sa_relationship_kwargs={"cascade": "all, delete"},
    )


class Analysis(SQLModel, table=True):
    __table_args__ = (
        CheckConstraint(
            "1 = (CASE WHEN device_data_id IS NOT NULL THEN 1 ELSE 0 END + \
                              CASE WHEN die_id IS NOT NULL THEN 1 ELSE 0 END + \
                              CASE WHEN wafer_id IS NOT NULL THEN 1 ELSE 0 END)",
            name="analysis_ids_xor_constraint",
        ),
    )
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=_now, index=True)
    parameters: dict = Field(sa_column=Column(JSON_VARIANT))
    output: dict = Field(sa_column=Column(JSON_VARIANT))
    summary_plot: str
    attributes: dict = Field(sa_column=Column(JSON_VARIANT), default={})
    is_bad: bool = Field(default=False, index=True)
    is_latest: bool = Field(default=True, index=True)
    input_hash: str
    device_data_id: Optional[int] = Field(foreign_key="device_data.id", nullable=True)
    device_data: Optional[DeviceData] = Relationship(back_populates="analysis")
    die_id: Optional[int] = Field(foreign_key="die.id", nullable=True)
    die: Optional[Die] = Relationship(back_populates="analysis")
    wafer_id: Optional[int] = Field(foreign_key="wafer.id", nullable=True)
    wafer: Optional[Wafer] = Relationship(back_populates="analysis")
    analysis_function_id: int = Field(foreign_key="analysis_function.id")
    analysis_function: AnalysisFunction = Relationship(
        back_populates="analysis", sa_relationship_kwargs=dict(lazy="joined")
    )

    @property
    def name(self) -> str:  # noqa
        mapping = {
            "Device Data": self.device_data_id,
            "Die": self.die_id,
            "Wafer": self.wafer_id,
        }
        model_id = f"{[ str(k) + ' #' + str(v) for k,v in mapping.items() if v][0] }"
        return f"{self.function_name} on {model_id}"
