import xml.etree.ElementTree as ET  # Модуль для обработки XML данных
import shutil  # Импортируем модуль для работы с файлами и директориями


# Пути к рабочим файлам конфигурации
simulationModels = '/home/clover/catkin_ws/src/clover/clover_simulation/models/'
markerLaunch = '/home/clover/catkin_ws/src/clover/clover/launch/aruco.launch'
droneLaunch = '/home/clover/catkin_ws/src/clover/clover/launch/clover.launch'
environmentFile = '/home/clover/catkin_ws/src/clover/clover_simulation/resources/worlds/clover_aruco.world'
markerData = '/home/clover/catkin_ws/src/clover/aruco_pose/map/'


shutil.copytree('./models/main_tube', simulationModels + 'main_tube')
shutil.copytree('./models/tube', simulationModels + 'tube')



# Обработка файла мира (world)
try:
    # Чтение и анализ XML структуры мира
    environmentData = ET.parse(environmentFile)
    worldRoot = environmentData.getroot()
    
    # Получение информации о маркерах из конфигурации
    markerInfo = worldRoot[0][2][0].text.split('_')
    
    # Открытие файла с данными о карте маркеров
    mapFile = open(markerData + markerInfo[1] + '.' + markerInfo[2], 'r')
    
    # Извлечение параметра размера из файла карты
    markerSize = mapFile.read().split('\n')[1].split('\t')[1]
except:
    # Сообщение об отсутствии карты маркеров
    print('Нет карта маркеров! Используйте genmap.py, подробности: https://clover.coex.tech/en/aruco_map.html#marker-map-definition')
    exit()







# Настройка параметров системы маркеров aruco.launch
markerConfig = ET.parse(markerLaunch)
markerRoot = markerConfig.getroot()

# Обновление параметров конфигурации маркеров
for index in range(len(markerConfig.findall('arg'))):
    if markerRoot[index].attrib['name'] in ['aruco_detect', 'aruco_map', 'aruco_vpe']:
        markerRoot[index].attrib['default'] = 'true'  # Активация модулей работы с маркерами
    elif markerRoot[index].attrib['name'] == 'placement':
        markerRoot[index].attrib['default'] = 'floor'  # Расположение маркеров на полу
    elif markerRoot[index].attrib['name'] == 'map':
        markerRoot[index].attrib['default'] = markerInfo[1] + '.' + markerInfo[2]  # Имя файла карты
    elif markerRoot[index].attrib['name'] == 'length':
        markerRoot[index].attrib['default'] = markerSize  # Установка размера маркера

# Сохранение обновленной конфигурации
markerConfig.write(markerLaunch)





# Конфигурация основных параметров дрона clover.launch
droneConfig = ET.parse(droneLaunch)
droneRoot = droneConfig.getroot()

# Настройка рабочих модулей системы
for index in range(len(droneConfig.findall('arg'))):
    if droneRoot[index].attrib['name'] in ['simulator', 'web_video_server', 'rosbridge', 'main_camera', 'optical_flow', 'aruco', 'rangefinder_vl53l1x', 'led']:
        droneRoot[index].attrib['default'] = 'true'  # Включение основных систем
    elif droneRoot[index].attrib['name'] in ['blocks', 'rc']:
        droneRoot[index].attrib['default'] = 'false'  # Отключение вспомогательных модулей

# Запись изменений в файл конфигурации
droneConfig.write(droneLaunch)