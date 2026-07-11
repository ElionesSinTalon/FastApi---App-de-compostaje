import uuid

from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import IntegrityError

from database import SessionLocal, engine, Base
import models
from schemas import (
    UsuarioCreate, UsuarioOut,
    DiarioCreate, DiarioOut,
    VentaCreate, VentaOut,
    RetoCreate, RetoOut,
    LogroCreate, LogroOut,
    RecordatorioCreate, RecordatorioOut,
    CapacitacionCreate, CapacitacionOut,
)

app = FastAPI(title="API - App de Compostaje", version="1.0")

# Crea las tablas automáticamente al levantar el servidor (si no existen).
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"status": "ok", "mensaje": "API de compostaje corriendo correctamente"}


# ---------- USUARIOS ----------

@app.post("/usuarios", response_model=UsuarioOut, status_code=201)
def crear_usuario(usuario: UsuarioCreate):
    db = SessionLocal()
    try:
        nuevo = models.Usuario(
            **usuario.model_dump()
        )
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        return nuevo
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="email o nombre_usuario ya existe")
    finally:
        db.close()


@app.get("/usuarios", response_model=list[UsuarioOut])
def listar_usuarios():
    db = SessionLocal()
    try:
        return db.query(models.Usuario).all()
    finally:
        db.close()


@app.get("/usuarios/{uid}", response_model=UsuarioOut)
def obtener_usuario(uid: str):
    db = SessionLocal()
    try:
        usuario = db.get(models.Usuario, uid)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return usuario
    finally:
        db.close()


@app.delete("/usuarios/{uid}", status_code=204)
def eliminar_usuario(uid: str):
    """Borra el usuario y, por la cascada configurada en los modelos,
    también borra automáticamente su diario, ventas, retos, etc."""
    db = SessionLocal()
    try:
        usuario = db.get(models.Usuario, uid)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        db.delete(usuario)
        db.commit()
    finally:
        db.close()


# ---------- DIARIO ----------

@app.post("/diario", response_model=DiarioOut, status_code=201)
def crear_entrada_diario(entrada: DiarioCreate):
    db = SessionLocal()
    try:
        if not db.get(models.Usuario, entrada.uid):
            raise HTTPException(status_code=404, detail="uid de usuario no existe")
        nueva = models.Diario(**entrada.model_dump())
        db.add(nueva)
        db.commit()
        db.refresh(nueva)
        return nueva
    finally:
        db.close()


@app.get("/usuarios/{uid}/diario", response_model=list[DiarioOut])
def listar_diario_de_usuario(uid: str):
    db = SessionLocal()
    try:
        return db.query(models.Diario).filter(models.Diario.uid == uid).all()
    finally:
        db.close()


# ---------- VENTAS ----------

@app.post("/ventas", response_model=VentaOut, status_code=201)
def crear_venta(venta: VentaCreate):
    db = SessionLocal()
    try:
        if not db.get(models.Usuario, venta.uid):
            raise HTTPException(status_code=404, detail="uid de usuario no existe")
        nueva = models.Venta(**venta.model_dump())
        db.add(nueva)
        db.commit()
        db.refresh(nueva)
        return nueva
    finally:
        db.close()


@app.get("/usuarios/{uid}/ventas", response_model=list[VentaOut])
def listar_ventas_de_usuario(uid: str):
    db = SessionLocal()
    try:
        return db.query(models.Venta).filter(models.Venta.uid == uid).all()
    finally:
        db.close()


# ---------- RETOS ----------

@app.post("/retos", response_model=RetoOut, status_code=201)
def crear_reto(reto: RetoCreate):
    db = SessionLocal()
    try:
        if not db.get(models.Usuario, reto.uid):
            raise HTTPException(status_code=404, detail="uid de usuario no existe")
        datos = reto.model_dump()
        # Si el reto viene como completado desde el inicio, registramos la fecha
        if datos.get("completado"):
            from datetime import datetime
            datos["fecha_completado"] = datetime.utcnow()
        nuevo = models.Reto(**datos)
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        return nuevo
    finally:
        db.close()


@app.get("/usuarios/{uid}/retos", response_model=list[RetoOut])
def listar_retos_de_usuario(uid: str):
    db = SessionLocal()
    try:
        return db.query(models.Reto).filter(models.Reto.uid == uid).all()
    finally:
        db.close()


