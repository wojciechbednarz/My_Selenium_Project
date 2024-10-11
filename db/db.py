from tinydb import TinyDB, Query
import logging

logger = logging.getLogger(__name__)


class EmployeeDatabaseFailInitializationException(Exception):
    """Custom exception for EmployeeDB initialization failures."""
    pass


class EmployeeDB:
    def __init__(self, db_path=None):
        self.db_path = db_path or ":memory:"
        self._db = None

    def __enter__(self):
        try:
            self._db = TinyDB(self.db_path)
            self.Employee = Query()
        except Exception as err:
            logging.error(f"Failed to initialize database from {self.db_path}: {err}")
            raise EmployeeDatabaseFailInitializationException("Failed to initialize database") from err
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._db:
            self._db.close()
        if exc_type is not None:
            logger.error(f"An error occurred: {exc_val}")

    def add_employee(self, employee):
        if not isinstance(employee, dict):
            raise ValueError("Data must be a dictionary")
        employee_id = self._db.insert(employee)
        logger.info(f"Employee added with ID: {employee_id}")
        return employee_id

    def remove_employee(self, employee_id):
        if self._db.contains(doc_id=employee_id):
            self._db.remove(doc_ids=[employee_id])
            logger.info(f"Employee with ID {employee_id} removed.")
        else:
            logger.error(f"Employee with ID {employee_id} not found.")

    def search_for_employee(self, employee_id):
        employee = self._db.get(doc_id=employee_id)
        if employee:
            return employee
        else:
            logger.error(f"Employee with id {employee_id} not found.")
            return None

    def remove_all_employees(self):
        self._db.truncate()
        logger.info("All employee records have been removed.")
