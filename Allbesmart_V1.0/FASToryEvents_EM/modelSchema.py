from FASToryEvents_EM import ma
from FASToryEvents_EM.dbModels import FASToryEvents,WorkstationInfo

class EeventSchema(ma.SQLAlchemyAutoSchema):
    class meta:
        model = FASToryEvents

class InfoSchema(ma.SQLAlchemyAutoSchema):
    class meta:
        model = WorkstationInfo