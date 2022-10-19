from random import choice, randint
from time import sleep
import datetime
from aya_functions import *

global dict_floor_queues #waiting queues to enter the runways
dict_floor_queues = {'queue_1':{}, 'queue_2':{}, 'queue_3':{}}

global dict_sky_queues #waiting queues to enter the runways
dict_sky_queues = {'queue_1':{}, 'queue_2':{}}

global dict_runways #airplane runways
dict_runways = {'runway_1':{}, 'runway_2':{}, 'runway_3':{}}

global dict_available_spaces
dict_available_spaces = {0:3,1:2,2:1,3:0} #parameterizing queues availability 

global dict_runway_to_queue #relating queues to runways
dict_runway_to_queue = {'runway_1':'queue_1','runway_2':'queue_2','runway_3':'queue_3'}

global dict_queue_to_runway #relating runways to queues
dict_queue_to_runway = {'queue_1':'runway_1','queue_2':'runway_2','queue_3':'runway_3'}

global global_dict_crashed_airplanes
global_dict_crashed_airplanes = {}
global_dict_crashed_airplanes['CURRENT TIME'] = {}

global airplane_crash #number of airplanes crashing
airplane_crash = 0

global emergency_landings #number of emergency landings
emergency_landings = 0


print('Welcome to AYA Airport!\n')

all_dicts_names = ['FLOOR QUEUES', 'RUNWAYS','TAKING OFF', 'SKY QUEUES','CRASHED AIRPLANES', 'EMERGENCY LANDINGS', 'LANDINGS']
moment_of_execution = str(datetime.datetime.now())
final_output_json = {'CURRENT TIME': {}}
all_df = []
SLEEP_TIME = 2
show_image = False
NUMBER_OF_ROUNDS = 4

for round_of_execution in range(NUMBER_OF_ROUNDS):
  N_SPACES = 5

  final_output_json[f'ROUND {round_of_execution}'] = {}
  dict_floor_queues = create_airplanes_floor(dict_floor_queues=dict_floor_queues, dict_available_spaces=dict_available_spaces)
  open_image(dict_name=all_dicts_names[0], dictionary=dict_floor_queues, list_imgs=queues_imgs, show_image=show_image)
  output_generator(final_output_json=final_output_json, key='CURRENT TIME', dict_name=all_dicts_names[0], dictionary=dict_floor_queues, all_df=all_df)
  sleep(SLEEP_TIME)
  #output.clear()

  dict_runways = enter_runway(dict_runways=dict_runways, dict_floor_queues=dict_floor_queues,\
                              dict_runway_to_queue=dict_runway_to_queue, dict_available_spaces=dict_available_spaces)
  open_image(dict_name=all_dicts_names[1], dictionary=dict_runways, list_imgs=runways_imgs, show_image=show_image)
  output_generator(final_output_json=final_output_json, key='CURRENT TIME', dict_name=all_dicts_names[1], dictionary=dict_runways, all_df=all_df)
  sleep(SLEEP_TIME)
  #output.clear()
  

  dict_airplanes_to_take_off = takeoff(dict_runways=dict_runways, dict_runway_to_queue=dict_runway_to_queue)
  open_image(dict_name=all_dicts_names[2], dictionary=dict_airplanes_to_take_off, list_imgs=taking_off_imgs,show_image=show_image)
  output_generator(final_output_json=final_output_json, key=f'ROUND {round_of_execution}', dict_name=all_dicts_names[2], dictionary=dict_airplanes_to_take_off, all_df=all_df)
  sleep(SLEEP_TIME)
  #output.clear()

  dict_sky_queues = create_airplanes_sky(dict_sky_queues=dict_sky_queues, dict_available_spaces=dict_available_spaces)
  open_image(dict_name=all_dicts_names[3], dictionary=dict_sky_queues, list_imgs=queues_imgs, show_image=show_image)
  output_generator(final_output_json=final_output_json, key='CURRENT TIME', dict_name=all_dicts_names[3], dictionary=dict_sky_queues, all_df=all_df)
  sleep(SLEEP_TIME)
  #output.clear()

  dict_crashed_airplanes, dict_airplanes_emergency_landings, dict_airplanes_normal_landings =landing(dict_sky_queues=dict_sky_queues, dict_runways=dict_runways,\
                                 dict_runway_to_queue=dict_runway_to_queue, dict_queue_to_runway=dict_queue_to_runway,\
                                 emergency_landings=emergency_landings, airplane_crash=airplane_crash)
  
  final_output_json['CURRENT TIME']['CRASHED AIRPLANES'] = dict_crashed_airplanes

  open_image(dict_name=all_dicts_names[4], dictionary=dict_crashed_airplanes, list_imgs=crashed_airplanes_imgs, show_image=show_image)
  output_generator(final_output_json=final_output_json, key=f'ROUND {round_of_execution}', dict_name=all_dicts_names[4], dictionary=dict_crashed_airplanes, all_df=all_df)
  sleep(SLEEP_TIME)
  #output.clear() 
   

  open_image(dict_name=all_dicts_names[5], dictionary=dict_airplanes_emergency_landings, list_imgs=emergency_landings_imgs, show_image=show_image)
  output_generator(final_output_json=final_output_json, key=f'ROUND {round_of_execution}', dict_name=all_dicts_names[5], dictionary=dict_airplanes_emergency_landings, all_df=all_df)
  sleep(SLEEP_TIME)
  #output.clear() 
  
  open_image(dict_name=all_dicts_names[6], dictionary=dict_airplanes_normal_landings, list_imgs=landings_imgs, show_image=show_image)
  output_generator(final_output_json=final_output_json, key=f'ROUND {round_of_execution}', dict_name=all_dicts_names[6], dictionary=dict_airplanes_normal_landings, all_df=all_df)
  sleep(SLEEP_TIME)
  #output.clear() 
  
  #sleep(5)

#saving DataFrame on .xlsx
final_df = pd.concat(all_df)
final_df = final_df.reset_index()
final_df.drop(["index"], axis=1, inplace=True)
exec_moment = moment_of_execution.replace(':','-').replace(' ','-')
final_df.to_excel(f'AYA_Airport_Output_{exec_moment}.xlsx')

#saving the data on .json
with open(f'AYA_Airport_Output_{exec_moment}.json','a') as file:
  file.write(str(final_output_json))

#saving the data on .json
with open(f'AYA_Airport_Output_{exec_moment}.txt','a') as file:
  file.write(f'Number of rounds: {NUMBER_OF_ROUNDS}')
  file.write(f'\nTotal of airplane crashed: {airplane_crash}')