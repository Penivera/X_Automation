from x import ReadFIle


file= ReadFIle(login_file='login.csv',url_file='urls.json')
print(file.login_data,file.Links)