from datetime import timedelta
from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
import psycopg2
from airflow.operators.python import PythonOperator

def load_csv_to_postgres():
    conn = psycopg2.connect(
        database="etl_toll_data",
        user="username",
        password="password",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    schema = "etl_data_loaded"
    table_name = "etl_toll"  # You can adjust this as needed
    file_path = "/airflow_projects/staging/transformed_data.csv"
    
    # Create schema if not exists
    create_schema_query = f'''
        CREATE SCHEMA IF NOT EXISTS {schema};
    '''
    cursor.execute(create_schema_query)
    conn.commit()
    
    # Create table if not exists
    create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {schema}.{table_name} (
            ID INTEGER,
            Date TIMESTAMP,
            Vehicle_number INTEGER,
            Vehicle_type VARCHAR,
            Axles_quantity INTEGER,
            Tollplaza_id INTEGER,
            Tollplaza_code VARCHAR,
            Payment_code_type VARCHAR,
            Vehicle_code VARCHAR
        );
    '''
    cursor.execute(create_table_query)
    conn.commit()

    # Load CSV file into the table
    with open(file_path, 'r') as f:
        # Use COPY command to load data from CSV
        copy_sql = f'''
            COPY {schema}.{table_name} (ID, Date, Vehicle_number, Vehicle_type, Axles_quantity, Tollplaza_id, Tollplaza_code, Payment_code_type, Vehicle_code)
            FROM stdin WITH CSV
        '''
        cursor.copy_expert(sql=copy_sql, file=f)
        conn.commit()

    cursor.close()
    conn.close()

default_args = {
    'owner': 'rnrolan',
    'start_date': days_ago(0),
    'email': ['example@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'ETL_Toll_Data',
    default_args=default_args,
    description='Road traffic data from different toll plaza',
    schedule_interval=timedelta(days=1),
)

unzip_data = BashOperator(
    task_id='unzip_data',
    bash_command='tar -xzf /airflow_projects/tolldata.tgz -C /airflow_projects/staging',
    dag=dag,
)

extract_data_from_csv = BashOperator(
    task_id='extract_data_from_csv',
    bash_command='cut -d "," -f1-4 /airflow_projects/staging/vehicle-data.csv > /airflow_projects/staging/csv_data.csv',
    dag=dag,
)

extract_data_from_tsv = BashOperator(
    task_id='extract_data_from_tsv',
    bash_command="awk -F'\\t' '{print $5\",\"$6\",\"$7}' /airflow_projects/staging/tollplaza-data.tsv | sed 's/\\r//' > /airflow_projects/staging/tsv_data.csv",
    dag=dag,
)

extract_data_from_fixed_width = BashOperator(
    task_id='extract_data_from_fixed_width',
    bash_command='cut -c59-67 /airflow_projects/staging/payment-data.txt | tr " " ","  > /airflow_projects/staging/fixed_width_data.csv',
    dag=dag,
)

consolidate_data = BashOperator(
    task_id='consolidate_data',
    bash_command='paste -d"," /airflow_projects/staging/csv_data.csv /airflow_projects/staging/tsv_data.csv /airflow_projects/staging/fixed_width_data.csv > /airflow_projects/staging/extracted_data.csv',
    dag=dag,
)

transform_data = BashOperator(
    task_id='transform_data',
    bash_command='tr "[a-z]" "[A-Z]" < /airflow_projects/staging/extracted_data.csv > /airflow_projects/staging/transformed_data.csv',
    dag=dag,
)

load_to_postgres = PythonOperator(
    task_id='load_to_postgres',
    python_callable=load_csv_to_postgres,
    dag=dag,
)

unzip_data >> extract_data_from_csv >> extract_data_from_tsv >> extract_data_from_fixed_width >> consolidate_data >> transform_data >> load_to_postgres