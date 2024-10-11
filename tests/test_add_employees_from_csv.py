
def test_add_employees_from_csv(open_browser_and_navigate_to_pim_page, employees_csv):
    pim_page = open_browser_and_navigate_to_pim_page
    employees_count = pim_page.get_length_of_employees()
    pim_page.add_employees_from_csv(employees_csv.name)
    employees = pim_page.get_all_employees()

    assert len(employees) == employees_count + 2
    assert employees[-2]['FirstName'] == 'John'
    assert employees[-2]['LastName'] == 'Doe'
    assert employees[-1]['FirstName'] == 'Jane'
    assert employees[-1]['LastName'] == 'Smith'


# def add_employees_from_csv(self, csv_file_path):
#     with open(csv_file_path, 'r') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             self.add_employee(row["FirstName"], row["LastName"], row["Username"], row["Password"])
#
