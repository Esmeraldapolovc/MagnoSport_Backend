from app.application.interfaces.repository.IUsuarioRepository import IUsuarioRepository
from app.domain.entities import Usuario, Alumno
from app.persistence.models.usuario import Usuario as UsuarioModel
from app.persistence.models.alumno import Alumno as AlumnoModel
from sqlalchemy.orm import Session
from typing import Optional, List

 
class UsuarioRepository(IUsuarioRepository):

    def __init__(self, db: Session):
        self.db = db
    
    ############
    def CrearUsuario(self, usuario: Usuario) -> Usuario:
        db_usuario = UsuarioModel(
            nombre=usuario.nombre,
            correo=usuario.correo,
            foto=usuario.foto,
            contrasenia=usuario.contrasenia,
            rolId=usuario.rol.idRol
        )

        self.db.add(db_usuario)
        self.db.commit()
        self.db.refresh(db_usuario)

        usuario.idUsuario = db_usuario.idUsuario
        usuario.estatus = db_usuario.estatus

        return usuario
    ###########
    def buscarPorCorreo(self, correo: str) -> bool:
        return self.db.query(UsuarioModel).filter(UsuarioModel.correo == correo).count() > 0
    ########## 
    def login(self,  correo: str) -> UsuarioModel:
        return self.db.query(UsuarioModel).filter(UsuarioModel.correo == correo, UsuarioModel.estatus == 1).first()
    ###########
    def crearAlumno(self, alumno: Alumno) -> Alumno:
        dbUsuario = UsuarioModel(
            nombre = alumno.nombre,
            correo = alumno.correo,
            foto   = alumno.foto,
            contrasenia = alumno.contrasenia,
            rolId = alumno.rol.idRol
        )

        self.db.add(dbUsuario)
        self.db.flush()

        id_lic_db = alumno.licenciatura.idLicenciatura if alumno.licenciatura else None
       
        dbAlumno = AlumnoModel(
            idUsuario  = dbUsuario.idUsuario,
            fechaInicio = alumno.fechaInicio,
            nivelId = alumno.nivel.idNivel,
            licenciaturaId = id_lic_db,
            fechaFin = alumno.fechaFin
            
        )

        self.db.add(dbAlumno)
        self.db.commit()
        self.db.refresh(dbUsuario)

        alumno.idUsuario = dbUsuario.idUsuario
        alumno.estatus = dbUsuario.estatus

        return alumno
    #############
    def obtenerUsuarioPorId(self, idUsuario: int) -> Usuario:
        dbUsuario = self.db.query(UsuarioModel).filter(UsuarioModel.idUsuario == idUsuario).first()

        if not dbUsuario:
            return None

        return Usuario(
            idUsuario=dbUsuario.idUsuario,
            nombre=dbUsuario.nombre,
            correo = dbUsuario.correo,
            foto=dbUsuario.foto,
            contrasenia=dbUsuario.contrasenia,
            rol=dbUsuario.rolId
        )  
    
    def obtenerAlumnoPorId(self, idUsuario: int) -> Optional[Alumno]:

        result = (
            self.db.query(UsuarioModel, AlumnoModel)
            .join(AlumnoModel, UsuarioModel.idUsuario == AlumnoModel.idUsuario)
            .filter(UsuarioModel.idUsuario == idUsuario)
            .first()
        )

        if not result:
            return None

        dbUsuario, dbAlumno = result

        return Alumno(
            idUsuario=dbUsuario.idUsuario,
            nombre=dbUsuario.nombre,
            correo=dbUsuario.correo,
            foto=dbUsuario.foto,
            contrasenia=dbUsuario.contrasenia,
            rol=dbUsuario.rolId,         
            fechaInicio=dbAlumno.fechaInicio,
            fechaFin=dbAlumno.fechaFin,
            nivel=dbAlumno.nivelId,      
            licenciatura=dbAlumno.licenciaturaId, 
            estatus=dbUsuario.estatus
        )
        
       
    
    def actualizarUsuario(self, usuario: Usuario) -> Usuario:
        dbUsuario = self.db.query(UsuarioModel).filter(UsuarioModel.idUsuario == usuario.idUsuario).first()
        
        if not dbUsuario:
            raise ValueError("El suario no existe")
        
        dbUsuario.nombre = usuario.nombre
        dbUsuario.correo = usuario.correo
        dbUsuario.foto = usuario.foto
        dbUsuario.rolId = usuario.rol.idRol

        if usuario.contrasenia:
            dbUsuario.contrasenia = usuario.contrasenia


        self.db.commit()
        self.db.refresh(dbUsuario)

        return usuario
    
    
    def actualizarAlumno(self, alumno: Alumno) -> Alumno:
        dbUsuario = self.db.query(UsuarioModel).filter(UsuarioModel.idUsuario == alumno.idUsuario).first()
        dbAlumno = self.db.query(AlumnoModel).filter(AlumnoModel.idUsuario == alumno.idUsuario).first()

        if not dbUsuario or not dbAlumno:
            raise ValueError("El alumno o el registro de usuario no existe")

        dbUsuario.nombre = alumno.nombre
        dbUsuario.correo = alumno.correo
        dbUsuario.foto = alumno.foto  
        dbUsuario.rolId = alumno.rol.idRol
        
        if alumno.contrasenia:
            dbUsuario.contrasenia = alumno.contrasenia

        dbAlumno.fechaInicio = alumno.fechaInicio
        dbAlumno.fechaFin = alumno.fechaFin
        dbAlumno.nivelId = alumno.nivel.idNivel
        
        if alumno.licenciatura:
            dbAlumno.licenciaturaId = alumno.licenciatura.idLicenciatura
        else:
            dbAlumno.licenciaturaId = None 
        self.db.add(dbUsuario)
        self.db.add(dbAlumno)
        self.db.commit()
        
        self.db.refresh(dbUsuario)
        self.db.refresh(dbAlumno)

        return alumno
    

    def actualizarUsuarioAdmin(self, usuario: Usuario) -> Usuario:
        dbUsuario = self.db.query(UsuarioModel).filter(UsuarioModel.idUsuario == usuario.idUsuario).first()
        
        if not dbUsuario:
            raise ValueError("El suario no existe")
        
        dbUsuario.nombre = usuario.nombre
        dbUsuario.correo = usuario.correo
        dbUsuario.foto = usuario.foto
        dbUsuario.rolId = usuario.rol.idRol
        if usuario.contrasenia:
            dbUsuario.contrasenia = usuario.contrasenia


        self.db.commit()
        self.db.refresh(dbUsuario)

        return usuario
    
    def actualizarAlumnoAdmin(self, alumno: Alumno)->Alumno:
        dbUsuario = self.db.query(UsuarioModel).filter(UsuarioModel.idUsuario == alumno.idUsuario).first()
        dbAlumno = self.db.query(AlumnoModel).filter(AlumnoModel.idUsuario == alumno.idUsuario).first()

        if not dbUsuario or not dbAlumno:
            raise ValueError("El alumno o el registro de usuario no existe")

        # Actualización de Usuario
        dbUsuario.nombre = alumno.nombre
        dbUsuario.correo = alumno.correo
        dbUsuario.foto = alumno.foto  
        dbUsuario.rolId = alumno.rol.idRol
        if alumno.contrasenia:
            dbUsuario.contrasenia = alumno.contrasenia

        # Actualización de Alumno
        dbAlumno.fechaInicio = alumno.fechaInicio
        dbAlumno.fechaFin = alumno.fechaFin
        dbAlumno.nivelId = alumno.nivel.idNivel
        
        # IMPORTANTE: Aseguramos la asignación del ID de licenciatura
        if alumno.licenciatura:
            dbAlumno.licenciaturaId = alumno.licenciatura.idLicenciatura
        else:
            dbAlumno.licenciaturaId = None # Si cambió a un nivel que no requiere lic

        self.db.add(dbUsuario)
        self.db.add(dbAlumno)
        self.db.commit() # Guarda ambos cambios
        
        self.db.refresh(dbUsuario)
        self.db.refresh(dbAlumno)

        return alumno
    
    def eliminarUsuario(self, idUsuario: int) -> bool:
        dbUsuario = self.db.query(UsuarioModel).filter(UsuarioModel.idUsuario == idUsuario).first()
        
        if not dbUsuario:
            return None

        dbUsuario.estatus = 0

        self.db.add(dbUsuario)
        self.db.commit()

        self.db.refresh(dbUsuario)

        return True
    
    def activarUsuario(self, idUsuario: int) -> bool:
        dbUsuario = self.db.query(UsuarioModel).filter(UsuarioModel.idUsuario == idUsuario).first()
        
        if not dbUsuario:
            return None

        dbUsuario.estatus = 1

        self.db.add(dbUsuario)
        self.db.commit()

        self.db.refresh(dbUsuario)

        return True
    ##################
    def listarUsuarios(self) -> List[Usuario]:
       usuarios_db = self.db.query(UsuarioModel).filter(UsuarioModel.estatus == 1, UsuarioModel.rolId.in_([3, 4])).all()

       return [
           Usuario(
            idUsuario=u.idUsuario,
            nombre=u.nombre,
            correo=u.correo,
            foto=u.foto,
            contrasenia=u.contrasenia,
            rol=u.rolId, 
            estatus=u.estatus
          ) for u in usuarios_db
    ]


    def listarAlumno(self) -> List[Alumno]:
        result = (
            self.db.query(UsuarioModel, AlumnoModel)
            .outerjoin(AlumnoModel, UsuarioModel.idUsuario == AlumnoModel.idUsuario)          
            .filter(UsuarioModel.estatus ==1, UsuarioModel.rolId == 2)
            .all()
        )


        lista_alumnos = []
        for dbUsuario, dbAlumno in result:
            alumno_entidad = Alumno(
               idUsuario=dbUsuario.idUsuario,
               nombre=dbUsuario.nombre,
               correo=dbUsuario.correo,
               foto=dbUsuario.foto,
               contrasenia=dbUsuario.contrasenia,
               rol=dbUsuario.rolId,
               fechaInicio=dbAlumno.fechaInicio if dbAlumno else None,
               fechaFin=dbAlumno.fechaFin if dbAlumno else None,
               nivel=dbAlumno.nivelId if dbAlumno else None,
               licenciatura=dbAlumno.licenciaturaId if dbAlumno else None,
              estatus=dbUsuario.estatus
        )
            lista_alumnos.append(alumno_entidad)

        return lista_alumnos
    
    def filtradoAlumno(self, nombre: Optional[str] = None, correo: Optional[str] = None, 
                   nivelId: Optional[int] = None, licenciaturaId: Optional[int] = None, 
                   estado: Optional[int] = None) -> List[Alumno]:
    
     query = self.db.query(UsuarioModel, AlumnoModel).join(
        AlumnoModel, UsuarioModel.idUsuario == AlumnoModel.idUsuario ).filter(UsuarioModel.rolId == 2)

     if nombre:
        query = query.filter(UsuarioModel.nombre.ilike(f"%{nombre}%"))

     if correo:
        query = query.filter(UsuarioModel.correo.ilike(f"%{correo}%"))

     if nivelId:
        query = query.filter(AlumnoModel.nivelId == nivelId)
    
    
     if nivelId == 2 and licenciaturaId:
       query = query.filter(AlumnoModel.licenciaturaId == licenciaturaId)

     if estado is not None: 
        query = query.filter(UsuarioModel.estatus == estado)
     else:
        query = query.filter(UsuarioModel.estatus == 1)

     result = query.all()

     lista_alumnos = []
     for dbUsuario, dbAlumno in result:
        lista_alumnos.append(Alumno(
            idUsuario=dbUsuario.idUsuario,
            nombre=dbUsuario.nombre,
            correo=dbUsuario.correo,
            foto=dbUsuario.foto,
            contrasenia=dbUsuario.contrasenia,
            rol=dbUsuario.rolId,
            fechaInicio=dbAlumno.fechaInicio,
            fechaFin=dbAlumno.fechaFin,
            nivel=dbAlumno.nivelId,
            licenciatura=dbAlumno.licenciaturaId,
            estatus=dbUsuario.estatus
        ))
     return lista_alumnos
 
    def filtradoUsuario(self, nombre: Optional[str] = None, correo: Optional[str] = None, rol: Optional[int] = None,
                        estado: Optional[int] = None) -> List[Usuario]:
          query = self.db.query(UsuarioModel).filter(  UsuarioModel.rolId.in_([3, 4]))

          query = query.filter(UsuarioModel.rolId.in_([3, 4]))

          if nombre:
                query = query.filter(UsuarioModel.nombre.ilike(f"%{nombre}%"))

          if correo:
               query = query.filter(UsuarioModel.correo.ilike(f"%{correo}%"))
    
          if rol:
              query = query.filter(UsuarioModel.rolId == rol)

          if estado is not None: 
            query = query.filter(UsuarioModel.estatus == estado)
          else:
            query = query.filter(UsuarioModel.estatus == 1)

          usuarios_db = query.all()

          return [
            Usuario(
            idUsuario=u.idUsuario,
            nombre=u.nombre,
            correo=u.correo,
            foto=u.foto,
            contrasenia=u.contrasenia,
            rol=u.rolId, 
            estatus=u.estatus
        ) for u in usuarios_db
        ]
    def crearAlumno1(self, alumno: Alumno) -> Alumno:
        dbUsuario = self.db.query(UsuarioModel).filter(UsuarioModel.idUsuario == alumno.idUsuario).first()

        id_lic_db = alumno.licenciatura.idLicenciatura if alumno.licenciatura else None
       
        dbAlumno = AlumnoModel(
            idUsuario  = dbUsuario.idUsuario,
            fechaInicio = alumno.fechaInicio,
            nivelId = alumno.nivel.idNivel,
            licenciaturaId = id_lic_db,
            fechaFin = alumno.fechaFin
            
        )

        self.db.add(dbAlumno)
        self.db.commit()
        self.db.refresh(dbUsuario)

        alumno.idUsuario = dbUsuario.idUsuario
        alumno.estatus = dbUsuario.estatus

        return alumno