from random import randint, choice
import pandas as pd
from skimage.io import imshow, imread
import matplotlib.pyplot as plt

def create_airplanes_floor(dict_floor_queues, dict_available_spaces): #creating airplanes to floor queues
  '''
  if the airplane is already on queue, and new ones are added, it means that in a round it doesn't move.
  So there's added one more unit of time to the airplane. 
  '''
  for queue in dict_floor_queues:
    for airplane in dict_floor_queues[queue]:
      dict_floor_queues[queue][airplane]['Time To Take Off'] += 1

  #Queues must be consulted
  for queue in dict_floor_queues:
    airplanes_on_queue = len(dict_floor_queues[queue])
    available_queues_spaces = dict_available_spaces[airplanes_on_queue]

    #TO ID
    letters = 'ABCDEFGIJKLMNOPQSTUVWXYZ'
    numbers = '123456789'

    #the random number of airplanes must be between zero and the maximum of spaces available on the queues
    number_of_airplanes = randint(0,available_queues_spaces) 
    for i in range(number_of_airplanes):
      ID = [choice(letters) for x in range(3)] + [choice(numbers) for x in range(3)] 
      ID = ''.join(ID)

      while (ID in dict_floor_queues[queue]):
        ID = [choice(letters) for x in range(3)] + [choice(numbers) for x in range(3)] 
        ID = ''.join(ID)

      time_to_take_off = 0
      airplane_fuel = randint(2,20)
      dict_airplane = {'Time To Take Off':time_to_take_off, 'Fuel':airplane_fuel}
      dict_floor_queues[queue][ID] = dict_airplane

  return dict_floor_queues

def enter_runway(dict_runways, dict_floor_queues, dict_runway_to_queue, dict_available_spaces):
  '''
  if the airplane is already on runway, and new ones are added, it means that in a round the airplane doesn't move.
  So there's added one more unit of time to the airplane. 
  '''
  for runway in dict_runways:
    for airplane in dict_runways[runway]:
      dict_runways[runway][airplane]['Time To Take Off'] += 1

  #Runways must be consulted
  list_airplanes_out_of_runway = []
  for runway in dict_runways:
    list_airplanes_in_queues = list(dict_floor_queues[dict_runway_to_queue[runway]].keys())
    airplanes_on_runway = len(dict_runways[runway])
    available_runways_spaces = dict_available_spaces[airplanes_on_runway]


    for ID in dict_floor_queues[dict_runway_to_queue[runway]]:
      #Adding new airplanes while there's still spaces available on runways
        if (available_runways_spaces > 0):
          airplane_to_runway = list_airplanes_in_queues[0]
          list_airplanes_out_of_runway.append(airplane_to_runway)
          dict_runways[runway][ID]= dict_floor_queues[dict_runway_to_queue[runway]][ID]
          list_airplanes_in_queues.remove(airplane_to_runway)
          available_runways_spaces -= 1
  
  '''
  Once the airplane is added to the runways, it must be removed from the floor queues.
  '''
  for runway in dict_runways:
    for airplane in list_airplanes_out_of_runway:
      if (airplane in dict_floor_queues[dict_runway_to_queue[runway]]):
        dict_floor_queues[dict_runway_to_queue[runway]].pop(airplane)

  return dict_runways

def takeoff(dict_runways, dict_runway_to_queue):
    '''
    for each round, the first airplane to enter in respective runway is gonna be the one that flies.
    '''
    dict_airplanes_to_take_off = {'runway_1':{}, 'runway_2':{}, 'runway_3':{}} 
    list_airplanes_take_off = []

    #Checking runways
    for runway in dict_runways:
        list_airplanes_in_runway = list(dict_runways[runway].keys())
        if (len(list_airplanes_in_runway)!=0):
            airplane_to_take_off =  list_airplanes_in_runway[0]
            list_airplanes_take_off.append(airplane_to_take_off)
            dict_airplanes_to_take_off[runway][airplane_to_take_off] = dict_runways[runway][airplane_to_take_off]

    
    #Once the airplane took off, it must be removed from the runway.
    for runway in dict_runways:
      for airplane in list_airplanes_take_off:
        if (airplane in dict_runways[runway]):
          dict_runways[runway].pop(airplane)
    return dict_airplanes_to_take_off
        

