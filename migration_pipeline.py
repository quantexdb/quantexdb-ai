from pyspark.sql import SparkSession

# ------------------------
# Paths to JDBC drivers
# ------------------------
oracle_jar = "file:///D:/oracle_to_postgres_pipeline/libs/ojdbc8.jar"
postgres_jar = "file:///D:/oracle_to_postgres_pipeline/libs/postgresql-42.6.2.jar"

# ------------------------
# Create SparkSession with jars and Windows-friendly temp folder
# ------------------------
spark = SparkSession.builder \
    .appName("OracleToPostgresEMP") \
    .config("spark.jars", f"{oracle_jar},{postgres_jar}") \
    .config("spark.local.dir", "D:/oracle_to_postgres_pipeline/spark_temp") \
    .getOrCreate()

# ------------------------
# Oracle connection details
# ------------------------
oracle_url = "jdbc:oracle:thin:@localhost:1521/orcl"  # Replace 'orcl' with your service name
oracle_properties = {
    "user": "scott",       # Replace with your Oracle username
    "password": "tiger",   # Replace with your Oracle password
    "driver": "oracle.jdbc.driver.OracleDriver"
}

# Read EMP table from Oracle
emp_df = spark.read.jdbc(url=oracle_url, table="emp", properties=oracle_properties)
print("Data read from Oracle EMP table:")
emp_df.show()

# ------------------------
# PostgreSQL connection details
# ------------------------
postgres_url = "jdbc:postgresql://localhost:5432/postgres"  # Replace with your DB name
postgres_properties = {
    "user": "postgres",        # Replace with your Postgres username
    "password": "Admin",       # Replace with your Postgres password
    "driver": "org.postgresql.Driver"
}

# Write data to PostgreSQL EMP table (append mode)
emp_df.write.jdbc(url=postgres_url, table="emp", mode="append", properties=postgres_properties)

print("Migration completed successfully: Oracle EMP -> PostgreSQL EMP")

# ------------------------
# Stop Spark session
# ------------------------
spark.stop()
