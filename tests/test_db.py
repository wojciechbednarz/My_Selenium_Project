from db.db import EmployeeDB
from unittest import mock


def test_add_employee_to_db(temp_file):
    with EmployeeDB(db_path=temp_file) as db:
        employee_id = db.add_employee({"name": "Jan"})
        search_for_employee = db.search_for_employee(employee_id)
    assert search_for_employee is not None


def test_remove_employee_to_db_(temp_file):
    with EmployeeDB(db_path=temp_file) as db:
        employee_id = db.add_employee({"name": "Jan"})
        db.remove_employee(employee_id)
        search_for_employee = db.search_for_employee(employee_id)
    assert search_for_employee is NoneS


def test_add_employee_to_db_mocked():
    with mock.patch('tinydb.TinyDB') as MockTinyDB:
        mock_db = MockTinyDB.return_value
        mock_db.insert.return_value = 1
        with mock.patch('db.db.EmployeeDB.__init__', return_value=None) as MockEmployeeDBInit:
            db = EmployeeDB(None)
            db.db_path = ":memory:"
            db._db = mock_db
            emp_id = db.add_employee({"name": "Alice", "role": "In Wonderland"})
            assert emp_id is not None
