from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

# ---------- Usuario ----------

class UsuarioCreate(BaseModel):
    nombre: str
    nombre_usuario: str
    email: EmailStr
    edad: Optional[int] = None
    ciudad: str | None
    genero: str | None  # 'Lola' o 'Lalo'


class UsuarioOut(BaseModel):
    uid: str
    nombre: str
    nombre_usuario: str
    email: str
    edad: Optional[int]
    ciudad: str | None
    genero: str | None
    estrellas: int
    monedas: int
    fecha_registro: datetime

    class Config:
        from_attributes = True  


# ---------- Diario ----------

class DiarioCreate(BaseModel):
    uid: str
    nota: str | None
    estado: str | None
    temperatura: str | None
    tipo_residuo: str | None
    composta_punos: Optional[int] = None
    lixiviado_cucharadas: Optional[int] = None


class DiarioOut(BaseModel):
    id: int
    uid: str
    fecha: datetime
    nota: str | None
    estado: str | None
    temperatura: str | None
    tipo_residuo: str | None

    class Config:
        from_attributes = True


# ---------- Venta ----------

class VentaCreate(BaseModel):
    uid: str
    producto: str
    cantidad: int
    precio_unitario: float
    total_ganado: int
    descripcion: str | None


class VentaOut(BaseModel):
    id: int
    uid: str
    producto: str
    cantidad: int
    precio_unitario: float
    total_ganado: int
    fecha: datetime

    class Config:
        from_attributes = True

#---------- Reto ----------

class RetoCreate(BaseModel):
    uid: str
    reto_id: str
    completado: bool = False
    medicion: Optional[int] = None
    foto_url: str | None
    
class RetoOut(BaseModel):
    id: int
    uid: str
    reto_id: str
    completado: bool
    fecha_completado: Optional[datetime]
    medicion: Optional[int]
    foto_url: str | None
    
    class Config: 
        from_attributes = True
        
#---------- Logro ----------

class LogroCreate(BaseModel):
    id: int
    uid: str
    tipo: str
    nombre: str
    descripcion: str | None
    
class LogroOut(BaseModel):
    id: int
    uid: str
    tipo: str
    nombre: str
    descripcion: str | None
    fecha_desbloqueo: datetime
    
    class Config:
        from_attributes = True
        
#---------- Recordatorio ----------

class RecordatorioCreate(BaseModel):
    uid: str
    titulo: str
    mensaje: str | None
    
class RecordatorioOut(BaseModel):
    id: int
    uid: str
    titulo: str
    mensaje: str | None
    fecha: datetime
    visto: bool
    
    class Config:
        from_attributes = True
        
#------------ Capacitacion --------

class CapacitacionCreate(BaseModel):
    uid: str
    nombre_capacitado: str
    edad_capacitado: Optional[int] = None
    municipio: str | None
    estado: str | None
    pais: str | None
    invitado_por: str | None
    monedas_ganadas: int = 50
    
class CapacitacionOut(BaseModel):
    id: int
    uid: str
    nombre_capacitado: str
    edad_capacitado: Optional[int]
    municipio: str | None
    estado: str | None
    pais: str | None
    invitado_por: str | None
    fecha: datetime
    monedas_ganadas: int
    
    class Config:
        from_attributes = True