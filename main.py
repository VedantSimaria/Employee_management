class Employee:
    def __init__(self, emp_id, emp_name, emp_mobile_number, emp_email, emp_designation):
        self.emp_id = emp_id
        self.emp_name = emp_name
        self.emp_mobile_number = emp_mobile_number
        self.emp_email = emp_email
        self.emp_designation = emp_designation


class EmployeeManagement:
    def __init__(self):
        self.employees = []

    def validate_employee_data(self, emp_id, emp_name, emp_mobile_number, emp_email, emp_designation):
        if not isinstance(emp_id, int) or emp_id <= 0:
            raise ValueError("Employee ID must be a positive integer.")
        if not emp_name or not isinstance(emp_name, str):
            raise ValueError("Employee name can't be empty.")
        if not isinstance(emp_mobile_number, str) or len(emp_mobile_number) != 10 or not emp_mobile_number.isdigit():
            raise ValueError("Employee mobile number must be a 10 digit string.")
        if '@' not in emp_email or '.' not in emp_email:
            raise ValueError("Invalid email address.")
        if not emp_designation or not isinstance(emp_designation, str):
            raise ValueError("Employee designation can't be empty.")

    def create_employee(self, emp_id, emp_name, emp_mobile_number, emp_email, emp_designation):
        try:
            self.validate_employee_data(emp_id, emp_name, emp_mobile_number, emp_email, emp_designation)
            for emp in self.employees:
                if emp.emp_id == emp_id:
                    raise ValueError("Employee ID already exists.")
            new_employee = Employee(emp_id, emp_name, emp_mobile_number, emp_email, emp_designation)
            self.employees.append(new_employee)
            print("Employee created successfully.")
        except Exception as e:
            print(f"Error: {e}")

    def read_employee(self, emp_id = None): # if you enter the emp_id you will get data of that specific employee but if you keep it blank than it will give data of all employees exist locally.
        try:
            if emp_id is None:
                return [
                    {
                        "emp_id": emp.emp_id,
                        "emp_name": emp.emp_name,
                        "emp_mobile_number": emp.emp_mobile_number,
                        "emp_email": emp.emp_email,
                        "emp_designation": emp.emp_designation
                        
                    }
                    for emp in self.employees
                ]
            for emp in self.employees:
                if emp.emp_id == emp_id:
                    return {
                        "emp_id": emp.emp_id,
                        "emp_name": emp.emp_name,
                        "emp_mobile_number": emp.emp_mobile_number,
                        "emp_email": emp.emp_email,
                        "emp_designation": emp.emp_designation
                    }
            raise ValueError(f"Employee with id {emp_id} not found.")
        except Exception as e:
            print(f"Error: {e}")

    def update_employee(self, emp_id, emp_name=None, emp_mobile_number=None, emp_email=None, emp_designation=None):
        try:
            emp_found = False
            for emp in self.employees:
                if emp.emp_id == emp_id:
                    emp_found = True
                    if emp_name:
                        self.validate_employee_data(emp_id, emp_name, emp_mobile_number or emp.emp_mobile_number, emp_email or emp.emp_email, emp_designation or emp.emp_designation)
                        emp.emp_name = emp_name
                    if emp_mobile_number:
                        self.validate_employee_data(emp_id, emp.emp_name, emp_mobile_number, emp_email or emp.emp_email, emp_designation or emp.emp_designation)
                        emp.emp_mobile_number = emp_mobile_number
                    if emp_email:
                        self.validate_employee_data(emp_id, emp.emp_name, emp_mobile_number or emp.emp_mobile_number, emp_email, emp_designation or emp.emp_designation)
                        emp.emp_email = emp_email
                    if emp_designation:
                        self.validate_employee_data(emp_id, emp.emp_name, emp_mobile_number or emp.emp_mobile_number, emp_email or emp.emp_email, emp_designation)
                        emp.emp_designation = emp_designation
                    print("Employee updated successfully.")
                    break
            if not emp_found:
                raise ValueError("Employee not found.")
        except Exception as e:
            print(f"Error: {e}")

    def delete_employee(self, emp_id):
        try:
            emp_found = False
            for emp in self.employees:
                if emp.emp_id == emp_id:
                    emp_found = True
                    self.employees.remove(emp)
                    print("Employee deleted successfully.")
                    break
            if not emp_found:
                raise ValueError("Employee not found.")
        except Exception as e:
            print(f"Error: {e}")


em = EmployeeManagement()
em.create_employee(1, "Vedant", "1234567890", "vedant@gmail.com", "Developer")
em.create_employee(2, "Simaria", "0987654321", "simaria@gmail.com", "Designer")

print("Data of employee with id 1",em.read_employee(1))

print("\n")

print("Data of employee with id 2",em.read_employee(2))

print("\n")

em.update_employee(1, emp_name="Vedant Atul Simaria")
print("Data of employee with id 1 after updating the data",em.read_employee(1))

print("\n")

print("Get data of all employees",em.read_employee())

print("\n")

em.delete_employee(2)
em.read_employee(2)

 