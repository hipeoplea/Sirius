from data.Bd_core import connect
from data.CreateDB import create_tables


engine = connect()
create_tables(engine)
