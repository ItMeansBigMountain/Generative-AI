import gym
import random
import numpy as np 
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, InputLayer
from tensorflow.keras.optimizers import Adam
from statistics import mean, median 
from collections import Counter

LR = 1e-3
env = gym.make("CartPole-v1", render_mode="human")
import time

def neural_network_model(input_size):
    model = Sequential()
    model.add(InputLayer(input_shape=(input_size,)))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.2))  # Dropout rate is the inverse of keep probability
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(2, activation='softmax'))
    model.compile(optimizer=Adam(learning_rate=LR), loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def train_model(training_data, model=False):
    X = np.array([i[0] for i in training_data]).reshape(-1, len(training_data[0][0]))
    y = np.array([i[1] for i in training_data])
    if not model:
        model = neural_network_model(input_size=len(X[0]))
    model.fit(X, y, epochs=5, batch_size=32, verbose=1)
    return model

def initial_population(epochs=5, game_time=10000):
    training_data = []
    scores = []
    accepted_scores = []
    score_requirement = 50

    for epoch in range(epochs):
        env.reset()
        score = 0
        game_memory = []
        prev_observation = []

        for _ in range(game_time):
            action = random.randrange(0, 2)
            observation, reward, done, truncated, info = env.step(action) 
            if len(prev_observation) > 0:
                game_memory.append([prev_observation, action])
            prev_observation = observation 
            score += reward
            if done:
                break 

        print("Score:", score)
        if score >= score_requirement:
            accepted_scores.append(score)
            for data in game_memory:
                output = [0, 1] if data[1] == 1 else [1, 0]
                training_data.append([data[0], output])
                # print(f"Data[0] shape: {np.array(data[0]).shape}, Output shape: {np.array(output).shape}")

        env.reset()
        scores.append(score)
    
    training_data_save = np.array(training_data, dtype=object)
    np.save('saved_.npy', training_data_save)

    if len(training_data):
        return training_data
    else:
        return None

def Random_Game_Simulation():
    for episode in range(5):
        env.reset()
        for t in range(500):
            env.render()
            action = env.action_space.sample()
            observation, reward, done, truncated, info = env.step(action)
            print(observation)
            print(reward)
            print(done)
            print(truncated)
            print(info)
            print("-------------------------------------\n")
            time.sleep(5)
            if done:
                break

def ai_plays_game(epochs=5, game_time=500, model = None):
    if not model:
        print("Please load model into function. Thanks...")
        return None
        
    scores = []
    choices  = []

    # EPISODES
    for epoch in range(epochs):
        env.reset()
        score = 0
        game_memory = []
        prev_observation = []
        
        # GAME DURING AN EPISODE OF PLAY TIME
        for _ in range(game_time):
            env.render()

            # CHECK IF THIS IS THE FIRST ROUND OF THE GAME
            if len(prev_observation) == 0:
                action = random.randrange(0, 2)
            else: 
                # translates the model's output probabilities into a concrete action
                action = np.argmax(model.predict(prev_observation.reshape(-1, len(prev_observation), 1))[0] )
            
            # ADD ACTION TO CHOICES ARRAY
            choices.append(action)

            # GET RESULTS OF ACTION AND SAVE INTO GAMES MEMORY
            new_observation, reward, done, truncated, info = env.step(action) 
            prev_observation = new_observation
            game_memory.append([new_observation , action])

            if done:
                break

            # SAVE SCORE 
            score += reward
            scores.append(score)

        print(f"AVERAGE SCORE : {sum(scores) / len(scores)}")
        print(f"Choice 0 : {choices.count(0)/ len(choices)}%")
        print(f"Choice 1 : {choices.count(1)/ len(choices)}%")




# TRAINING MODEL
training_data = None
while not training_data:
    training_data = initial_population(epochs=5000, game_time=50000)
model = train_model(training_data)

# EXAMPLE OF SAVING & LOADING MODEL 
model.save("trained_gt50.h5")
# model.load("trained_gt50.h5")


# AI PLAYS THE GAME!
ai_plays_game(epochs=10, game_time=10000, model=model)