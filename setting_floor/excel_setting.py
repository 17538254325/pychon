import xlrd
from xlutils.copy import copy

def read_interface(case_file_url,case_sheet):
    lol_file = xlrd.open_workbook(case_file_url)

    sheet_file = lol_file.sheet_by_name(case_sheet)
    shop_bi = []
    for i in range(1, sheet_file.nrows):
        # [text: 'lol_shop_01', text: '添加商品信息', text: '购物模块', text: 'http://127.0.0.1:8080/lol/servlet/shop', text: 'post', text: '{"method":"addGoods","id":"zq-001","name":"牙刷","num":"100","price":"9.65"}', text: '[{"message":"新增成功","商品ID":"zq-001","商品名称":"牙刷","商品数量":"100","商品价格":"9.65"}]', empty: '', empty: '']
        shop_zi = {}

        shop_zi["shop_name"] = sheet_file.row(i)[1].value
        shop_zi["shop_path"] = sheet_file.row(i)[3].value
        shop_zi["shop_requ"] = sheet_file.row(i)[4].value
        shop_zi["shop_query"] = sheet_file.row(i)[5].value
        shop_zi["shop_expected"] = sheet_file.row(i)[6].value

        shop_bi.append(shop_zi)

    return shop_bi




def write_test_result(resp_text_list,result_list,case_file_url,case_sheet):
    shop_case = xlrd.open_workbook(case_file_url)

    new_shop_case = copy(shop_case)

    new_sheet = new_shop_case.get_sheet(case_sheet)

    for i in range(len(result_list)):
        new_sheet.write(i + 1, 7, resp_text_list[i])
        new_sheet.write(i + 1, 8, result_list[i])

    new_shop_case.save(case_file_url)



def get_sheet_list(excel_file_url):

    lol_file = xlrd.open_workbook(excel_file_url)

    return lol_file.sheet_names()

