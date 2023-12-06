import openai
import numpy as np
from utils.env import *

class Baseline():
    def __init__(self, objects):
        self.system_prompt = """
        I am a robot that can pick up objects and place them.
        Please remember that you cannot move the bowls, you can only move blocks.
        You can put blocks in a bowl, or move blocks on top of other blocks, or move blocks into a certain position.
        I have to reason out the user's preferences and execute them. Each time, I will tell you what the user likes comparing two goals.
        I can spawn maximum 5 objects at a time.
        Available objects are: {}
        """.format(ALL_BLOCKS+ALL_BOWLS)
        self.obj_prompt = """
        First, choose an objects you want to spawn in the environment. You can choose 3-5 objects.
        format: objects = {}
        """.format(str(objects))
        self.goal_prompt = """
        The user told me what they like, but we haven't reached the goal yet. Please generate different goals that match the user's preference.
        I can see {}
        Next, specify the two different goal state of the environment, written in one sentence.
        Based on the user's comparison, please reason out the user's preference.
        Try to make different context of goal from the past goals, do not generate in same context.
        Please match the preference, and two goal has to be as diverse as possible, put two goals should still match the preference.
        format: 
                preference =
                goal1 = 
                goal2 = 
        if you think you are sure about the preference, please type 'done'
            format: 
                preference = done
                goal1 = done
                goal2 = done
        """.format(str(objects))
        self.messages = [{'role': 'system', 'content': self.system_prompt}]
        self.answer = None
        self.log = []
    def goal_generation(self):
        if self.answer == None:
            self.messages.append({'role':'user','content':self.goal_prompt})
        else:
            self.messages.append({'role':'user','content': self.answer + self.goal_prompt})
        goal_1, goal_2 = None, None
        preference = None
        while goal_1 == None or goal_2 == None:
            f_src = openai.ChatCompletion.create(
                        messages=self.messages,
                        model = 'gpt-4'
                    )['choices'][0]['message']['content'].strip()
            lines = f_src.split('\n')
            print(f_src)
            for l in lines:
                l = l.lower()
                if 'goal 1' in l or 'goal1' in l:
                    goal_1 = l
                if 'goal 2' in l or 'goal2' in l:
                    goal_2 = l
                if 'preference' in l and self.answer!=None:
                    preference = l
        if preference== None: preference = ''
        self.log.append(f_src)
        self.messages.append({'role':'assistant', 'content': preference+'\n'+goal_1+'\n'+goal_2})
        return goal_1, goal_2
    
    def answer_generation(self, indx = 1):
        if indx == 1:
            msg = 'goal_1 is better than goal_2'
        elif indx == 2: 
            msg = 'goal_2 is better than goal_1'
        elif indx == 3:
            msg = 'Both of them are bad. You need to explore more'
        else:
            msg = 'I do not know'
        self.log.append(msg)
        self.answer = msg

    def final_goal(self, new_lists):
        question = """ Now, you see {}  please generate the goal that fits the preference
        format: goal =
""".format(str(new_lists))  
        self.messages.append({'role':'user','content':question})
        f_src = openai.ChatCompletion.create(
                        messages=self.messages,
                        model = 'gpt-4'
                    )['choices'][0]['message']['content'].strip()
        lines = f_src.split('\n')
        for l in lines:
            l = l.lower()
            if 'goal' in l:
                goal = l
                break
        self.log.append(f_src)
        return goal