@app.patch("/retos/{reto_id}/completar", response_model=RetoOut)
def completar_reto(reto_id: int):
    """Marca un reto como completado y registra la fecha automáticamente."""
    from datetime import datetime
    db = SessionLocal()
    try:
        reto = db.get(models.Reto, reto_id)
        if not reto:
            raise HTTPException(status_code=404, detail="Reto no encontrado")
        if reto.completado:
            raise HTTPException(status_code=400, detail="El reto ya estaba completado")
        reto.completado = True
        reto.fecha_completado = datetime.utcnow()
        db.commit()
        db.refresh(reto)
        return reto
    finally:
        db.close()

# ---------- LOGROS ----------

@app.post("/logros", response_model=LogroOut, status_code=201)
def crear_logro(logro: LogroCreate):
    db = SessionLocal()
    try:
        if not db.get(models.Usuario, logro.uid):
            raise HTTPException(status_code=404, detail="uid de usuario no existe")
        nuevo = models.Logro(**logro.model_dump())
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        return nuevo
    finally:
        db.close()


@app.get("/usuarios/{uid}/logros", response_model=list[LogroOut])
def listar_logros_de_usuario(uid: str):
    db = SessionLocal()
    try:
        return db.query(models.Logro).filter(models.Logro.uid == uid).all()
    finally:
        db.close()


@app.delete("/logros/{logro_id}", status_code=204)
def eliminar_logro(logro_id: int):
    db = SessionLocal()
    try:
        logro = db.get(models.Logro, logro_id)
        if not logro:
            raise HTTPException(status_code=404, detail="Logro no encontrado")
        db.delete(logro)
        db.commit()
    finally:
        db.close()


# ---------- RECORDATORIOS ----------

@app.post("/recordatorios", response_model=RecordatorioOut, status_code=201)
def crear_recordatorio(recordatorio: RecordatorioCreate):
    db = SessionLocal()
    try:
        if not db.get(models.Usuario, recordatorio.uid):
            raise HTTPException(status_code=404, detail="uid de usuario no existe")
        nuevo = models.Recordatorio(**recordatorio.model_dump())
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        return nuevo
    finally:
        db.close()


@app.get("/usuarios/{uid}/recordatorios", response_model=list[RecordatorioOut])
def listar_recordatorios_de_usuario(uid: str):
    db = SessionLocal()
    try:
        return db.query(models.Recordatorio).filter(models.Recordatorio.uid == uid).all()
    finally:
        db.close()


@app.patch("/recordatorios/{recordatorio_id}/marcar-visto", response_model=RecordatorioOut)
def marcar_recordatorio_visto(recordatorio_id: int):
    """Marca un recordatorio como visto."""
    db = SessionLocal()
    try:
        recordatorio = db.get(models.Recordatorio, recordatorio_id)
        if not recordatorio:
            raise HTTPException(status_code=404, detail="Recordatorio no encontrado")
        recordatorio.visto = True
        db.commit()
        db.refresh(recordatorio)
        return recordatorio
    finally:
        db.close()


@app.delete("/recordatorios/{recordatorio_id}", status_code=204)
def eliminar_recordatorio(recordatorio_id: int):
    db = SessionLocal()
    try:
        recordatorio = db.get(models.Recordatorio, recordatorio_id)
        if not recordatorio:
            raise HTTPException(status_code=404, detail="Recordatorio no encontrado")
        db.delete(recordatorio)
        db.commit()
    finally:
        db.close()


# ---------- CAPACITACIONES ----------

@app.post("/capacitaciones", response_model=CapacitacionOut, status_code=201)
def crear_capacitacion(capacitacion: CapacitacionCreate):
    db = SessionLocal()
    try:
        if not db.get(models.Usuario, capacitacion.uid):
            raise HTTPException(status_code=404, detail="uid de usuario no existe")
        nueva = models.Capacitacion(**capacitacion.model_dump())
        db.add(nueva)
        db.commit()
        db.refresh(nueva)
        return nueva
    finally:
        db.close()


@app.get("/usuarios/{uid}/capacitaciones", response_model=list[CapacitacionOut])
def listar_capacitaciones_de_usuario(uid: str):
    db = SessionLocal()
    try:
        return db.query(models.Capacitacion).filter(models.Capacitacion.uid == uid).all()
    finally:
        db.close()


@app.delete("/capacitaciones/{capacitacion_id}", status_code=204)
def eliminar_capacitacion(capacitacion_id: int):
    db = SessionLocal()
    try:
        capacitacion = db.get(models.Capacitacion, capacitacion_id)
        if not capacitacion:
            raise HTTPException(status_code=404, detail="Capacitación no encontrada")
        db.delete(capacitacion)
        db.commit()
    finally:
        db.close()