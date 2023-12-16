import numpy as np
import pandas as pd
import random, os, datetime

total_reward = 0
bandit_dict = {}
exploration_done = 0
mimic_count = 0
stepping = 0

def set_seed(my_seed=42):
    os.environ['PYTHONHASHSEED'] = str(my_seed)
    random.seed(my_seed)
    np.random.seed(my_seed)

def get_next_bandit():
    global exploration_done, mimic_count, stepping
    
    #get base calculators
    total_tries = [bandit_dict[bnd]['win'] + bandit_dict[bnd]['loss'] + bandit_dict[bnd]['opp'] for bnd in bandit_dict]
    
    #comparable with number of wins (already inlcudes the total_tries)
    factor_machine = [((0.03)/(1-0.97**total_tries[bnd])*(0.97**(total_tries[bnd]-1)))*total_tries[bnd] \
                      if total_tries[bnd] > 0 else 1 for bnd in bandit_dict]
    
    #is opponent mimicking
    if last_pull == previous_my:
        if bandit_dict[last_pull]['oppinf'] < 0:
            oppinf = 0
        else:
            oppinf = bandit_dict[last_pull]['oppinf']
        bandit_dict[last_pull]['wininf'] +=  \
        (bandit_dict[last_pull]['win'] + bandit_dict[last_pull]['wininf']) /\
        (bandit_dict[last_pull]['win'] + oppinf + bandit_dict[last_pull]['loss'])
        bandit_dict[last_pull]['oppinf'] += 1
    
    
    #3 first visits exploitation analysis
    else: 
        #set the number of opponent moves to use to compare to wininf
        if bandit_dict[last_pull]['visits'] <= 7:
            if bandit_dict[last_pull]['mimicked'] == 0:
                if bandit_dict[last_pull]['visits'] <= 4:
                    bandit_dict[last_pull]['oppinf'] += 1 

                #v1r
                if (bandit_dict[last_pull]['visits'] == 1) & (bandit_dict[last_pull]['repeat'] >= 2):
                        bandit_dict[previous_pull]['wininf'] +=  1
                #v2r1 - we are assuming he is still exploring
                if (bandit_dict[last_pull]['repeat'] == 1) & (bandit_dict[last_pull]['visits'] == 2):
                    explored = 0
                    visited_2nd = 0
                    for bnd in bandit_dict:
                        if bandit_dict[bnd]['opp'] > 0:
                            explored += 1
                        if bandit_dict[bnd]['visits'] > 1:
                            visited_2nd += 1
                    if visited_2nd / explored < 0.5:
                        if bandit_dict[last_pull]['opp'] == 2:
                            bandit_dict[last_pull]['wininf'] +=  1
                #v2r
                if (bandit_dict[last_pull]['repeat'] >= 2) & (bandit_dict[last_pull]['visits'] == 2):
                    bandit_dict[last_pull]['wininf'] +=  1

                #v3r1 - we are assuming he is still exploring, but will decrease the quality of his results gradually

                if (bandit_dict[last_pull]['visits'] == 3) & (bandit_dict[last_pull]['repeat'] == 1):
                    explored = 0
                    visited_2nd = 0
                    for bnd in bandit_dict:
                        if bandit_dict[bnd]['opp'] > 0:
                            explored += 1
                        if bandit_dict[bnd]['visits'] > 2:
                            visited_2nd += 1
                    if visited_2nd / explored < 0.25:
                            bandit_dict[last_pull]['wininf'] +=  1

                #v3r
                if (bandit_dict[last_pull]['repeat'] >= 2) & (bandit_dict[last_pull]['visits'] == 3):
                    bandit_dict[last_pull]['wininf'] +=  1

                
                #v4r1 - we are assuming he is still exploring, but will decrease the quality of his results gradually
                if (bandit_dict[last_pull]['visits'] == 4) & (bandit_dict[last_pull]['repeat'] == 1):
                    explored = 0
                    visited_2nd = 0
                    for bnd in bandit_dict:
                        if bandit_dict[bnd]['opp'] > 0:
                            explored += 1
                        if bandit_dict[bnd]['visits'] > 3:
                            visited_2nd += 1
                    if visited_2nd / explored < 0.125:
                            bandit_dict[last_pull]['wininf'] +=  1


                #v4r
                if (bandit_dict[last_pull]['repeat'] >= 2) & (bandit_dict[last_pull]['visits'] == 4):
                    bandit_dict[last_pull]['wininf'] +=  1
                    
                #v5r1 - we are assuming he is still exploring, but will decrease the quality of his results gradually
                if (bandit_dict[last_pull]['visits'] == 5) & (bandit_dict[last_pull]['repeat'] == 1):
                    explored = 0
                    visited_2nd = 0
                    for bnd in bandit_dict:
                        if bandit_dict[bnd]['opp'] > 0:
                            explored += 1
                        if bandit_dict[bnd]['visits'] > 4:
                            visited_2nd += 1
                    if visited_2nd / explored < 0.00625:
                            bandit_dict[last_pull]['wininf'] +=  1
                            bandit_dict[last_pull]['oppinf'] += 1 


                #v5r
                if (bandit_dict[last_pull]['repeat'] >= 2) & (bandit_dict[last_pull]['visits'] == 5):
                    bandit_dict[last_pull]['wininf'] +=  1
                    bandit_dict[last_pull]['oppinf'] += 1 
                    #v5r1 - we are assuming he is still exploring, but will decrease the quality of his results gradually
                
                if (bandit_dict[last_pull]['visits'] == 6) & (bandit_dict[last_pull]['repeat'] == 1):
                    explored = 0
                    visited_2nd = 0
                    for bnd in bandit_dict:
                        if bandit_dict[bnd]['opp'] > 0:
                            explored += 1
                        if bandit_dict[bnd]['visits'] > 5:
                            visited_2nd += 1
                    if visited_2nd / explored <0.03125:
                            bandit_dict[last_pull]['wininf'] +=  1
                            bandit_dict[last_pull]['oppinf'] += 1

                #v5r
                if (bandit_dict[last_pull]['repeat'] >= 2) & (bandit_dict[last_pull]['visits'] == 6):
                    bandit_dict[last_pull]['wininf'] +=  1   
                    bandit_dict[last_pull]['oppinf'] += 1
                
                if (bandit_dict[last_pull]['visits'] == 7) & (bandit_dict[last_pull]['repeat'] == 1):
                    explored = 0
                    visited_2nd = 0
                    for bnd in bandit_dict:
                        if bandit_dict[bnd]['opp'] > 0:
                            explored += 1
                        if bandit_dict[bnd]['visits'] > 6:
                            visited_2nd += 1
                    if visited_2nd / explored <0.015625:
                            bandit_dict[last_pull]['wininf'] +=  1
                            bandit_dict[last_pull]['oppinf'] += 1


                #v5r
                if (bandit_dict[last_pull]['repeat'] >= 2) & (bandit_dict[last_pull]['visits'] == 7):
                    bandit_dict[last_pull]['wininf'] +=  1  
                    bandit_dict[last_pull]['oppinf'] += 1
                    
            else:
                bandit_dict[last_pull]['mimicked'] = 0
        

    #mimicking
    mimic = [bnd for bnd in bandit_dict if (bandit_dict[bnd]['repeat'] >= 2) & (bandit_dict[bnd]['visits'] <= 4)]

        
    r = 0
    for bnd in bandit_dict:
        if (bandit_dict[bnd]['win'] + bandit_dict[bnd]['loss'] > 0) & (bandit_dict[bnd]['opp'] == 0):
            r+= 1
        if (bandit_dict[bnd]['win'] + bandit_dict[bnd]['loss'] == 0) & (bandit_dict[bnd]['opp'] > 0):
            r-= 1    

    if r >= 2:
        rand = random.random()
        if rand > 0.9:
            exploration_done = 0
        else:
            exploration_done = 2
    else: 
        exploration_done = 0


    #exploration    
    if exploration_done == 0:        
        candidates = [bnd for bnd in bandit_dict if bandit_dict[bnd]['win'] + bandit_dict[bnd]['loss'] + bandit_dict[bnd]['opp'] == 0]
        if len(candidates) == 0:
            exploration_done = 1
        
    if exploration_done == 1:
        exploration_list_1 = [bnd for bnd in bandit_dict if (bandit_dict[bnd]['win'] + bandit_dict[bnd]['loss'] + bandit_dict[bnd]['opp'] == 1) \
                              | (bandit_dict[bnd]['win'] + bandit_dict[bnd]['loss'] + bandit_dict[bnd]['oppinf'] == 0)]
        if len(exploration_list_1) == 0:
            exploration_done = 2
        else:
            exploration_priority_1 = []
            for bnd in exploration_list_1:
                exploration_priority_1.append({'bnd': bnd, 'priority': bandit_dict[bnd]['wininf'] + bandit_dict[bnd]['win']})   
            priorities_1 = [x['priority'] for x in exploration_priority_1]
            max_1 = max(priorities_1)
            candidates = [x['bnd'] for x in exploration_priority_1 if x['priority'] == max_1]

            
    #exploitation
    if exploration_done >= 2:
      #  print(stepping)
        percentages = []
        percentages = [(bandit_dict[bnd]['wininf'] + bandit_dict[bnd]['win']) \
                       /(bandit_dict[bnd]['win'] + bandit_dict[bnd]['oppinf'] + bandit_dict[bnd]['loss']) \
                       * factor_machine[bnd] if (bandit_dict[bnd]['win'] + bandit_dict[bnd]['oppinf'] + bandit_dict[bnd]['loss']) > 0 else 1
                       for bnd in bandit_dict]
        pcts_bnd =  [bnd for bnd in bandit_dict]
        w = max(percentages)
        percentages = [w
                       if ((bandit_dict[bnd]['win'] + bandit_dict[bnd]['oppinf'] + bandit_dict[bnd]['loss']) < 5) & (w <= 0.4) \
                       & (percentages[bnd] < 0.1)
                       else percentages[bnd]  for bnd in bandit_dict]
        k = random.random()
        if k > 0:
            percentages = [w
                           if (bnd == last_pull) & (stepping >= 1700) else percentages[bnd]  for bnd in bandit_dict]
        exploitation = [i for i, j in enumerate(percentages) if (j >= w - 0.05 + ((stepping/1999*0.8)*0.05))]

    #my pull
    if (len(mimic) != 0) & (stepping <= 400) & (mimic_count<= 3): 
        my_pull = mimic[0]
        mimic_count += 1
    elif (len(mimic) != 0) & (stepping >= 400) & (mimic_count<= 5):
        my_pull = mimic[0]
        mimic_count += 1
        #exploration
    elif exploration_done < 2:
        mimic_count = 0
        my_pull = random.choice(candidates)
        #exploitation
    else:
        mimic_count = 0
        my_pull = random.choice(exploitation)


    return my_pull

