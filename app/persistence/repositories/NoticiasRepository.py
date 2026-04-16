from sqlalchemy.orm import Session
from app.application.interfaces.repository.INoticiaRepository import INoticiaRepository
from app.persistence.models.noticia import Noticia as NoticiaModel
from app.domain.entities import Noticia
from datetime import date

class NoticiasRepository(INoticiaRepository):

    def __init__(self, db: Session):
        self.db = db

    def agregarNoticia(self, noticia: Noticia) -> Noticia:
        dbNoticia = NoticiaModel(
            titulo = noticia.titulo,
            descripcion = noticia.descripcion,
            estado = noticia.estado,
            fechaPublicacion = noticia.fechaPublicacion,
            horaPublicacion = noticia.horaPublicacion)
        
        self.db.add(dbNoticia)
        self.db.commit()
        self.db.refresh(dbNoticia)

        noticia.idNoticia = dbNoticia.idNoticia
        return noticia
    
    def obtenerNoticias(self) -> list[Noticia]:
        noticias = self.db.query(NoticiaModel).filter(NoticiaModel.estado == 1).all()

        if not noticias:
         return []
    
        return [Noticia(
            idNoticia=noticia.idNoticia,
            titulo=noticia.titulo,
            descripcion=noticia.descripcion,
            estado=noticia.estado,
            fechaPublicacion=noticia.fechaPublicacion,
            horaPublicacion=noticia.horaPublicacion
        ) for noticia in noticias]
        

    def detalleNoticia(self, idNoticia: int) -> Noticia:
        noticia = self.db.query(NoticiaModel).filter(NoticiaModel.idNoticia == idNoticia).first()

        if not noticia:
            return None

        return Noticia(
            idNoticia=noticia.idNoticia,
            titulo=noticia.titulo,
            descripcion=noticia.descripcion,
            estado=noticia.estado,
            fechaPublicacion=noticia.fechaPublicacion,
            horaPublicacion=noticia.horaPublicacion
        )
    
    def modificarNoticia(self, noticia: Noticia) -> Noticia:
        dbNoticia = self.db.query(NoticiaModel).filter(NoticiaModel.idNoticia == noticia.idNoticia).first()

        if not dbNoticia:
            return None

        dbNoticia.titulo = noticia.titulo
        dbNoticia.descripcion = noticia.descripcion
        dbNoticia.fechaPublicacion = noticia.fechaPublicacion
        dbNoticia.horaPublicacion = noticia.horaPublicacion

        self.db.commit()
        self.db.refresh(dbNoticia)

        return Noticia(
            idNoticia=dbNoticia.idNoticia,
            titulo=dbNoticia.titulo,
            descripcion=dbNoticia.descripcion,
            estado=dbNoticia.estado,
            fechaPublicacion=dbNoticia.fechaPublicacion,
            horaPublicacion=dbNoticia.horaPublicacion
        )
    
    def eliminarNoticia(self, idNoticia: int) -> bool:
        dbNoticia = self.db.query(NoticiaModel).filter(NoticiaModel.idNoticia == idNoticia).first()

        if not dbNoticia:
            return False

        dbNoticia.estado = 0

        self.db.add(dbNoticia)
        self.db.commit()
        self.db.refresh(dbNoticia)

        return True
    
    def buscarPorFecha (self, fecha: date) -> list[Noticia]:
        noticias = self.db.query(NoticiaModel).filter(NoticiaModel.fechaPublicacion == fecha, NoticiaModel.estado == 1).all()

        if not noticias:
            return []
        
        return [Noticia(
            idNoticia=noticia.idNoticia,
            titulo=noticia.titulo,
            descripcion=noticia.descripcion,
            estado=noticia.estado,
            fechaPublicacion=noticia.fechaPublicacion,
            horaPublicacion=noticia.horaPublicacion
        ) for noticia in noticias]

