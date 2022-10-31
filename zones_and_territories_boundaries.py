import xml.etree.ElementTree as ET
import os

# функция возвращает список .xml файлов из папки, включая подпапки, кроме proto_.xml
def get_file_list(path_KPT):
    filelist = []
    for root, dirs, files in os.walk(path_KPT):
        for file in files:
            if file.endswith(".xml") and file != "proto_.xml":
                filelist.append(os.path.join(root, file))
    print("Проверка пути", filelist)  #  Проверка пути!!!!!!!!!!!!!!!!
    return filelist


#  MIF Функция парсит кпт и вытаскивает количество контуров, количество точек и их координаты
def make_list_for_mif_actual_land(file_name):
    list_land = []
    tree = ET.parse(file_name)
    # ------------------------------возвращает список участков----------------------------------------------
    zones_and_territories_records = tree.findall('cadastral_blocks/cadastral_block/zones_and_territories_boundaries/zones_and_territories_record')
    for zones_and_territories_record in zones_and_territories_records:
        #  ---------------------------возвращает список контуров в каждом участке----------------------------
        spatal_elements = zones_and_territories_record.findall("./b_contours_location/contours/contour/entity_spatial/"
                                              "spatials_elements/spatial_element")
        if len(spatal_elements) > 0:
            list_land.append("Region ")
            list_land.append(len(spatal_elements))
            for spatal_element in spatal_elements:
                # ---------------возвращает список координат точек в каждом контуре в каждом участке---------
                ordinates = spatal_element.findall("./ordinates/ordinate")
                list_land.append(len(ordinates))
                # возращаем значение координат из списка
                for ordinate in ordinates:
                    y = ordinate.find('y').text
                    x = ordinate.find('x').text
                    list_land.append(y)
                    list_land.append(x)
    return list_land


#  MIF Функция печатает в файл mif заголовочные данные
def print_head_mif(path_mid_mif):
    file_mif_head = open(path_mid_mif + '/zones_and_territories_boundaries.mif', 'a')
    head_data = [
        'Version   450',
        'Charset "WindowsCyrillic"',
        'Delimiter ","',
        'CoordSys Earth Projection 8, 1001, "m", 88.466666, 0, 1, 2300000, -5512900.5630000001 '
        'Bounds (-5949281.53901, -15515038.0608) (10549281.539, 4489236.93476)',
        'Columns 6',
        'type_boundary Char(50)',
        'code_boundary Char(3)'
        'reg_numb_border Char(30)',
        'type_zone Char(100)',
        'code_type_zone Char(13)',
        'date_download Char(10)',
        'Data'
        ]
    for index in head_data:
        file_mif_head.write(index + '\n')
    file_mif_head.close()


def make_list_for_mid_actual_land(file_name):
    tree = ET.parse(file_name)
    root = tree.getroot()
    request = root[1][0].text
    list_semantic_land = ''
    data = tree.findall('cadastral_blocks/cadastral_block/zones_and_territories_boundaries/zones_and_territories_record')
    for data1 in data:
        #  ------------------- проверка на наличие координат границ------------------------------------------
        coordinates = data1.findall("./b_contours_location/contours/contour/entity_spatial/"
                                              "spatials_elements/spatial_element")
        if len(coordinates) > 0:
            #  -------------------Тип объекта------------------------------------------
            data2 = data1.findall('./b_object_zones_and_territories/b_object/type_boundary/value')
            if len(data2) >= 1:
                for type in data2:
                    _type_boundary = type.text
            else:
                _type_boundary = "None"
            #  -------------------Код зоны------------------------------------------
            data21 = data1.findall('./b_object_zones_and_territories/b_object/type_boundary/code')
            if len(data21) >= 1:
                for code_boundary in data21:
                    _code_boundary = code_boundary.text
            else:
                _code_boundary = "None"
            #  -------------------Рег номер зоны------------------------------------------
            data3 = data1.findall('./b_object_zones_and_territories/b_object/reg_numb_border')
            if len(data3) >= 1:
                for reg_numb_border in data3:
                    _reg_numb_border = reg_numb_border.text
            else:
                _reg_numb_border = "None"
            #  -------------------Тип зоны-------------------------------------------
            data4 = data1.findall('./b_object_zones_and_territories/type_zone/value')
            if len(data4) >= 1:
                for type_zone in data4:
                    _type_zone = type_zone.text
            else:
                _type_zone = "None"
            #  -------------------Код типа зоны--------------
            data5 = data1.findall('./b_object_zones_and_territories/type_zone/code')
            if len(data5) >= 1:
                for code in data5:
                    _code = code.text
            else:
                _code = "None"
            # ----------------Формирует строку mid файла-----------------------
            a = ("\"" + _type_boundary[:50] +
                 "\"," + "\"" + _code_boundary[:30] +
                 "\"," + "\"" + _reg_numb_border[:30] +
                 "\"," + "\"" + _type_zone[:100] +
                 "\"," + "\"" + _code[:13] +
                 "\"," + "\"" + request +
                 "\"," + "\n")
            # Формирует данные по всем строкам для записи в mid файл
            list_semantic_land = (list_semantic_land + a)
    print(list_semantic_land)
    return list_semantic_land

if __name__ == '__main__':
    path_mid_mif = str(input('Укажите путь к папке, куда сохранить mid/mif в формате D:/project_Python/XML_Parser/1 '))
    print_head_mif(path_mid_mif)
# -------------------------Открываем поочередно кпт.xml файлы----------------------------------
    path_KPT = str(input('Укажите путь к папке, где содержатся КПТ в формате D:/project_Python/XML_Parser/1 '))
    filelist = get_file_list(path_KPT)
    for file_name in filelist:
        file_mif = open(path_mid_mif + '/zones_and_territories_boundaries.mif', 'a')
# ------------------------записываем полученный список в mif файл-------------------------------
        list_coordinate_land_record = make_list_for_mif_actual_land(file_name)
        for data8 in list_coordinate_land_record:
           file_mif.write(str(data8) + '\n')
        file_mif.close()
# ---------------------------записываем данные mid в файл---------------------------------------
        land = make_list_for_mid_actual_land(file_name)
        file_mid = open(path_mid_mif + '/zones_and_territories_boundaries.mid', 'a')
        file_mid.write(land)
        file_mid.close()
