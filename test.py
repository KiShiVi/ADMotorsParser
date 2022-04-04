a = 'aaaaa \"\" title=\"Название товара1Hello!!\"'
print(a[a.find('title') + 7:][:a[a.find('title') + 7:].find('\"')])