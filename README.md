|||
| --- | --- |
| Трек | Летающая робототехника |
| Задание | Командное задание |
| Тип | Инструкция |
| Команда | КвадроКотики |

|Участник| Роль |
| --- | --- |
| • Демьян Тарасов | капитан, инженер программист|
| • Андрей Петров | инженер техник |
| • Даниил Белов | программист |
| • Александр Перминов | мимокрокодил |

## 1. Установка виртуальной машины.

Для установки виртуальной машины необходимо скачать ПО для виртуализации (Virtual Box, WMVare Player или WMVare Workstation). 
В нашем примере мы будем использовать WMVare Workstation Pro. 
- Устанавливаем ПО для виртуализации
- Скачиваем образ виртуальной машины с симулятором Клевера с репозитория по ссылке: 
 [Release v1.4 · CopterExpress/clover_vm](https://github.com/CopterExpress/clover_vm/releases/tag/v1.4) 
 - Открываем ПО для виртуализации, нажимаем `CTRL+O` , или `File->Open` чтобы открыть существующую виртуальную машину. Выбираем скаченный файл `clover-devel_v1.4.ova`
 - Нам предложат ввести название виртуальной машины. Называем `Clover`
 - После установки образа и создания ВМ мы можем её настроить. Выбираем нашу ВМ в правой колонке `Library`. Затем нажимаем `Edit virtual machine settings`. В открывшемся окне настраиваем параметры:
	 - Memory. Необходимо выделить минимум половину от имеющейся оперативной памяти. (У нас это будет 8Гб), но мы выбираем выделить около 12-13 Гб, т.к. в целом при 16Гб это не сильно повлияет на работоспособность ПК, но ускорит работу симуляции. 
	- Processors. Количество процессоров - 1 (Number of processors).
				Количество ядер - 3. (Number of cores per perocessor).
	- Network Adapter.  Выбрать тип соединения `NAT: Used to share the hosts IP address` Поставить галочку  на `Connect at power on`. 
	Остальное можно оставить по умолчанию. Жмем кнопку `Ok`. Теперь отображаются актуальные параметры.

Для запуска скрипта прописываем.
```bash
cd Desktop
git clone https://github.com/DemianTarasov/NTO-KvadroKotiki.git
```
Перейдя в проводник, перетащите все файлы из скаченной папки на рабочий стол.

## 2. Настройка симулятора.   

Для настройки симулятора был написан скрипт, который выполняет следующие действия: 
- Скачивает из репозитория [bart02/dronepoint: Dronepoint Gazebo Models](https://github.com/bart02/dronepoint) модели зданий и устанавливает их в необходимую папку `models`.
- Проверяет, существует ли Aruco-карта с тем же названием из файла `clover_aruco.world` в папке `aruco_pose/map`
  - Если карта существует, то скрипт вносит изменения в `aruco.launch`, где в том числе меняет название карты, а также вносит параметр размера маркера из файла карты `.txt`
- Вносит необходимые изменения в файл `clover.launch`.


> [!IMPORTANT]
> Перед настройкой симулятора с помощью скрипта нужно выполнить в терминале команду: 
> ``` bash
>pip install GitPython 
>```
>Данная команда устанавливает модуль для взаимодействия с git-репозиториями. Она необходима, чтобы скачать модели зданий. 

- Файл `launch.py` должен находится на рабочем столе (см. пункт 1 Установка виртуальной машины).
- Вызываем терминал из рабочего стола, либо переходим с помощью команды и вызываем скрипт.
```bash
cd Desktop #Если вы все ещё не находитесь в данной дериктории - перейдите в неё
python3 launch.py
```

Исходный код скрипта c комментариями: 

``` python

from xml.etree import ElementTree as ET  # Импортируем модуль для работы с XML
import git  # Импортируем библиотеку для работы с Git
import shutil  # Импортируем модуль для работы с файлами и директориями

# Определяем пути к различным ресурсам
modelsPath = '/home/clover/catkin_ws/src/clover/clover_simulation/models/'
arucoPath = '/home/clover/catkin_ws/src/clover/clover/launch/aruco.launch'
cloverPath = '/home/clover/catkin_ws/src/clover/clover/launch/clover.launch'
worldPath = '/home/clover/catkin_ws/src/clover/clover_simulation/resources/worlds/clover_aruco.world'
mitPath = '/home/clover/catkin_ws/src/clover/aruco_pose/map/'

# Попытка клонировать репозиторий с моделями из GitHub
try:
    git.Git(modelsPath).clone('https://github.com/bart02/dronepoint.git')  # Клонируем репозиторий
    # Перемещаем модели в нужные директории
    shutil.move(modelsPath + 'dronepoint/dronepoint_blue', modelsPath + 'dronepoint_blue')
    shutil.move(modelsPath + 'dronepoint/dronepoint_green', modelsPath + 'dronepoint_green')
    shutil.move(modelsPath + 'dronepoint/dronepoint_red', modelsPath + 'dronepoint_red')
    shutil.move(modelsPath + 'dronepoint/dronepoint_yellow', modelsPath + 'dronepoint_yellow')
except:
    print('Models already exist')  # Если модели уже существуют, выводим сообщение

# Попытка открыть и обработать файл мира (world)
try:
    root = ET.parse(worldPath)  # Парсим XML файл мира
    world = root.getroot()  # Получаем корневой элемент
    mit = world[0][2][0].text.split('_')  # Извлекаем текст и разбиваем его на части
    f = open(mitPath + mit[1] + '.' + mit[2], 'r')  # Открываем файл карты по извлеченному имени
    length = f.read().split('\n')[1].split('\t')[1]  # Читаем длину из файла карты
except:
    print('Map not found! Run genmap.py, https://clover.coex.tech/en/aruco_map.html#marker-map-definition')  # Выводим сообщение об ошибке
    exit()  # Завершаем выполнение программы

# Обработка файла aruco.launch
root = ET.parse(arucoPath)  # Парсим XML файл aruco
aruco = root.getroot()  # Получаем корневой элемент

# Устанавливаем значения для аргументов в aruco.launch
for i in range(len(root.findall('arg'))):
    if aruco[i].attrib['name'] in ['aruco_detect', 'aruco_map', 'aruco_vpe']:
        aruco[i].attrib['default'] = 'true'  # Устанавливаем значение на true для этих аргументов
    elif aruco[i].attrib['name'] == 'placement':
        aruco[i].attrib['default'] = 'floor'  # Устанавливаем значение ию для размещения
    elif aruco[i].attrib['name'] == 'map':
        aruco[i].attrib['default'] = mit[1] + '.' + mit[2]  # Устанавливаем имя карты
    elif aruco[i].attrib['name'] == 'length':
        aruco[i].attrib['default'] = length  # Устанавливаем длину из файла карты
root.write(arucoPath)  # Записываем изменения обратно в файл aruco.launch

# Обработка файла clover.launch
root = ET.parse(cloverPath)  # Парсим XML файл clover
aruco = root.getroot()  # Получаем корневой элемент

# Устанавливаем значения  для аргументов в clover.launch
for i in range(len(root.findall('arg'))):
    if aruco[i].attrib['name'] in ['simulator', 'web_video_server', 'rosbridge', 'main_camera', 'optical_flow', 'aruco', 'rangefinder_vl53l1x', 'led']:
        aruco[i].attrib['default'] = 'true'  # Устанавливаем значение на true для этих аргументов
    elif aruco[i].attrib['name'] in ['blocks', 'rc']:
        aruco[i].attrib['default'] = 'false'  # Устанавливаем значение на false для этих аргументов

root.write(cloverPath)  # Записываем изменения обратно в файл clover.launch
```

В нашем случае мы будем работать со стандартной картой `cmit.txt`, именно она прописана в мире `clover_aruco.world`, но у вас может быть сгенерирована другая карта. В случае, если в "мозгах" Клевера не будет найден файл карты как в мире, то скрипт предложить сгенерировать вам карту с помощью утилиты `genmap.py` и даст ссылку на конкретный пункт в документации. Вам нужно будет создать такую же карту, как и на поле в симуляции. Соответствие модели карты и ещё описания скрипт не проверяет. 
## 3. Случайная генерация мира.

Случайная генерация мира происходит с помощью скрипта, который прописывает в файл `clover_aruco.world` подключение папок с моделями зданий 


С каждым запуском скрипт генерирует цвета зданий и их расположение случайно. Для генерации цвета используется замена расположения к модели, тем самым каждый раз ссылаясь на одну из четырех моделей.  Расположение генерируется случайно в соответствии с ограничениями задания. 

Применение скрипта: 
- Файл `houses.py` должен находится на рабочем столе (см. пункт 1 Установка виртуальной машины).
- Закройте Gazebo. 
- Откройте терминал и вызовите следующие команды:
```bash
cd Desktop #Если вы все ещё не находитесь в данной дериктории - перейдите в неё
python3 houses.py
```
- Запустите Gazebo 

Исходный код программы с комментариями: 

``` python
import random  # Импортируем модуль random для генерации случайных чисел

# Список доступных цветов для зданий
colors = ['model://dronepoint_yellow',
          'model://dronepoint_red',
          'model://dronepoint_green',
          'model://dronepoint_blue']

# Список возможных позиций (координат) для размещения зданий
poss = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8),
        (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8),
        (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8),
        (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8),
        (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8),
        (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8),
        (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8),
        (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8)]

randPos = []   # Список для хранения случайно выбранных позиций зданий
randColor = [] # Список для хранения случайно выбранных цветов зданий

# Цикл для выбора случайных позиций и цветов для пяти зданий
for i in range(5):
    p = poss[random.randrange(len(poss))] # Выбор случайной позиции из списка
    poss.remove(p)                        # Удаление выбранной позиции из списка возможных
    randColor.append(colors[random.randrange(4)]) # Выбор случайного цвета и сохранения в список
    randPos.append(f"{p[0]} {p[1]}")     # Форматирование позиции в строку и сохрание в список

# Открытие файла для записи настроек мира
world = open('/home/clover/catkin_ws/src/clover/clover_simulation/resources/worlds/clover_aruco.world', 'w')

# Запись содержимого файла
world.write('''<?xml version="1.0" ?>
<sdf version="1.5">
  <world name="NTO">
    <include>
      <uri>model://sun</uri>
    </include>

    <include>
      <uri>model://parquet_plane</uri>
      <pose>0 0 -0.01 0 0 0</pose>
    </include>

    <include>
      <uri>model://aruco_cmit_txt</uri>
    </include>

    <include>
      <name>dronepoint_n1</name>
      <uri>{}</uri>
      <pose>{} 0 0 0 0</pose>
    </include>

    <include>
      <name>dronepoint_n2</name>
      <uri>{}</uri>
      <pose>{} 0 0 0 0</pose>
    </include>

    <include>
      <name>dronepoint_n3</name>
      <uri>{}</uri>
      <pose>{} 0 0 0 0</pose>
    </include>

    <include>
      <name>dronepoint_n4</name>
      <uri>{}</uri>
      <pose>{} 0 0 0 0</pose>
    </include>

    <include>
      <name>dronepoint_n5</name>
      <uri>{}</uri>
      <pose>{} 0 0 0 0</pose>
    </include>

    <scene>
      <ambient>0.8 0.8 0.8 1</ambient>
      <background>0.8 0.9 1 1</background>
      <shadows>false</shadows>
      <grid>false</grid>
      <origin_visual>false</origin_visual>
    </scene>
  
    <physics name='default_physics' default='0' type='ode'>
      <gravity>0 0 -9.8066</gravity>
      <ode>
        <solver>
          <type>quick</type>
          <iters>10</iters>
          <sor>1.3</sor>
          <use_dynamic_moi_rescaling>0</use_dynamic_moi_rescaling>
        </solver>
        <constraints>
          <cfm>0</cfm>
          <erp>0.2</erp>
          <contact_max_correcting_vel>100</contact_max_correcting_vel>
          <contact_surface_layer>0.001</contact_surface_layer>
        </constraints>
      </ode>
      <max_step_size>0.004</max_step_size>
      <real_time_factor>1</real_time_factor>
      <real_time_update_rate>250</real_time_update_rate>
      <magnetic_field>6.0e-6 2.3e-5 -4.2e-5</magnetic_field>
    </physics>
  </world>
</sdf>

'''.format(
    randColor[0], randPos[0],   # Форматирование данных для первого здания
    randColor[1], randPos[1],   # Форматирование данных для второго здания
    randColor[2], randPos[2],   # Форматирование данных для третьего здания
    randColor[3], randPos[3],   # Форматирование данных для четвертого здания
    randColor[4], randPos[4]    # Форматирование данных для пятого здания
))

world.close() # Закрытие файла после записи
```

## 4. Полетная миссия 

Полетная миссия представляет из себя полет дрона из точки `(0, 0)` траекторией "змейка". Происходит сканирование каждого ArUco-маркера на наличие здания. Как только крыша здания будет находится в центре кадра камеры, то программа определит цвет, тип и координаты здания.  Отладочную информацию можно увидеть в терминале, откуда происходит запуск ноды, а также информацию о типах здания можно увидеть, подписавшись на топик `/buldings.
`
> [!IMPORTANT]
> Перед запуском полетной миссии нужно выполнить в терминале команду: 
> ``` bash
>pip install Flask==2.2.2
>```
>Данная команда устанавливает более новую версию модуля Flask. Он необходим для работы веб-сервиса. 

- Файл `colour_vse.py` должен находится на рабочем столе (см. пункт 1 Установка виртуальной машины).
- Создайте терминал. В данном терминале мы будем запускать миссию. и наблюдать за отладочной информацией.
- Откройте Gazebo. 
- Введите в терминале следующие команды:
```bash
cd Desktop #Если вы все ещё не находитесь в данной дериктории - перейдите в неё
python3 colour_vse.py
```
Миссия запущенна. Начать полет можно в веб сервисе (см. пункт 5. Работа с веб-сервисом).
> [!IMPORTANT]
> Полная остановка кода осуществляется через закрытие окна терминала.

Также возможен просмотр топика.
- Запустите ещё один терминал и введите следующую команду, чтобы подписаться на топик `/buildings`: 
```bash
rostopic echo /buildings
```
В случае нахождения здания в данный топик будет публиковаться информация о цвете, типе здания и его координатах.

Исходный код программы с комментариями: 
```python
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np
import math
from clover import srv
from std_srvs.srv import Trigger
from std_msgs.msg import String
from server import Server
from threading import Thread
from mavros_msgs.srv import CommandBool

# Инициализация сервера управления
server = Server

# Инициализация ROS-ноды
rospy.init_node('flight')

# Создание топика для публикации информации о зданиях
buildings = rospy.Publisher('/buildings', String, queue_size=1)

# Прокси для вызова сервисов Clover
get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
land = rospy.ServiceProxy('land', Trigger)
arming = rospy.ServiceProxy('mavros/cmd/arming', CommandBool)

# Создание объекта для преобразования изображений из ROS в OpenCV
bridge = CvBridge()

# Функция навигации с ожиданием достижения цели
def navigate_wait(x=0, y=0, z=0, yaw=float('nan'), speed=0.4, frame_id='', auto_arm=False, tolerance=0.2):
    navigate(x=x, y=y, z=z, yaw=yaw, speed=speed, frame_id=frame_id, auto_arm=auto_arm)

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            break
        rospy.sleep(0.2)


# Обработчик изображения для определения цвета зданий
def image_callback_color():
    img = bridge.imgmsg_to_cv2(rospy.wait_for_message('main_camera/image_raw', Image), 'bgr8') # Получение изображения
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # Преобразование изображения в HSV
    telemet = get_telemetry(frame_id='aruco_map') # Получение телеметрии для координат
    
    # Задание границ цветов для определения зданий
    red_high= (15, 255, 255)   
    red_low= (0, 240, 240)

    blue_high= (122, 255, 255)  
    blue_low= (110, 245, 245)

    green_high= (62, 255, 255)  
    green_low= (55, 247, 250)

    yellow_high= (35, 255, 255)  
    yellow_low= (25, 245, 250)
    
    # Создание масок для каждого цвета
    red_mask = cv2.inRange(img_hsv, red_low, red_high)
    blue_mask = cv2.inRange(img_hsv, blue_low, blue_high)
    green_mask = cv2.inRange(img_hsv, green_low, green_high)
    yellow_mask = cv2.inRange(img_hsv, yellow_low, yellow_high)
    
    # Определение цвета в центре изображения и публикация информации в топик и на веб-сервер
    if red_mask[119][159] == 255:
        server.buildings.append([round(telemet.x), round(telemet.y), 'red'])
        print("administration building; red at x: " + str(round(telemet.x)) + ", y: " + str(round(telemet.y)))    
        buildings.publish(data = ("administration building; red at x: " + str(round(telemet.x)) + ", y: " + str(round(telemet.y))))    

    elif blue_mask[119][159] == 255:
        server.buildings.append([round(telemet.x), round(telemet.y), 'blue'])
        print("coal enrichment building; blue at x: " + str(round(telemet.x)) + ", y: " + str(round(telemet.y)))
        buildings.publish(data = ("coal enrichment building; blue at x: " + str(round(telemet.x)) + ", y: " + str(round(telemet.y))))
    elif green_mask[119][159] == 255:
        server.buildings.append([round(telemet.x), round(telemet.y), 'green'])
        print("laboratory; green at x: " + str(round(telemet.x)) + ", y: " + str(round(telemet.y)))
        buildings.publish(data = ("laboratory; green at x: " + str(round(telemet.x)) + ", y: " + str(round(telemet.y))))
    elif yellow_mask[119][159] == 255:
        server.buildings.append([round(telemet.x), round(telemet.y), 'yellow'])
        print("entrance to the mine; yellow at x: " + str(round(telemet.x)) + ", y: " + str(round(telemet.y)))
        buildings.publish(data = ("entrance to the mine; yellow at x: " + str(round(telemet.x)) + ", y: " + str(round(telemet.y))))

# Проверка на остановку и возобновление полета
def checkStop():
    stoped = False
    if (server.action != 'start'):
        land() # Приземление, если полет остановлен
        stoped = True
        if(server.action == 'kill'): # Завершение программы, если команда "kill switch"
            print('Killed')
            exit()
        rospy.sleep(10)
        print('Disarmed, can start again')
        server.action = 'landed'
    while (server.action != 'start'): # Ожидание возобновления полета
        if(server.action == 'kill'): # Завершение программы, если команда "kill switch"
            print('Killed')
            exit()
        pass
    if (stoped): # Возобновление полета
        print('Started again')
        navigate(x=0, y=0, z=1.7, speed=0.5, frame_id='body', auto_arm=True)
        rospy.sleep(5)

# Основная функция управления дроном
def main():
    while (server.action != 'start'): # Ожидание возобновления полета
        if(server.action == 'kill'): # Завершение программы, если команда "kill switch"
            print('Killed')
            exit()
        pass
    # Начало полёта
    print('Start fly')
    navigate(x=0, y=0, z=1.7, speed=0.5, frame_id='body', auto_arm=True)
    rospy.sleep(7)
    teleme = get_telemetry(frame_id='aruco_map')
    startx = round(teleme.x)
    starty = round(teleme.y)

    # Сканирование территории
    for y1 in range(10): # Поочередное движение по сетке
        if y1 % 2==0:
            for x1 in range(10):
                checkStop()
                navigate_wait(x = x1, y = y1, z = 1.7, frame_id='aruco_map')
                rospy.sleep(1)
                image_callback_color()
                rospy.sleep(2)
        else:
            for x1 in range(9, -1, -1):
                checkStop()
                navigate_wait(x = x1, y = y1, z = 1.7, frame_id='aruco_map')
                rospy.sleep(1)
                image_callback_color()
                rospy.sleep(2)
                
    # Возврат на стартовую позицию
    x1, y1 = 0, 9
    while (x1 > startx or y1 > starty):
        x1 -= x1 > startx
        y1 -= y1 > starty
        checkStop()
        navigate_wait(x = x1, y = y1, z = 1.7, frame_id='aruco_map')
        rospy.sleep(1.5)
    
    land() # Приземление по завершении работы
    print('End program')
    exit()

# Запуск основной функции в отдельном потоке
th = Thread(target=main)
th.start()

# Запуск веб-сервиса
server.start()
```
## 5. Работа с веб-сервисом 

Веб-сервис позволяет нам контролировать полёт дрона.
- Перед открытием веб-сервиса необходимо запустить полетную миссию (см. пункт 4. Полетная миссия).
- Откройте браузер.
- В поисковой строке введите адрес http://localhost:4000/

<img src="/web-service.png" style="width:50%; height:auto;">

В веб-сервисе можно наблюдать 2d карту, с началом координат в левом нижнем углу. На данной карте отображаются все найденые дома с обозначением его координат и цвета. Каждый квадрат на карте соответствует 1м в симуляторе. Для того чтобы не нагружать систему дрона, расположение домов обновляется каждые 100мс.

Ниже карты имеются кнопки управления, а также подпись последнего действия (изначально `Landed`). 
- Если была нажата кнопка `Start`, то дрон начнёт или продолжит с последнего шага свой полет. Доступны последующие кнопки `Stop` и `Kil switch`. Действие `Started`.
- Если была нажата кнопка `Stop`, то дрон будет посажен. Доступна последующая кнопка `Start` (только после полной посадки). Действие `Landed`.
- Если была нажата кнопка `Kill switch`, то дрон опустится на землю, а код будет прерван. Никакие последующие кнопки не доступны. Действие `Killed`.

> [!IMPORTANT]
> Команда `Kill switch` прерывает работу кода, но полное отключение осуществляется через закрытие окна терминала.

> [!IMPORTANT]
> Посадка дрона осуществляется только на поверхность пола. Если посадить дрон на дом, то сработает `Failsafe` из-за не верной поверхности и не возможно будет взлететь.

Также чуть ниже в веб-сервисе представлен список найденых зданий с указанием их цвета, координат и типа.

Исходный код веб-сервиса с комментариями: 

```python
from flask import Flask, request, jsonify

# Инициализация приложения Flask
app = Flask(__name__)

# Создание класса Server, для хранения функций и переменных веб-сервиса
class Server:
  action = 'landed' # Текущее состояние, по умолчанию "landed"
  buildings = [] # Список зданий на "карте"
  
  # Эндпоинт для обновления текущего состояния сервера
  @app.route('/action', methods=['POST'])
  def actPage():
    Server.action = request.json['action'] # Установка нового состояния из запроса
    return '' # Пустой ответ
  
  # Эндпоинт для получения текущего состояния и списка зданий
  @app.route('/buildings')
  def positionsPage():
    return [Server.action, Server.buildings] # Возвращает состояние и список зданий
  
  # Главная страница, генерирует HTML-код с интерфейсом
  @app.route('/')
  def actionPage():
    return '''
  <div style="text-align:center">
    <!-- Основной блок с отображением карты и кнопок управления -->
    <div style="display:flex; flex-direction:column;">
      
      <div id="map" style="position:relative; margin: auto">
        <!-- Карта, состоящая из ячеек -->
        <span style="position:absolute; left: -15px; bottom: -5px; font-size: 20px"> 0</span>
        
        <div id="building0" style="display:none; position:absolute; width:50px; height:50px; text-align:center;">
        </div>
        <div id="building1" style="display:none; position:absolute; width:50px; height:50px; text-align:center;">
        </div>
        <div id="building2" style="display:none; position:absolute; width:50px; height:50px; text-align:center;">
        </div>
        <div id="building3" style="display:none; position:absolute; width:50px; height:50px; text-align:center;">
        </div>
        <div id="building4" style="display:none; position:absolute; width:50px; height:50px; text-align:center;">
        </div>
        
      </div>
      
      
        
    </div>
    <div style="margin-top: 20px">
        <!-- Кнопки управления -->
        <button id="start-button" type="button" style="dislay:block; color:green">Start</button>
        <button id="stop-button" type="button" style="dislay:block; color:red">Stop</button>
        <button id="kill-button" type="button" style="dislay:block; color:red">Kill switch</button>
    </div>
    <span id="message"></span>
    <span id="buildings"></span>
  </div>

  <script>
    // Код JavaScript, управляющий отображением карты и обработкой кнопок
    
    // При загрузке страницы создаётся карта и запускается обновление зданий
    document.body.onload = () => {createMap(); setInterval(updateBuildings, 100);};
    
    // Обработчики для кнопок
    document.getElementById("start-button").addEventListener("click", startClick);
    document.getElementById("stop-button").addEventListener("click", stopClick);
    document.getElementById("kill-button").addEventListener("click", killClick);
    
    let startStatus = "''' + Server.action + '''"; // Хранит текущее состояние
    
    // Обновляет информацию о зданиях на карте
    function updateBuildings(){
      fetch("/buildings", {
        method: "GET",
        headers: {"Content-type": "application/json"}
      })
      .then(response => response.json())
      .then(json => {
        let bs = document.getElementById("buildings");
        bs.innerHTML = "";
        if(json[0] == "landed" && startStatus == "landing"){ // Обработка посадки
          startStatus = json[0];
          document.getElementById("start-button").style.color = "green";
          document.getElementById("stop-button").style.color = "red";
          document.getElementById("kill-button").style.color = "green";
          document.getElementById("message").innerHTML = "Landed";
        }
        for(let i = 0; i < json[1].length; i++){
          let b = document.getElementById("building" + i.toString());
          b.style.display = "block"
          b.style.left = json[1][i][0] * 50 + 2 * json[1][i][0] - 24
          b.style.bottom = json[1][i][1] * 50 + 2 * json[1][i][1] - 24
          b.style.background = (json[1][i][2] == "yellow"?"#e6db00":json[1][i][2])
          b.innerHTML = "<span style=\\"color:white\\">x: " + json[1][i][0] + "</span><br/><span style=\\"color:white\\">y: " + json[1][i][1] + "</span>";
          bs.innerHTML = bs.innerHTML + "<br/>" + (json[1][i][2]=="red"?"Администрация":(json[1][i][2]=="green"?"Лаборатория":(json[1][i][2]=="yellow"?"Шахта":"Здание для обогащения угля"))) + "; color: " + json[1][i][2] + "; x: " + json[1][i][0] + "; y: " + json[1][i][1];
        }
      });
    }
    
    // Создаёт карту (9x9 ячеек)
    function createMap() {
      let map = document.getElementById('map');
      document.getElementById("start-button").style.color = "'''+('green' if Server.action == 'landed' else 'red') + '''";
      document.getElementById("stop-button").style.color = "'''+('green' if Server.action == 'start' else 'red') + '''";
      document.getElementById("kill-button").style.color = "'''+('green' if Server.action != 'kill' else 'red') + '''";
      document.getElementById("message").innerHTML = "''' + ('Landed' if Server.action == 'landed' else ('Landing' if Server.action == 'landing' else ('Started' if Server.action == 'start' else 'Killed'))) + '''";

      for (let i = 0; i < 9; i++) {
        let row = document.createElement('div');
        row.style = 'display: flex; justify-content:center';
        for (let i = 0; i < 9; i++) {
          let col = document.createElement('div');
          col.style = 'width:50px; height:50px; border:solid 1px gray';
          row.appendChild(col);
        }
        map.appendChild(row);
      }
    }
    
    // Логика обработки кнопки "Start"
    function startClick() {
      if(startStatus == "start" || startStatus == "kill"|| startStatus == "landing"){
        return
      }
      fetch("/action", {
        method: "POST",
        body:JSON.stringify({action:"start"}),
        headers: {"Content-type": "application/json"}
      })
      document.getElementById("start-button").style.color = "red";
      document.getElementById("stop-button").style.color = "green";
      document.getElementById("kill-button").style.color = "green";
      document.getElementById("message").innerHTML = "Started";
      startStatus = "start";
    }
    
    // Логика обработки кнопки "Stop"
    function stopClick() {
      if(startStatus == "landed" || startStatus == "kill" || startStatus == "landing"){
        return
      }
      fetch("/action", {
        method: "POST",
        body:JSON.stringify({action:"landing"}),
        headers: {"Content-type": "application/json"}
      })
      document.getElementById("start-button").style.color = "red";
      document.getElementById("stop-button").style.color = "red";
      document.getElementById("kill-button").style.color = "red";
      document.getElementById("message").innerHTML = "Landing";
      startStatus = "landing";
    }
    
    // Логика обработки кнопки "Kill"
    function killClick() {
      if(startStatus == "kill" || startStatus == "landing"){
        return
      }
      fetch("/action", {
        method: "POST",
        body:JSON.stringify({action:"kill"}),
        headers: {"Content-type": "application/json"}
      })
      document.getElementById("start-button").style.color = "red";
      document.getElementById("stop-button").style.color = "red";
      document.getElementById("kill-button").style.color = "red";
      document.getElementById("message").innerHTML = "Killed";
      startStatus = "kill";
    }
    
  </script>
  '''
  
  # Метод для запуска сервера
  def start():
    app.run(host='0.0.0.0', port='4000') # Сервер доступен на порту 4000

```