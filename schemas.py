from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
)

# USUARIO

class UsuarioCreate(BaseModel):
    uid: str = Field(
        ...,
        min_length=1,
        max_length=128,
        description="Identificador único del usuario",
    )

    nombre: str = Field(
        ...,
        min_length=2,
        max_length=150,
    )

    nombre_usuario: str = Field(
        ...,
        min_length=3,
        max_length=50,
    )

    email: EmailStr

    edad: int | None = Field(
        default=None,
        ge=1,
        le=120,
    )

    ciudad: str | None = Field(
        default=None,
        max_length=100,
    )

    genero: str | None = Field(
        default=None,
        max_length=10,
    )


class UsuarioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uid: str
    nombre: str
    nombre_usuario: str
    email: str
    edad: int | None = None
    ciudad: str | None = None
    genero: str | None = None
    estrellas: int
    monedas: int
    fecha_registro: datetime

# DIARIO

class DiarioCreate(BaseModel):
    uid: str = Field(
        ...,
        min_length=1,
        max_length=128,
    )

    nota: str | None = Field(
        default=None,
        max_length=500,
    )

    estado: str | None = Field(
        default=None,
        max_length=10,
    )

    temperatura: str | None = Field(
        default=None,
        max_length=20,
    )

    tipo_residuo: str | None = Field(
        default=None,
        max_length=20,
    )

    composta_punos: int | None = Field(
        default=None,
        ge=0,
    )

    lixiviado_cucharadas: int | None = Field(
        default=None,
        ge=0,
    )

    fotos: list[str] = Field(
        default_factory=list,
    )


class DiarioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    uid: str
    fecha: datetime
    nota: str | None = None
    estado: str | None = None
    temperatura: str | None = None
    tipo_residuo: str | None = None
    composta_punos: int | None = None
    lixiviado_cucharadas: int | None = None
    fotos: list[str] = Field(default_factory=list)

# VENTA

class VentaCreate(BaseModel):
    uid: str = Field(
        ...,
        min_length=1,
        max_length=128,
    )

    producto: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )

    cantidad: int = Field(
        ...,
        gt=0,
    )

    precio_unitario: float = Field(
        ...,
        ge=0,
    )

    total_ganado: int = Field(
        ...,
        ge=0,
    )

    descripcion: str | None = Field(
        default=None,
        max_length=255,
    )


class VentaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    uid: str
    producto: str
    cantidad: int
    precio_unitario: float
    total_ganado: int
    fecha: datetime
    descripcion: str | None = None

# RETO

class RetoCreate(BaseModel):
    uid: str = Field(
        ...,
        min_length=1,
        max_length=128,
    )

    reto_id: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )

    completado: bool = False

    medicion: int | None = Field(
        default=None,
        ge=0,
    )

    foto_url: str | None = Field(
        default=None,
        max_length=500,
    )


class RetoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    uid: str
    reto_id: str
    completado: bool
    fecha_completado: datetime | None = None
    medicion: int | None = None
    foto_url: str | None = None

# LOGRO

class LogroCreate(BaseModel):
    uid: str = Field(
        ...,
        min_length=1,
        max_length=128,
    )

    tipo: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )

    nombre: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    descripcion: str | None = Field(
        default=None,
        max_length=255,
    )


class LogroOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    uid: str
    tipo: str
    nombre: str
    descripcion: str | None = None
    fecha_desbloqueo: datetime

# RECORDATORIO

class RecordatorioCreate(BaseModel):
    uid: str = Field(
        ...,
        min_length=1,
        max_length=128,
    )

    titulo: str = Field(
        ...,
        min_length=1,
        max_length=150,
    )

    mensaje: str | None = Field(
        default=None,
        max_length=500,
    )


class RecordatorioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    uid: str
    titulo: str
    mensaje: str | None = None
    fecha: datetime
    visto: bool

# CAPACITACION

class CapacitacionCreate(BaseModel):
    uid: str = Field(
        ...,
        min_length=1,
        max_length=128,
    )

    nombre_capacitado: str = Field(
        ...,
        min_length=2,
        max_length=150,
    )

    edad_capacitado: int | None = Field(
        default=None,
        ge=1,
        le=120,
    )

    municipio: str | None = Field(
        default=None,
        max_length=100,
    )

    estado: str | None = Field(
        default=None,
        max_length=100,
    )

    pais: str | None = Field(
        default=None,
        max_length=100,
    )

    invitado_por: str | None = Field(
        default=None,
        max_length=150,
    )

class CapacitacionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    uid: str
    nombre_capacitado: str
    edad_capacitado: int | None = None
    municipio: str | None = None
    estado: str | None = None
    pais: str | None = None
    invitado_por: str | None = None
    fecha: datetime
    monedas_ganadas: int