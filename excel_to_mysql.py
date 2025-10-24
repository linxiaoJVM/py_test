"""
功能：将Excel数据导入到MySQL数据库
"""
# -- coding: utf-8 --
import xlrd
import MySQLdb
# Open the workbook and define the worksheet
book = xlrd.open_workbook("D:\\aa.xlsx")
sheet = book.sheet_by_name("aa")

#建立一个MySQL连接
database = MySQLdb.connect (host="rm-2ze8vch3mlfl995kr90110.mysql.rds.aliyuncs.com", user = "vcgapp", passwd = "cbkHw&PNW9n2C8en", db = "boss3")

# 获得游标对象, 用于逐行遍历数据库数据
cursor = database.cursor()

# 创建插入SQL语句
query = """INSERT INTO orders (product, customer_type, rep, date, actual, expected, open_opportunities, closed_opportunities, city, state, zip, population, region) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

# 创建一个for循环迭代读取xls文件每行数据的, 从第二行开始是要跳过标题
for r in range(1, sheet.nrows):
    product      = sheet.cell(r,0).value
    customer = sheet.cell(r,1).value
    rep          = sheet.cell(r,2).value
    date     = sheet.cell(r,3).value
    actual       = sheet.cell(r,4).value
    expected = sheet.cell(r,5).value
    open        = sheet.cell(r,6).value
    closed       = sheet.cell(r,7).value
    city     = sheet.cell(r,8).value
    state        = sheet.cell(r,9).value
    zip         = sheet.cell(r,10).value
    pop          = sheet.cell(r,11).value
    region   = sheet.cell(r,12).value

    values = (product, customer, rep, date, actual, expected, open, closed, city, state, zip, pop, region)

    # 执行sql语句
    cursor.execute(query, values)

# 关闭游标
cursor.close()

# 提交
database.commit()

# 关闭数据库连接
database.close()

# 打印结果
print("")
print("Done!")
columns = str(sheet.ncols)
rows = str(sheet.nrows)
# print ("我刚导入了 " columns %2B " 列 and " %2B rows %2B " 行数据到MySQL!")