def create_airplanes_sky(dict_sky_queues, dict_available_spaces):
    '''
    Once the airplane is already on the queue and new airplanes are added, it means
    that in a round the airplane doesn't move 
    '''
    for queue in dict_sky_queues:
      for airplane in dict_sky_queues[queue]:
        dict_sky_queues[queue][airplane]['Time To Land'] += 1
        dict_sky_queues[queue][airplane]['Fuel'] -= 1
  
  #Queues must be consulted
    for queue in dict_sky_queues:
        airplanes_on_queue = len(dict_sky_queues[queue])
        available_queues_spaces = dict_available_spaces[airplanes_on_queue]

        #TO ID
        letters = 'ABCDEFGIJKLMNOPQSTUVWXYZ'
        numbers = '123456789'
        
        number_of_airplanes = randint(0,available_queues_spaces)
        for i in range(number_of_airplanes): 
          ID = [choice(letters) for x in range(3)] + [choice(numbers) for x in range(3)] 
          ID = ''.join(ID)

          while (ID in dict_sky_queues[queue]):
              ID = [choice(letters) for x in range(3)] + [choice(numbers) for x in range(3)] 
              ID = ''.join(ID)

          time_to_land = 0
          airplane_fuel = randint(2,20)
          dict_airplane = {'Time To Land':time_to_land, 'Fuel':airplane_fuel}
          dict_sky_queues[queue][ID] = dict_airplane
    return dict_sky_queues
        

def landing(dict_runways, dict_sky_queues, dict_runway_to_queue, dict_queue_to_runway, emergency_landings, airplane_crash):
    dict_airplanes_normal_landings = {'runway_1':{}, 'runway_2':{}, 'runway_3':{}}
    dict_airplanes_on_emergency_landings = {'runway_1':{}, 'runway_2':{}, 'runway_3':{}}
    dict_crashed_airplanes = {'queue_1':{}, 'queue_2':{}, 'queue_3':{}}
    list_queues = [queue for queue in dict_sky_queues]
    for queue in dict_sky_queues:
        for airplane in dict_sky_queues[queue]:
          if(dict_sky_queues[queue][airplane]['Fuel']==1): #emergency landings 
            verify_airplane = True
            i = 0
            while verify_airplane == True: #this while runs through the sky queues one and two
                if (i<2):
                  #if one of the runways 1 or 2 is available to the emergency landing, the airplane is sent it
                  if (len(dict_airplanes_on_emergency_landings[dict_queue_to_runway[list_queues[i]]].keys())==0):
                    dict_airplanes_on_emergency_landings[dict_queue_to_runway[list_queues[i]]][airplane] = dict_sky_queues[queue][airplane]
                    emergency_landings += 1
                    verify_airplane = False
                  else:
                    i += 1
              
                # if i==2 it means that none of runways 1 or 2 is available to the emergency landing, so the airplane is sent to runway 3
                elif (i==2):
                  if (len(dict_airplanes_on_emergency_landings['runway_3'].keys())==0):
                    dict_airplanes_on_emergency_landings['runway_3'][airplane] = dict_sky_queues[queue][airplane]
                    verify_airplane = False
                  else:
                    #if none of runways 1, 2 or 3 is available, the airplane crash
                    airplane_crash += 1
                    dict_crashed_airplanes[queue][airplane] = dict_sky_queues[queue][airplane]
                    verify_airplane = False
              
          else: #regular landing
            if (len(dict_airplanes_normal_landings[dict_queue_to_runway[queue]].keys())==0):
              dict_airplanes_normal_landings[dict_queue_to_runway[queue]][airplane] = dict_sky_queues[queue][airplane]

    #removing crashed airplanes from sky queues 
    for queue in dict_crashed_airplanes:
      for airplane in dict_crashed_airplanes[queue]:
          if (airplane in dict_sky_queues[queue]):
            dict_sky_queues[queue].pop(airplane)

    #removing airplanes on emergency landings from sky queues 
    for runway in dict_airplanes_on_emergency_landings:
      for airplane in dict_airplanes_on_emergency_landings[runway]:
        for queue in dict_sky_queues:
          if (airplane in dict_sky_queues[queue]):
            dict_sky_queues[queue].pop(airplane)

    #removing airplanes on normal landings from sky queues 
    for runway in dict_airplanes_normal_landings:
      for airplane in dict_airplanes_normal_landings[runway]:
        for queue in dict_sky_queues:
          if (airplane in dict_sky_queues[queue]):
            dict_sky_queues[queue].pop(airplane)
        
    return dict_crashed_airplanes, dict_airplanes_on_emergency_landings, dict_airplanes_normal_landings


