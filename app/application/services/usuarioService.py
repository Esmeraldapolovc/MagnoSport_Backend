from app.domain.entities import Usuario, Alumno
from ..interfaces.service.IUsuarioService import IUsuarioService
from ..interfaces.repository.IUsuarioRepository import IUsuarioRepository
from ..dtos.usuario import UsuarioCreateDTO, UsuarioLoginDTO, UsuarioDeleteDTO, AlumnoCreateDTO,AlumnoUpdateDTO, UsuarioUpdateDTO
from app.infrastructure.security import Security
from ..interfaces.repository.IRolRepository import IRolRepository
from ..interfaces.repository.ILicenciaturaRepository import ILicenciaturaRepository
from ..interfaces.repository.INivelAcademicoRepository import INivelAcademicoRepository
import uuid
from typing import List
import os
from app.infrastructure.jwt_manager import create_access_token

class UsuarioService(IUsuarioService):

    def __init__(self, repository: IUsuarioRepository, repositoryRol: IRolRepository,  repositoryNivel: INivelAcademicoRepository, repositoryLic: ILicenciaturaRepository):
        self.repository = repository
        self.repositoryRol = repositoryRol
        self.repositoryNivel = repositoryNivel
        self.repositoryLic = repositoryLic

    # Servicio para la creación de los Usuarios  Personal y Profesor 
    def crearUsuario(self, dto: UsuarioCreateDTO, archivoFoto = None) -> str:
        entidadRol = self.repositoryRol.obtenerRol(dto.rolId)
        correovalidar = dto.correo.strip().lower()
        
        if self.repository.buscarPorCorreo(correovalidar):
            raise ValueError(f"El correo {dto.correo} ya está registrado")

        nombrefoto = "default.png"
        if archivoFoto:
            extension = os.path.splitext(archivoFoto.filename)[1]
            nombrefoto = f"{uuid.uuid4()}{extension}"
            
            basePath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            rutaCarpeta = os.path.join(basePath, "uploads", "fotos")
            if not os.path.exists(rutaCarpeta):
               os.makedirs(rutaCarpeta, exist_ok=True)

            rutaFinal = os.path.join(rutaCarpeta, nombrefoto)
            print(f"--- VERIFICANDO RUTA ---: {os.path.abspath(rutaFinal)}")

            with open(rutaFinal, "wb") as buffer:
                archivoFoto.file.seek(0)
                buffer.write(archivoFoto.file.read())

        nuevoUsuario = Usuario(
            nombre=dto.nombre,
            correo=dto.correo,
            foto=nombrefoto,
            contrasenia=dto.contrasenia,
            rol=entidadRol
        )
        nuevoUsuario.contrasenia = Security.hash_password(dto.contrasenia)
        self.repository.CrearUsuario(nuevoUsuario)
        

        return f"Los datos del {entidadRol.nombreRol.lower()} {nuevoUsuario.nombre} fueron guardados"
    
    #################
    def login(self, dto: UsuarioLoginDTO):

     usuariodb = self.repository.login(dto.correo)

     if not usuariodb:
        raise ValueError("El correo o la contraseña son incorrectos")

     if not Security.verify_password(dto.contrasenia, usuariodb.contrasenia):
        raise ValueError("El correo o la contraseña son incorrectos")

     token = create_access_token({
        "idUsuario": usuariodb.idUsuario,
        "correo": usuariodb.correo,
        "nombre": usuariodb.nombre,
        "rol": usuariodb.rol.idRol
    })
     
     return {
        "mensaje": f"Bienvenido {usuariodb.nombre}",
        "token": token
    }
    
    ######### servicios para crear alumnos
    def crearAlumno(self, dto: AlumnoCreateDTO, archivoFoto = None)-> str:
        correovalidar = dto.correo.strip().lower()
 
        if self.repository.buscarPorCorreo(correovalidar):
            raise ValueError(f"El correo {dto.correo} ya está registrado")
       
        entidadRol = self.repositoryRol.obtenerRol(dto.rolId)

        entidadNivel = self.repositoryNivel.obtenerNivel(dto.nivelId)

        nombrefoto = "default.png"
        if archivoFoto:
            extension = os.path.splitext(archivoFoto.filename)[1]
            nombrefoto = f"{uuid.uuid4()}{extension}"
            
            basePath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            rutaCarpeta = os.path.join(basePath, "uploads", "fotos")
            if not os.path.exists(rutaCarpeta):
               os.makedirs(rutaCarpeta, exist_ok=True)

            rutaFinal = os.path.join(rutaCarpeta, nombrefoto)
            print(f"--- VERIFICANDO RUTA ---: {os.path.abspath(rutaFinal)}")

            with open(rutaFinal, "wb") as buffer:
                archivoFoto.file.seek(0)
                buffer.write(archivoFoto.file.read())
    
        nombrenivel = entidadNivel.nombreNivel.strip()
      
        entidadLic = None

        if nombrenivel =='Licenciatura':
            if not dto.licId:
             raise ValueError("Debe proporcionar una licenciatura para este nivel.")
        entidadLic = self.repositoryLic.obtenerLicenciatura(dto.licId)

        

        nuevoAlumno = Alumno(
        nombre=dto.nombre,
        correo=dto.correo,
        foto=nombrefoto,
        contrasenia=dto.contrasenia,
        rol=entidadRol,
        fechaInicio=dto.fechaInicio,
        fechaFin=dto.fechaFin,
        nivel=entidadNivel,
        licenciatura=entidadLic  
       )
        nuevoAlumno.contrasenia = Security.hash_password(dto.contrasenia)
        self.repository.crearAlumno(nuevoAlumno)
        return f"Los datos del alumno {nuevoAlumno.nombre} fueron guardados correctamente"
    

    #############
    def actualizarUsuario(self, dto: UsuarioUpdateDTO, archivoFoto = None) -> str:
        usuarioActual = self.repository.obtenerUsuarioPorId(dto.idUsuario)
        if not usuarioActual:
            raise ValueError("El usuario no existe")
        
        if dto.contrasenia and dto.contrasenia.strip():
          if not dto.contraseniaActual:
             raise ValueError("Debe proporcionar la contraseña actual para realizar cambios de seguridad")
        
          es_valida = Security.verify_password(dto.contraseniaActual, usuarioActual.contrasenia)
          if not es_valida:
              raise ValueError("La contraseña actual es incorrecta")
        
          password_final = Security.hash_password(dto.contrasenia)
        else:
          password_final = usuarioActual.contrasenia


        correovalidar = dto.correo.strip().lower()
        if correovalidar != usuarioActual.correo.lower():
            if self.repository.buscarPorCorreo(correovalidar):
                raise ValueError(f"El correo {dto.correo} ya está registrado por otro usuario")
        
        entidadRol = self.repositoryRol.obtenerRol(dto.rolId)
        foto_anterior = usuarioActual.foto 
        nombrefoto = foto_anterior 
        if archivoFoto:
            extension = os.path.splitext(archivoFoto.filename)[1]
            nombrefoto = f"{uuid.uuid4()}{extension}"
            basePath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            rutaCarpeta = os.path.join(basePath, "uploads", "fotos")
        
            if not os.path.exists(rutaCarpeta):
                os.makedirs(rutaCarpeta, exist_ok=True)

            rutaFinal = os.path.join(rutaCarpeta, nombrefoto)

            with open(rutaFinal, "wb") as buffer:
              archivoFoto.file.seek(0)
              buffer.write(archivoFoto.file.read())

       
        
            if foto_anterior and foto_anterior != "default.png":
               rutaFotoVieja = os.path.join(rutaCarpeta, foto_anterior)
               try:
                   if os.path.exists(rutaFotoVieja):
                       os.remove(rutaFotoVieja)
                       print(f"--- ARCHIVO ANTERIOR ELIMINADO ---: {foto_anterior}")
               except Exception as e:
                   print(f"Advertencia: No se pudo eliminar el archivo físico anterior: {e}")

    

    
        usuarioEditado = Usuario(
        nombre=dto.nombre,
        correo=dto.correo,
        foto=nombrefoto,
        contrasenia=password_final,
        rol=entidadRol
    )
        usuarioEditado.idUsuario = dto.idUsuario

       

        self.repository.actualizarUsuario(usuarioEditado)

        return {
    "mensaje": f"Los datos de {usuarioEditado.nombre} fueron actualizados correctamente",
    "foto": nombrefoto, 
}    
    
    ##########
    def actualizarAlumno(self, dto: AlumnoUpdateDTO, archivoFoto = None) -> str:
        alumnoActual = self.repository.obtenerAlumnoPorId(dto.idUsuario)
        if not alumnoActual:
            raise ValueError("El alumno no existe")
        

        if dto.contrasenia and dto.contrasenia.strip():
          if not dto.contraseniaActual:
             raise ValueError("Debe proporcionar la contraseña actual para realizar cambios de seguridad")
        
          es_valida = Security.verify_password(dto.contraseniaActual, alumnoActual.contrasenia)
          if not es_valida:
              raise ValueError("La contraseña actual es incorrecta")
        
          password_final = Security.hash_password(dto.contrasenia)
        else:
          password_final = alumnoActual.contrasenia

        correovalidar = dto.correo.strip().lower()
        if correovalidar != alumnoActual.correo.lower():
            if self.repository.buscarPorCorreo(correovalidar):
                raise ValueError(f"El correo {dto.correo} ya está registrado")

        entidadRol = self.repositoryRol.obtenerRol(dto.rolId)
        entidadNivel = self.repositoryNivel.obtenerNivel(dto.nivelId)
        
        entidadLic = None
        if entidadNivel.idNivel== 2:
            if not dto.licId:
                raise ValueError("Debe proporcionar una licenciatura para este nivel.")
            entidadLic = self.repositoryLic.obtenerLicenciatura(dto.licId)

        foto_anterior = alumnoActual.foto 
        nombrefoto = foto_anterior

        if archivoFoto:
            extension = os.path.splitext(archivoFoto.filename)[1]
            nombrefoto = f"{uuid.uuid4()}{extension}"
            
            basePath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            rutaCarpeta = os.path.join(basePath, "uploads", "fotos")
            
            if not os.path.exists(rutaCarpeta):
                os.makedirs(rutaCarpeta, exist_ok=True)

            rutaFinal = os.path.join(rutaCarpeta, nombrefoto)
            with open(rutaFinal, "wb") as buffer:
                archivoFoto.file.seek(0)
                buffer.write(archivoFoto.file.read())

            if foto_anterior and foto_anterior != "default.png":
                rutaFotoVieja = os.path.join(rutaCarpeta, foto_anterior)
                if os.path.exists(rutaFotoVieja):
                    os.remove(rutaFotoVieja)


        alumnoEditado = Alumno(
            nombre=dto.nombre,
            correo=dto.correo,
            foto=nombrefoto,
            contrasenia=password_final,
            rol=entidadRol,
            fechaInicio=dto.fechaInicio,
            fechaFin=dto.fechaFin,
            nivel=entidadNivel,
            licenciatura=entidadLic
        )
        alumnoEditado.idUsuario = dto.idUsuario


        self.repository.actualizarAlumno(alumnoEditado)

        return {
    "mensaje": f"Los datos del alumno {alumnoEditado.nombre} fueron actualizados correctamente",
    "foto": nombrefoto, 
}    
    #####
    def actualizarUsuarioAdmin(self, dto: UsuarioUpdateDTO, archivoFoto = None) -> str:
        usuarioActual = self.repository.obtenerUsuarioPorId(dto.idUsuario)
        if not usuarioActual:
            raise ValueError("El usuario no existe")
        correovalidar = dto.correo.strip().lower()
        if correovalidar != usuarioActual.correo.lower():
            if self.repository.buscarPorCorreo(correovalidar):
                raise ValueError(f"El correo {dto.correo} ya está registrado por otro usuario")
        
        entidadRol = self.repositoryRol.obtenerRol(dto.rolId)
        foto_anterior = usuarioActual.foto 
        nombrefoto = foto_anterior 
        if archivoFoto:
            extension = os.path.splitext(archivoFoto.filename)[1]
            nombrefoto = f"{uuid.uuid4()}{extension}"
            basePath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            rutaCarpeta = os.path.join(basePath, "uploads", "fotos")
        
            if not os.path.exists(rutaCarpeta):
                os.makedirs(rutaCarpeta, exist_ok=True)

            rutaFinal = os.path.join(rutaCarpeta, nombrefoto)

            with open(rutaFinal, "wb") as buffer:
              archivoFoto.file.seek(0)
              buffer.write(archivoFoto.file.read())

       
        
            if foto_anterior and foto_anterior != "default.png":
               rutaFotoVieja = os.path.join(rutaCarpeta, foto_anterior)
               try:
                   if os.path.exists(rutaFotoVieja):
                       os.remove(rutaFotoVieja)
                       print(f"--- ARCHIVO ANTERIOR ELIMINADO ---: {foto_anterior}")
               except Exception as e:
                   print(f"Advertencia: No se pudo eliminar el archivo físico anterior: {e}")

    
        password_final = usuarioActual.contrasenia 

        if dto.contrasenia and dto.contrasenia.strip():
           password_final = Security.hash_password(dto.contrasenia)
    
        usuarioEditado = Usuario(
        nombre=dto.nombre,
        correo=dto.correo,
        foto=nombrefoto,
        contrasenia=password_final,
        rol=entidadRol
    )
        usuarioEditado.idUsuario = dto.idUsuario

        self.repository.actualizarUsuario(usuarioEditado)

        return f"Los datos de {usuarioEditado.nombre} fueron actualizados correctamente"
    

    def actualizarAlumnoAdmin(self, dto: AlumnoUpdateDTO, archivoFoto = None) -> str:
    # 1. Buscamos al usuario (que es la base de todo)
     usuarioActual = self.repository.obtenerUsuarioPorId(dto.idUsuario)
     if not usuarioActual:
        raise ValueError("El usuario base no existe en el sistema")

    # 2. Intentamos buscar al alumno
     alumnoExistente = self.repository.obtenerAlumnoPorId(dto.idUsuario)
 
    # Validar correo (si cambió y ya existe en otro usuario)
     correovalidar = dto.correo.strip().lower()
     if correovalidar != usuarioActual.correo.lower():
        if self.repository.buscarPorCorreo(correovalidar):
            raise ValueError(f"El correo {dto.correo} ya está registrado")

    # 3. Preparar entidades de catálogo
     entidadRol = self.repositoryRol.obtenerRol(dto.rolId)
     entidadNivel = self.repositoryNivel.obtenerNivel(dto.nivelId)
    
     entidadLic = None
     if entidadNivel and entidadNivel.idNivel == 2: # Suponiendo 2 es Licenciatura
        if not dto.licId:
            raise ValueError("Debe proporcionar una licenciatura para este nivel.")
        entidadLic = self.repositoryLic.obtenerLicenciatura(dto.licId)

    # 4. Manejo de Foto (Misma lógica que ya tenías)
    # Si no hay alumno, usamos la foto del usuario actual
     foto_anterior = alumnoExistente.foto if alumnoExistente else usuarioActual.foto
     nombrefoto = foto_anterior
    # ... (aquí va tu bloque de guardado de archivoFoto que ya tienes) ...

    # 5. Gestionar Contraseña
     if dto.contrasenia and dto.contrasenia.strip():
        password_final = Security.hash_password(dto.contrasenia)
     else:
        password_final = usuarioActual.contrasenia

    # 6. Crear objeto de dominio Alumno con los datos nuevos
     alumnoDatos = Alumno(
        nombre=dto.nombre,
        correo=dto.correo,
        foto=nombrefoto,
        contrasenia=password_final,
        rol=entidadRol,
        fechaInicio=dto.fechaInicio,
        fechaFin=None, # Forzamos a None para que esté activo
        nivel=entidadNivel,
        licenciatura=entidadLic
    )
     alumnoDatos.idUsuario = dto.idUsuario

    # --- LÓGICA CRÍTICA ---
     if not alumnoExistente:
        # SI EL USUARIO EXISTE PERO EL ALUMNO NO: Lo creamos
        print(f"Creando registro de alumno para el usuario {dto.idUsuario}")
        self.repository.crearAlumno1(alumnoDatos)
     else:
        # SI YA EXISTE: Lo actualizamos
        self.repository.actualizarAlumno(alumnoDatos)

     return f"Los datos de {alumnoDatos.nombre} fueron procesados correctamente"
    #####################################
    def eliminarUsuario(self, dto: UsuarioDeleteDTO) -> str:
        usuarioActual = self.repository.obtenerUsuarioPorId(dto.idUsuario)
        rol = self.repositoryRol.obtenerRol(usuarioActual.rol)
        if not usuarioActual:
            raise ValueError("El usuario no existe")
        
        self.repository.eliminarUsuario(dto.idUsuario)

        return f"El {rol.nombreRol.lower()} {usuarioActual.nombre} fue eliminado exitosamente"
    
    def activarUsuario(self, dto: UsuarioDeleteDTO) -> str:
        usuarioActual = self.repository.obtenerUsuarioPorId(dto.idUsuario)
        rol = self.repositoryRol.obtenerRol(usuarioActual.rol)
        if not usuarioActual:
            raise ValueError("El usuario no existe")
        
        self.repository.activarUsuario(dto.idUsuario)

        return f"El {rol.nombreRol.lower()} {usuarioActual.nombre} fue activado exitosamente"
    
    #######
    def listarUsuario(self) -> List[dict]:
        usuarios = self.repository.listarUsuarios()
        resultado = []

        for u in usuarios:
           entidadRol = self.repositoryRol.obtenerRol(u.rol)
        
           resultado.append({
              "idUsuario": u.idUsuario,
              "nombre": u.nombre,
              "correo": u.correo,
             "foto": u.foto,
             "rol": entidadRol.nombreRol.lower(),
             "estatus": u.estatus
           })
        return resultado
    
    def listarAlumno(self) -> List[dict]:
        alumnos = self.repository.listarAlumno()
        resultado = []

        for a in alumnos:
            
            entidadRol = self.repositoryRol.obtenerRol(a.rol)
            entidadNivel = self.repositoryNivel.obtenerNivel(a.nivel)
            
            nombreLic = "N/A"
            if a.licenciatura:
                entidadLic = self.repositoryLic.obtenerLicenciatura(a.licenciatura)
                nombreLic = entidadLic.nombreLic

            resultado.append({
                "idUsuario": a.idUsuario,
                "nombre": a.nombre,
                "correo": a.correo,
                "foto": a.foto,
                "rol": entidadRol.nombreRol if entidadRol else "alumno",
                "nivel": entidadNivel.nombreNivel if entidadNivel else "N/A",
                "licenciatura": nombreLic,
                "fechaInicio": a.fechaInicio.isoformat() if a.fechaInicio else None,
                "fechaFin": a.fechaFin.isoformat() if a.fechaFin else None,
                "estatus": a.estatus
            })

        return resultado
    
    
    def filtradoAlumno(self, nombre=None, correo=None, nivelId=None, licenciaturaId=None, estado=int) -> List[dict]:
    # Regla de negocio
        if nivelId != 2: 
           licenciaturaId = None

        alumnos_entidad = self.repository.filtradoAlumno(nombre, correo, nivelId, licenciaturaId, estado)
    
        resultado = []
        for a in alumnos_entidad:
            entidadRol = self.repositoryRol.obtenerRol(a.rol)
            entidadNivel = self.repositoryNivel.obtenerNivel(a.nivel)

            nombreLic = "N/A"
            if a.licenciatura:
                entidadLic = self.repositoryLic.obtenerLicenciatura(a.licenciatura)
                nombreLic = entidadLic.nombreLic

            resultado.append({
                "idUsuario": a.idUsuario,
                "nombre": a.nombre,
                "correo": a.correo,
                "foto": a.foto,
                "rol": entidadRol.nombreRol if entidadRol else "alumno",
                "nivel": entidadNivel.nombreNivel if entidadNivel else "N/A",
                "licenciatura": nombreLic,
                "fechaInicio": a.fechaInicio.isoformat() if a.fechaInicio else None,
                "fechaFin": a.fechaFin.isoformat() if a.fechaFin else None,
                "estatus": a.estatus
        })
        return resultado
    
    def filtradoUsuario(self, nombre = None, correo = None, rol = None, estado = None) -> List[dict]:
         usuarios_entidad = self.repository.filtradoUsuario(nombre, correo, rol, estado)
      
         resultado = []

         for u in usuarios_entidad:
             entidadRol = self.repositoryRol.obtenerRol(u.rol)
        
             resultado.append({
            "idUsuario": u.idUsuario,
            "nombre": u.nombre,
            "correo": u.correo,
            "foto": u.foto,
            "rol": entidadRol.nombreRol, 
            "estatus": u.estatus
        })
         return resultado
    
    def obtenerUsuarioPorId(self, idUsuario: int) -> Usuario:

        return self.repository.obtenerUsuarioPorId(idUsuario)
    
    def obtenerAlumnoPorId(self, idUsuario:int) ->Alumno :
        return self.repository.obtenerAlumnoPorId(idUsuario)
