from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, EmailStr
import sqlite3
from typing import List, Dict


def connection():
    return sqlite3.connect("employees.db")

def db_connection(sql: str):
    try:
        mydb = connection()
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        mydb.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if mydb:
            mydb.close()

def get_sql_data_all_dict(sql: str) -> List[Dict[str, any]]:

    def row_to_dict(cursor, row):
        return {cursor.description[i][0]: row[i] for i in range(len(row))}

    try:
        mydb = connection()
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        rows = mycursor.fetchall()
        result = [row_to_dict(mycursor, row) for row in rows]
        return result
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        raise  
    finally:
        if mydb:
            mydb.close()

def create_table():
    try:
        mydb = connection()
        mycursor = mydb.cursor()
        mycursor.execute("""
            SELECT name from sqlite_master where type='table' and name='employees';
        """)
        if not mycursor.fetchone():
            mycursor.execute("""
                CREATE TABLE employees (
                    emp_id integer PRIMARY KEY AUTOINCREMENT,
                    emp_name varchar(100),
                    emp_mobile_number varchar(100),
                    emp_email varchar(100),
                    emp_designation varchar(100)
                );
            """)
            print("Table created successfully.")
        else:
            print("Table already exists.")
        mydb.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if mydb:
            mydb.close()

create_table()

class insert_employee(BaseModel):
    emp_name: str
    emp_mobile_number: str
    emp_email: EmailStr
    emp_designation: str

class update_employee(BaseModel):
    emp_id: int
    emp_name: str
    emp_mobile_number: str
    emp_email: EmailStr
    emp_designation: str

app = FastAPI()



@app.post("/employees/insert_details", tags=['Employee'])
def create_employee(q: insert_employee, response: Response):
    try:
        sql = f"""
        INSERT INTO employees (emp_name, emp_mobile_number, emp_email, emp_designation)
        VALUES ('{q.emp_name}','{q.emp_mobile_number}', '{q.emp_email}', '{q.emp_designation}')
        """
        
        if len(q.emp_name) == 0 :
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"status": "failed", "error_code": 400, "msg": "Employee name can't be empty", "data": []}
        elif len(q.emp_mobile_number)!=10 or not q.emp_mobile_number.isdigit():
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"status": "failed", "error_code": 400, "msg": "Enter valid mobile number", "data": []}
        elif len(q.emp_designation) == 0:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"status": "failed", "error_code": 400, "msg": "Employee designation can't be empty", "data": []}
        else:
            db_connection(sql)
            response.status_code = status.HTTP_200_OK
            return {"status": "success", "error_code": 200, "msg": "Data inserted successfully", "data": {"emp_name": q.emp_name,"emp_mobile_number": q.emp_mobile_number,"emp_email": q.emp_email,"emp_designation": q.emp_designation
            }}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"status": "failed", "error_code": 500, "msg": "Internal Server Error", "data": []}
    

@app.get("/employees/get_employee", tags=['Employee'])
def get_employee(emp_id:int = None, response: Response = None): # if you enter the emp_id you will get data of that specific employee but if you keep it blank than it will give data of all employees.
    try:
        sql ="select * from employees"
        if emp_id :
            sql += f" where emp_id={emp_id}"
        data=get_sql_data_all_dict(sql)
        if data == None or not data:   
            if emp_id:
                response.status_code = status.HTTP_400_BAD_REQUEST
                return {"status": "failed", "error_code": 400, "msg": "Employee with this ID does not exist", "data": []} 
            response.status_code = status.HTTP_200_OK
            return {"status": "success", "error_code": 200, "msg": "No data found", "data": []}   
        else: 
            response.status_code = status.HTTP_200_OK
            return {"status": "success", "error_code": 200, "msg": "Data fetched successfully", "data": data}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"status": "failed", "error_code": 500, "msg": "Internal Server Error", "data": []}


@app.put("/employees/update_employee", tags=['Employee'])
def update_employee_by_id(q: update_employee,  response: Response):
    try:
        id_check = f"SELECT * FROM employees WHERE emp_id={q.emp_id}"
        data = get_sql_data_all_dict(id_check)
        
        if data == None or not data:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"status": "failed", "error_code": 400, "msg": "Employee with this ID does not exist", "data": []}
        elif len(q.emp_name) == 0 :
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"status": "failed", "error_code": 400, "msg": "Employee name can't be empty", "data": []}
        elif len(q.emp_mobile_number)!=10 or not q.emp_mobile_number.isdigit():
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"status": "failed", "error_code": 400, "msg": "Enter valid mobile number", "data": []}
        elif len(q.emp_designation) == 0:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"status": "failed", "error_code": 400, "msg": "Employee designation can't be empty", "data": []}
        else:
            sql = f"""
            update employees set emp_name='{q.emp_name}', emp_mobile_number='{q.emp_mobile_number}', emp_email='{q.emp_email}' , emp_designation='{q.emp_designation}' where emp_id='{q.emp_id}'"""
            db_connection(sql)
            response.status_code = status.HTTP_200_OK
            return {"status": "success", "error_code": 200, "msg": "Data updated successfully", "data": []}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"status": "failed", "error_code": 500, "msg": "Internal Server Error", "data": []}
   

@app.delete("/employees/delete_employee", tags=['Employee'])
def delete_employee_by_id(id:int, response: Response):
    try:
        sql_check = f"SELECT * FROM employees WHERE emp_id={id}"
        data = get_sql_data_all_dict(sql_check)
        
        if data == None or not data:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"status": "failed", "error_code": 400, "msg": "Employee with this ID does not exist", "data": []}
        else:
            sql = f"""
            delete from employees where emp_id={id}"""
            
            db_connection(sql)
            response.status_code = status.HTTP_200_OK
            return {"status": "success", "error_code": 200, "msg": "Data deleted successfully", "data": []}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"status": "failed", "error_code": 500, "msg": "Internal Server Error", "data": []}