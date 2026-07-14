"""
7 tablas:
  - usuarios       (tabla padre)
  - diario         (hija, FK -> usuarios.uid)
  - ventas         (hija, FK -> usuarios.uid)
  - retos          (hija, FK -> usuarios.uid)
  - logros         (hija, FK -> usuarios.uid)
  - recordatorios  (hija, FK -> usuarios.uid)
  - capacitaciones (hija, FK -> usuarios.uid)

Todas las tablas hijas usan ondelete="CASCADE": si se borra un usuario,
PostgreSQL borra automáticamente todos sus registros relacionados.
"""
from datetime import datetime

from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Usuario(Base):
    """Tabla padre — tabla maestra del sistema."""
    __tablename__ = "usuarios"

    # String(128) porque uid viene de un proveedor de auth tipo Firebase (UUID).
    uid: Mapped[str] = mapped_column(String(128), primary_key=True)

    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    nombre_usuario: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    edad: Mapped[int] = mapped_column(Integer, nullable=True)
    ciudad: Mapped[str] = mapped_column(String(100), nullable=True)
    genero: Mapped[str] = mapped_column(String(10), nullable=True)  # 'Lola' o 'Lalo'
    fecha_registro: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    estrellas: Mapped[int] = mapped_column(Integer, default=0)
    monedas: Mapped[int] = mapped_column(Integer, default=0)

    # Campos Map / List del documento original -> columnas JSON en PostgreSQL.
    accesorios_equipados: Mapped[dict] = mapped_column(JSON, default=dict)
    accesorios_comprados: Mapped[list] = mapped_column(JSON, default=list)

    # cascade="all, delete-orphan" replica a nivel ORM lo mismo que
    # ON DELETE CASCADE hace a nivel base de datos (ver ForeignKey en cada hija).
    diario: Mapped[list["Diario"]] = relationship(back_populates="usuario", cascade="all, delete-orphan")
    ventas: Mapped[list["Venta"]] = relationship(back_populates="usuario", cascade="all, delete-orphan")
    retos: Mapped[list["Reto"]] = relationship(back_populates="usuario", cascade="all, delete-orphan")
    logros: Mapped[list["Logro"]] = relationship(back_populates="usuario", cascade="all, delete-orphan")
    recordatorios: Mapped[list["Recordatorio"]] = relationship(back_populates="usuario", cascade="all, delete-orphan")
    capacitaciones: Mapped[list["Capacitacion"]] = relationship(back_populates="usuario", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Usuario {self.nombre_usuario}>"


class Diario(Base):
    """Entradas diarias del usuario sobre su composta."""
    __tablename__ = "diario"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uid: Mapped[str] = mapped_column(String(36), ForeignKey("usuarios.uid", ondelete="CASCADE"), nullable=False)

    fecha: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    nota: Mapped[str] = mapped_column(String(500), nullable=True)
    estado: Mapped[str] = mapped_column(String(10), nullable=True)
    temperatura: Mapped[str] = mapped_column(String(20), nullable=True)
    tipo_residuo: Mapped[str] = mapped_column(String(20), nullable=True)
    composta_punos: Mapped[int] = mapped_column(Integer, nullable=True)        # solo día 1
    lixiviado_cucharadas: Mapped[int] = mapped_column(Integer, nullable=True)  # solo día 1
    fotos: Mapped[list] = mapped_column(JSON, default=list)  # URLs (Firebase Storage / S3 / etc.)

    usuario: Mapped["Usuario"] = relationship(back_populates="diario")

    def __repr__(self) -> str:
        return f"<Diario {self.id} uid={self.uid}>"


class Venta(Base):
    """Ventas de productos derivados del compostaje (lombrices, humus, etc.)."""
    __tablename__ = "ventas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uid: Mapped[str] = mapped_column(String(36), ForeignKey("usuarios.uid", ondelete="CASCADE"), nullable=False)

    producto: Mapped[str] = mapped_column(String(50), nullable=False)  # 'lombrices', 'atomizador', 'humus'
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    precio_unitario: Mapped[float] = mapped_column(Float, nullable=False)
    total_ganado: Mapped[int] = mapped_column(Integer, nullable=False)  # monedas ganadas
    fecha: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    descripcion: Mapped[str] = mapped_column(String(255), nullable=True)

    usuario: Mapped["Usuario"] = relationship(back_populates="ventas")

    def __repr__(self) -> str:
        return f"<Venta {self.id} producto={self.producto}>"


class Reto(Base):
    """Retos/desafíos que el usuario puede completar."""
    __tablename__ = "retos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uid: Mapped[str] = mapped_column(String(36), ForeignKey("usuarios.uid", ondelete="CASCADE"), nullable=False)

    reto_id: Mapped[str] = mapped_column(String(50), nullable=False)  # 'reto_1', 'reto_humus', etc.
    completado: Mapped[bool] = mapped_column(Boolean, default=False)
    fecha_completado: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    medicion: Mapped[int] = mapped_column(Integer, nullable=True)  # puños o cucharadas
    foto_url: Mapped[str] = mapped_column(String(500), nullable=True)

    usuario: Mapped["Usuario"] = relationship(back_populates="retos")

    def __repr__(self) -> str:
        return f"<Reto {self.reto_id} uid={self.uid}>"


class Logro(Base):
    """Logros/insignias desbloqueados por el usuario."""
    __tablename__ = "logros"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uid: Mapped[str] = mapped_column(String(36), ForeignKey("usuarios.uid", ondelete="CASCADE"), nullable=False)

    tipo: Mapped[str] = mapped_column(String(50), nullable=False)  # 'clasificador', 'alimentador', etc.
    fecha_desbloqueo: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(255), nullable=True)

    usuario: Mapped["Usuario"] = relationship(back_populates="logros")

    def __repr__(self) -> str:
        return f"<Logro {self.nombre} uid={self.uid}>"


class Recordatorio(Base):
    """Recordatorios/notificaciones enviadas al usuario."""
    __tablename__ = "recordatorios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uid: Mapped[str] = mapped_column(String(36), ForeignKey("usuarios.uid", ondelete="CASCADE"), nullable=False)

    titulo: Mapped[str] = mapped_column(String(150), nullable=False)
    mensaje: Mapped[str] = mapped_column(String(500), nullable=True)
    fecha: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    visto: Mapped[bool] = mapped_column(Boolean, default=False)

    usuario: Mapped["Usuario"] = relationship(back_populates="recordatorios")

    def __repr__(self) -> str:
        return f"<Recordatorio {self.titulo} uid={self.uid}>"


class Capacitacion(Base):
    """Registro de niños capacitados por un usuario (programa de difusión)."""
    __tablename__ = "capacitaciones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uid: Mapped[str] = mapped_column(String(36), ForeignKey("usuarios.uid", ondelete="CASCADE"), nullable=False)

    nombre_capacitado: Mapped[str] = mapped_column(String(150), nullable=False)
    edad_capacitado: Mapped[int] = mapped_column(Integer, nullable=True)
    municipio: Mapped[str] = mapped_column(String(100), nullable=True)
    estado: Mapped[str] = mapped_column(String(100), nullable=True)
    pais: Mapped[str] = mapped_column(String(100), nullable=True)
    invitado_por: Mapped[str] = mapped_column(String(150), nullable=True)
    fecha: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    monedas_ganadas: Mapped[int] = mapped_column(Integer, default=50)

    usuario: Mapped["Usuario"] = relationship(back_populates="capacitaciones")

    def __repr__(self) -> str:
        return f"<Capacitacion {self.nombre_capacitado} uid={self.uid}>"
