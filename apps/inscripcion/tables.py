from models import Inscripcion_Examen
from table import Table
from table.columns import Column

class CitacionTable(Table):
    id = Column(field='id', header=u'Id')
    nota = Column(field='nota', header=u'nota')
    inscripcion = Column(field='inscripcion.persona.nombres', header=u'inscripcion')
    citacion = Column(field='citacion.salon', header=u'citacion')
    nivel_sugerido = Column(field='nivel.nombre', header=u'nivel')
    class Meta:
        model = Inscripcion_Examen