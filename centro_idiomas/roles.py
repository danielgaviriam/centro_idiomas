from rolepermissions.roles import AbstractUserRole

class Administrador(AbstractUserRole):
    available_permissions = {
        
    }

class Root(AbstractUserRole):
    available_permissions = {
        
    }
    
class Estudiante(AbstractUserRole):
    available_permissions = {
        
    }
    
class Calificador(AbstractUserRole):
    available_permissions = {
        
    }