def format_line_name(line_name:str):
  #formatting the line name (runways and queues)
  name = line_name.split('_')[0].title()
  number = line_name.split('_')[1]

  output = [name, ' ',number]

  return ''.join(output)

def df_to_print(dictionary, round_of_execution):
  #this function creates a DataFrame from the dictionary
  rounds = []
  lines = []
  airplanes = []
  times = []
  fuels = []
  for line in dictionary:
    for airplane in dictionary[line]:
      rounds.append(round_of_execution)
      line_name = format_line_name(line)
      lines.append(line_name)
      airplanes.append(airplane)
      fuel = dictionary[line][airplane]['Fuel']
      fuels.append(fuel)
      if ('runway_1' in dictionary):
        if ('Time To Take Off' in dictionary[line][airplane].keys()):
          time = dictionary[line][airplane]['Time To Take Off']
          times.append(time)
        else:
           time = dictionary[line][airplane]['Time To Land']
           times.append(time) 
      else: 
        if ('Time To Take Off' in dictionary[line][airplane].keys()):
          time = dictionary[line][airplane]['Time To Take Off']
          times.append(time)
        else:
           time = dictionary[line][airplane]['Time To Land']
           times.append(time)
    
  df = pd.DataFrame()
  df= df.assign(ROUND=rounds).assign(AIRPLANE=airplanes).assign(LINE=lines).assign(TIME=times).assign(FUEL=fuels)

  return df

round_of_execution = 0

def output_generator(final_output_json, key, dict_name, dictionary, all_df, round_of_execution=round_of_execution):
  #exhibition of the dataframe 
  df = df_to_print(dictionary, round_of_execution)
  N_SPACES = 5
  head = '\n'+'--'*N_SPACES + ' '+ dict_name + ' '+'--'*N_SPACES
  print('\n')
  print(head)
  print('\n')
  if (len(df.index)!=0):
    print(df)
  else:
    print('')
  all_df.append(pd.DataFrame([{'AIRPLANE': dict_name}]))
  all_df.append(df)
  final_output_json[key][dict_name] = dictionary

def save_imgs(list_imgs, number_of_imgs, names_imgs):
  for i in range(number_of_imgs):
    img = imread(f'{names_imgs}_{i}.png')
    list_imgs.append(img)

runways_imgs =[]
queues_imgs =[]
taking_off_imgs = []
crashed_airplanes_imgs = []
emergency_landings_imgs = []
landings_imgs = []

save_imgs(runways_imgs, 4, 'runway')
save_imgs(queues_imgs, 4, 'queue')
save_imgs(taking_off_imgs, 2, 'taking_off')
save_imgs(crashed_airplanes_imgs, 2, 'crashed_airplane')
save_imgs(emergency_landings_imgs, 2, 'emergency_landing')
save_imgs(landings_imgs, 2, 'landing')

def open_image(dict_name, dictionary, list_imgs, show_image):
  if (show_image == True):
    name_to_display = {'FLOOR QUEUES':' FLOOR QUEUE', 'RUNWAYS': 'RUNWAY', 'TAKING OFF':'TAKING OFF', 'SKY QUEUES':'SKY QUEUE',\
                      'CRASHED AIRPLANES':'CRASHED AIRPLANE', 'EMERGENCY LANDINGS':'EMERGENCY LANDING', 'LANDINGS':'LANDING'}

    spaces = 10-len(name_to_display[dict_name])

    plt.figure(figsize=(4.5, 4.5))
    i = 0
    for line in dictionary: 
      number_of_airplanes = len(dictionary[line])
      img = list_imgs[number_of_airplanes]
      plt.subplot(3, 3, i+1)
      plt.imshow(img)
      plt.axis('off')
      i += 1

      plt.tight_layout()
    return plt.show()
    

