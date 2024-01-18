from excel import Excel
excel = Excel('C:\\Users\\95329\\Desktop\\20240105依据采购平台信息调整 - 医院（省中心整理仅供参考）.xlsx','变更')
# excel.find_value('项目编码')
excel.read_data_cols(2,['项目编码','通用名称','备注'])