def multi_armed_probabilities(observation, configuration):
    global total_reward, bandit_dict, last_pull, previous_pull, last_reward, last_my, previous_my, exploration_done, stepping

    my_pull = random.randrange(configuration['banditCount'])
    if 0 == observation['step']:
        set_seed()
        total_reward = 0
        bandit_dict = {}
        for i in range(configuration['banditCount']):
            bandit_dict[i] = {'win': 0, 'loss': 0, 'opp': 0, 'visits':0, 'repeat':0, 'wininf':0, 'oppinf':-1, 'mimicked': 0}
    else:
        if 1 == observation['step']:
            previous_pull = -1
            previous_my = -1
        last_reward = observation['reward'] - total_reward
        total_reward = observation['reward']
        
        my_idx = observation['agentIndex']
        if 0 < last_reward:
            bandit_dict[observation['lastActions'][my_idx]]['win'] = bandit_dict[observation['lastActions'][my_idx]]['win'] +1
        else:
            bandit_dict[observation['lastActions'][my_idx]]['loss'] = bandit_dict[observation['lastActions'][my_idx]]['loss'] +1
        bandit_dict[observation['lastActions'][1-my_idx]]['opp'] = bandit_dict[observation['lastActions'][1-my_idx]]['opp'] +1
        bandit_dict[observation['lastActions'][1-my_idx]]['repeat'] += 1
        last_pull = observation['lastActions'][1-my_idx]
        last_my = observation['lastActions'][my_idx]
        if last_pull != previous_pull:
            if bandit_dict[observation['lastActions'][1-my_idx]]['mimicked'] == 0:
                bandit_dict[observation['lastActions'][1-my_idx]]['visits'] += 1
            if previous_pull != -1:
                bandit_dict[previous_pull]['repeat'] = 0
        if last_pull == previous_my:
            bandit_dict[previous_pull]['mimicked'] = 1
        stepping = observation['step']
        previous_pull = last_pull  
        previous_my = last_my

        my_pull = get_next_bandit()

    return my_pull
