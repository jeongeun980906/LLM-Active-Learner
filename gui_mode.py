from utils.env import *
from utils.lmp import *
from utils.lmp_wrapper import *
import copy
from utils.cap_prompts import *
import matplotlib.pyplot as plt
from utils.config import *
from moviepy.editor import ImageSequenceClip
import openai
from llm.gui import GUI
from llm.baseline import Baseline
import openai
from utils.key_register import set_openai_api_key_from_txt

set_openai_api_key_from_txt(key_path='./key/key.txt',VERBOSE=True)

#@title Initialize Env { vertical-output: true }
num_blocks = 3 #@param {type:"slider", min:0, max:4, step:1}
num_bowls = 1 #@param {type:"slider", min:0, max:4, step:1}
high_resolution = False #@param {type:"boolean"}
high_frame_rate = False #@param {type:"boolean"}

# setup env and LMP
env = PickPlaceEnv(render=True, high_res=high_resolution, high_frame_rate=high_frame_rate)
block_list = np.random.choice(ALL_BLOCKS, size=num_blocks, replace=False).tolist()
bowl_list = np.random.choice(ALL_BOWLS, size=num_bowls, replace=False).tolist()
obj_list = block_list + bowl_list
_ = env.reset(['green block', 'purple block', 'blue block','purple bowl'])
lmp_tabletop_ui = setup_LMP(env, cfg_tabletop)

# display env
img =env.get_camera_image()

# display image
# plt.figure(figsize=(5,5))
# plt.imshow(img)
# plt.axis('off')
# plt.show()

print('available objects:')
print(obj_list)

from llm.baseline import Baseline
logger = Baseline(['orange block', 'yellow block', 'red block','purple bowl'])
goal_1, goal_2 = logger.goal_generation()
from llm.gui import GUI
gui = GUI()
gui.root.update()
gui.display_image(img, img)
for _ in range(5):
    if 'done' in goal_1 or 'done' in goal_2:
        break
    goal_1 = goal_1.split("=")[-1]
    goal_2 = goal_2.split("=")[-1]
    gui.display_goals(goal_1, goal_2)

    _ = env.reset(['orange block', 'yellow block', 'red block','purple bowl'])

    env.cache_video = []
    try:
        lmp_tabletop_ui(goal_1, f'objects = {env.object_list}')
        # display env
        img_1 =env.get_camera_image()
    except:
        img_1 = None
    _ = env.reset(['orange block', 'yellow block', 'red block','purple bowl'])
    env.cache_video = []
    try:
        lmp_tabletop_ui(goal_2, f'objects = {env.object_list}')
    except:
        img_2 = None
    # display env
    img_2 =env.get_camera_image()
    gui.display_image(img_1, img_2)
    while gui.label == None:
        gui.root.update()
    logger.answer_generation(gui.label)
    goal_1, goal_2 = logger.goal_generation()


    
#@title Interactive Demo { vertical-output: true }
goal = logger.final_goal(['green block', 'purple block', 'blue block','purple bowl'])

# run policy
_ = env.reset(['green block', 'purple block', 'blue block','purple bowl'])
user_input = goal

env.cache_video = []
gui.display_goals("final", goal)

print('Running policy and recording video...')
lmp_tabletop_ui(user_input, f'objects = {env.object_list}')
img =env.get_camera_image()
gui.display_image(img, img)
# import copy
# render video
if env.cache_video:
    rendered_clip = ImageSequenceClip(env.cache_video, fps=35 if high_frame_rate else 25)
#   display(rendered_clip.ipython_display(autoplay=1, loop=1))
while True:
    gui.root.update()