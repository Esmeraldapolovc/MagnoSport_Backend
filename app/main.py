from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.config import settings
from fastapi.staticfiles import StaticFiles
import os
from app.presentation.api.routers import router as  usuario_router, horario_router, reserva_router, asistenciasyreservas_router, noticia_router, equipo_router, licenciatura_router, nivel_router, asistencia_router
import uvicorn


# instancia de FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="API para la gestión de reservas de MAGNOSport"
)

# Configuracion de CORS
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "uploads")), name="static")

# rutas de las capas de presentación
app.include_router(usuario_router, prefix="/api")
app.include_router(horario_router, prefix="/api")
app.include_router(reserva_router, prefix="/api")
app.include_router(asistenciasyreservas_router, prefix="/api")
app.include_router(noticia_router, prefix="/api")
app.include_router(equipo_router, prefix="/api")
app.include_router(licenciatura_router, prefix="/api")
app.include_router(nivel_router,prefix="/api" )
app.include_router(asistencia_router, prefix="/api")
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
