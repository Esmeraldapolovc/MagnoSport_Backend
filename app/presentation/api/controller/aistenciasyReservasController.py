from fastapi import HTTPException
from pendulum import date
from app.application.interfaces.service.IAsistenciasyReservasService import IAsistenciasyReservasService


class AsistenciasyReservasController:
    def __init__(self, service: IAsistenciasyReservasService):
        self.service = service

    def obtenerHorariosAsistenciasyReservas(self, idArea: int):
        try:
            return self.service.obtenerHorariosAsistenciasyReservas(idArea)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        

    def obtenerHorariosAsistenciasyReservasPorFecha(self, fecha_referencia: date, idArea: int):
        try:
            return self.service.obtenerHorariosAsistenciasyReservasPorFecha(fecha_referencia, idArea)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    def obtenerdetallesusuario(self, idReserva: int):
        try:
            return self.service.detallesUsuarioReserva(idReserva)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    def registrarAsistencia(self, idReserva: int):
        try:
            return self.service.registrarAsistencia(idReserva)
        except ValueError as e:
            # Si el repository lanza "Reserva no encontrada" o validaciones de estado
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))