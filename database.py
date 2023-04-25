from sqlalchemy import create_engine, text


db_connection = "mysql+pymysql://4u638pzvhu4ta106fhhs:pscale_pw_OPZ0NxrN4YJCBTZiMqPV6V7c5SMFuK0eoHrqWXGz2VM@aws.connect.psdb.cloud/smart-diet-application?charset=utf8mb4"

engine = create_engine(
  db_connection,
  connect_args={
    "ssl": {
      "ssl_ca": "/etc/ssl/cert.pem",
    }
    
  })

with engine.connect() as conn:
  result = conn.execute(text("select * from diet"))

  results_dicts=[]
  for row in result.all():
    results_dicts.append(dict(row))
    
  
  print(result)

