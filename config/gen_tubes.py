import random  # Импортируем модуль random для генерации случайных чисел
import math

# Список доступных цветов для зданий
main_tube = 'model://main_tube'
tube = 'model://tube'

poss = [random.randint(0,16)/100 +1]
#[f"{1+i*0.5} 4", ["1.57", "-1.57"]] for i in range(1, 9)] + [[f"{round(5+ i*0.5*math.cos(30*math.pi/180), 2)} {round(4-i*0.5*math.sin(30*math.pi/180), 2)}", ["1.05", "-2.09"]] for i in range(1, 9)]

randPos = []   # Список для хранения случайно выбранных позиций зданий
randTurn = [] # Список для хранения случайно выбранных цветов зданий

randPos.append(f"{poss[0]} 4")
randTurn.append(1.57)
print(0, randPos[len(randPos)-1], randTurn[len(randTurn)-1])



# Цикл для выбора случайных позиций и цветов для пяти зданий
pold = 0
i = 4
while(i):
    p = random.randint(int((poss[4-i]+0.75)*100), ((4-i)+2)*160 +1)/100 # Выбор случайной позиции из списка
    if p<5:
      poss.append(p)                        # Удаление выбранной позиции из списка возможных
      randPos.append(f"{p} 4")     # Форматирование позиции в строку и сохрание в список
      if random.randint(0,1):
        randTurn.append(90*math.pi/180) # Выбор случайного цвета и сохранения в список
      else:
         randTurn.append(270*math.pi/180) # Выбор случайного цвета и сохранения в список
      pold = p
      i = i-1
      print(i +1, randPos[len(randPos)-1], randTurn[len(randTurn)-1])
    else:
      pp = (p - 5) / math.cos(30*math.pi/180)
      if (pold < 5 and (((pp+5 - pold)**2 + (pp*math.sin(30*math.pi/180))**2)**0.5 > 0.75)) or pold > 5:
        poss.append(pp+5)
        randPos.append(f"{pp+5} {4-pp*math.sin(30*math.pi/180)-0.15}")
        if random.randint(0,1):
          randTurn.append(90*math.pi/180 -30*math.pi/180) # Выбор случайного цвета и сохранения в список
        else:
          randTurn.append(270*math.pi/180 -30*math.pi/180) # Выбор случайного цвета и сохранения в список
        pold = pp
        i = i-1
        print(i +1, randPos[len(randPos)-1], randTurn[len(randTurn)-1])
    

# Открытие файла для записи настроек мира
world = open('/home/clover/catkin_ws/src/clover/clover_simulation/resources/worlds/clover_aruco.world', 'w')

# Запись содержимого файла
world.write(f'''<?xml version="1.0" ?>
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
      <name>main_tube</name>
      <uri>{main_tube}</uri>
      <pose>1 4 0 0 0 1.57</pose>
    </include>

    <include>
      <name>tube_n1</name>
      <uri>{tube}</uri>
      <pose>{randPos[0]} 0 0 0 {randTurn[0]}</pose>
    </include>
    <include>
      <name>tube_n2</name>
      <uri>{tube}</uri>
      <pose>{randPos[1]} 0 0 0 {randTurn[1]}</pose>
    </include>
    <include>
      <name>tube_n3</name>
      <uri>{tube}</uri>
      <pose>{randPos[2]} 0 0 0 {randTurn[2]}</pose>
    </include>
    <include>
      <name>tube_n4</name>
      <uri>{tube}</uri>
      <pose>{randPos[3]} 0 0 0 {randTurn[3]}</pose>
    </include>
    <include>
      <name>tube_n5</name>
      <uri>{tube}</uri>
      <pose>{randPos[4]} 0 0 0 {randTurn[4]}</pose>
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

''')

world.close() # Закрытие файла после записи
