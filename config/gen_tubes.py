import random  # Импортируем модуль random для генерации случайных чисел
import math

#Импорт моделей труб
main_tube = 'model://main_tube'
tube = 'model://tube'

poss = [random.randint(0,16)/100 +1]    #Выбираем случайную позицию для первой врезки между 0 и 8/5 длины трубы(чтобы точно хватило места для 5 врезок) 
randPos = [] 
randTurn = []

randPos.append(f"{poss[0]:.3f} 1.000")    #Создаем первую врезку
randTurn.append(1.57)

pold = 0
i = 4
while(i):
    p = random.randint(int((poss[4-i]+0.75)*100), ((4-i)+2)*160 +1)/100   #Выбираем позицию для следующей рейки, отступая 0,75 от предыдущей
    if p<5:   #Если выбрали позицию на превой половине трубы (до изгиба), то записываем позицию без изменений
      poss.append(p)
      randPos.append(f"{p:.3f} 1.000")
      if random.randint(0,1):
        randTurn.append(90*math.pi/180)   #Выбираем с какой стороны трубы будет врезка (справа/слева)
      else:
         randTurn.append(270*math.pi/180)
      pold = p
      i = i-1
    else:   #Если же выбранная позиция на второй половине трубы, то конвертируем координаты трубы из одномерной системы в двумерную
      pp = (p - 5)
      if (pold < 5 and (((pp*math.cos(30*math.pi/180)+5-pold)**2 + (pp*math.cos(30*math.pi/180)*math.tan(30*math.pi/180))**2)**0.5)>0.75) or pold > 5:    #Проверяем, что расстояние между предыдущей врезкой (если она была до изгиба трубы) и создаваемой не меньше 0.75
        poss.append(p)
        randPos.append(f"{(pp*math.cos(30*math.pi/180)+5):.3f} {(1+pp*math.cos(30*math.pi/180)*math.tan(30*math.pi/180)):.3f}")
        if random.randint(0,1):
          randTurn.append(90*math.pi/180 +30*math.pi/180)     #Выбираем с какой стороны трубы будет врезка (справа/слева)
        else:
          randTurn.append(270*math.pi/180 +30*math.pi/180)
        pold = pp
        i = i-1
    

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
      <pose>1 1 0 0 {1.57*2} 1.57</pose>
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
