user = {
            'name' : 'cool',
            'gender' : None,
            'birth' : '1900-01-01',
            'note' : 'mono',
        }
        
query = []
for key , value in user.items():
    if value != None:
        query.append(key + " = " + " {} ".format(value))
query = ",".join(query)
print(query)
