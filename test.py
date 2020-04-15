import cellyzer as cz

records = cz.read_call('G:\messages.xlsx','xlsx')
print(records.get_all_users())
