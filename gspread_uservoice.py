import gspread

class Spreadsheet(object):
    def __init__(self, login, login_psswd, spreadsheet_name, worksheet_name):
        self.login = self.set_login(login, login_psswd)
        self.spreadsheet = self.set_spreadsheet(spreadsheet_name)
        self.worksheet = self.set_worksheet(worksheet_name)
        self.bug_totals = 0
        self.feature_totals = 0
        self.users_to_delete = 0
        self.set_worksheet_headers()
        
    def set_login(self,login, login_psswd):
        return gspread.login(login, login_psswd)
    
    def set_spreadsheet(self, spreadsheet_name):
        return self.login.open(spreadsheet_name)
    
    def set_worksheet(self, worksheet_name):
        return self.spreadsheet.worksheet(worksheet_name)
        
    def get_all_worksheets(self):
        return self.spreadsheet.worksheets
    
    def set_worksheet_headers(self):
        try:
            if self.check_row_values(1) == True:
                self.worksheet.update_acell('A1', 'Bugs')
                self.worksheet.update_acell('C1', 'Features')
                self.worksheet.update_acell('E1', 'Users to Delete')
        except Exception:
            return 'Something wrong with Row1'
        
        try:
            if self.check_row_values(2) == True:
                self.worksheet.update_acell('A2', 'Total')
                self.worksheet.update_acell('C2', 'Total')
                
        except Exception:
            return 'Something wrong with Row2'
        
    def check_row_values(self, row):
        if not self.get_row_values(row):
            return True
        else:
            return self.get_row_values(row)
    
    def check_cell_value(self, label):
        if self.worksheet.acell(label).value != None:
            return True
        else:
            return False

    def get_all_worksheets(self):
        return self.spreadsheet.worksheets
    
    def get_cell_value(self, label):
        return self.worksheet.acell(label).value

    def get_cell_value_with_coord(self, row, col):
        return self.worksheet.cell(row, col).value

    def get_row_values(self, row):
        return self.worksheet.row_values(row)
        
    def get_col_values(self, col):
        return self.worksheet.col_values(col)

    def update_cell(self, label, value):
        self.worksheet.update_acell(label, str(value))

    def update_cell_with_coord(row, col, value):
        self.worksheet.update_cell(row, cole, value)

    def search_for_cell(self, value):
        return self.worksheet.find(str(value))
    
    def update_users_to_delete(self, user_email):
        row_counter = 3
        while True:
            if self.check_cell_value('E' + str(row_counter)) == True:
                row_counter = row_counter + 1
            else:
                self.update_cell('E' + str(row_counter), user_email)
                return False

    def update_bugs(self, bug_report, device_data):
        row_counter = 3
        while True:
            if self.check_cell_value('A' + str(row_counter)) == True:
                row_counter = row_counter + 1
            else:
                self.update_cell('A' + str(row_counter), bug_report)
                self.update_cell('B' + str(row_counter), device_data)
                return False

    def update_features(self, feature_request):
        try:
            feature = self.worksheet.find(feature_request)
            feature_value = self.worksheet.cell(feature.row, feature.col + 1)
            self.worksheet.update_cell(feature.row, feature.col +1, int(feature_value.value) + 1)
            return True

        except:
            row_counter = 3
            while True:
                if self.check_cell_value('C' + str(row_counter)) == True:
                    row_counter = row_counter + 1
                else:
                    self.update_cell('C' + str(row_counter), str(feature_request))
                    self.update_cell('D' + str(row_counter), 1)
                    return False
    

gs = Spreadsheet()##<- INFORMATION REDACTED FOR SECURITY REASONS. CREDENTIALS MUST BE PROVIDED FOR THIS TO WORK. ASK ABOUT CREDENTIALS FOR A DEMONSTRATION

    
    