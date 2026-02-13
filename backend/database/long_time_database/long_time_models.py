from sqlalchemy import Table,Column,String,MetaData


metadata_obj = MetaData()

main_table = Table(
    "long_time_table",
    metadata_obj,
    Column("username",String,primary_key=True),
    Column("last_date",String)
    
)
