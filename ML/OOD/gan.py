#!/usr/bin/env python3
# Matt

from keras.layers import Input
from keras.models import Model
from keras.optimizers import Adam
from sklearn.preprocessing import LabelEncoder

from discriminator import Discriminator
from generator import Generator

import numpy as np
import pandas as pd


class GAN(object):

    def __init__(self, attack):
        """ Constructor """
        self.attack_type = attack
        self.discriminator = None
        self.generator = None
        self.gan = None

    def train(self):
        batch_size = 256
        epochs = 7000
        optimizer = Adam(0.0002, 0.5)
        
        dataframe = pd.read_csv('../../../CSV/kdd_neptune_only_5000.csv').sample(500) # sample 100 data points randomly from the csv
        
        # apply "le.fit_transform" to every column (usually only works on 1 column)
        le = LabelEncoder()
        dataframe_encoded = dataframe.apply(le.fit_transform)
        dataset = dataframe_encoded.values
        
        #to visually judge results
        print("Real neptune attacks:")
        print(dataset[:2])
        
        # Set X as our input data and Y as our label
        X_train = dataset[:, 0:41].astype(float)
        Y_train = dataset[:, 41]
        
        # labels for data. 1 for valid attacks, 0 for fake (generated) attacks
        valid = np.ones((batch_size, 1))
        fake = np.zeros((batch_size, 1))
        
        # build the discriminator portion
        self.discriminator = Discriminator().get()
        self.discriminator.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])
        
        # build the generator portion
        self.generator = Generator(self.attack_type).get()
        
        #input and output of our combined model
        z = Input(shape=(41,))
        attack = self.generator(z)
        validity = self.discriminator(attack)
        
        # build combined model from generator and discriminator
        self.gan = Model(z, validity)
        self.gan.compile(loss='binary_crossentropy', optimizer=optimizer)
        
        #break condition for training (when diverging)
        loss_increase_count = 0;
        prev_g_loss = 0;
        
        for epoch in range(epochs):

            # ---------------------
            #  Train Discriminator
            # ---------------------
            
            # selecting batch_size random attacks from our training data
            idx = np.random.randint(0, X_train.shape[0], batch_size)
            attacks = X_train[idx]
            
            # generate a matrix of noise vectors
            noise = np.random.normal(0, 1, (batch_size, 41))
            
            # create an array of generated attacks
            gen_attacks = self.generator.predict(noise)
            
            # loss functions, based on what metrics we specify at model compile time
            d_loss_real = self.discriminator.train_on_batch(attacks, valid)
            d_loss_fake = self.discriminator.train_on_batch(gen_attacks, fake)
            d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)
            
            # generator loss function
            g_loss = self.gan.train_on_batch(noise, valid)
            
            if epoch % 100 == 0:
                print("%d [D loss: %f, acc.: %.2f%%] [G loss: %f] [Loss change: %.3f, Loss increases: %.0f]" % (epoch, d_loss[0], 100 * d_loss[1], g_loss, g_loss - prev_g_loss, loss_increase_count))
            
            # if our generator loss icreased this iteration, increment the counter by 1
            if (g_loss - prev_g_loss) > 0:
                loss_increase_count = loss_increase_count + 1
            else: 
                loss_increase_count = 0  # otherwise, reset it to 0, we are still training effectively
                
            prev_g_loss = g_loss
                
            if loss_increase_count > 5:
                print('Stoping on iteration: ', epoch)
                break
                
            if epoch % 20 == 0:
                f = open("../../../Results/GANresultsNeptune.txt", "a")
                np.savetxt("../../../Results/GANresultsNeptune.txt", gen_attacks, fmt="%.0f")
                f.close()
                
        # peek at our results
        results = np.loadtxt("../../../Results/GANresultsNeptune.txt")
        print("Generated Neptune attacks: ")
        print(results[:2])
        


def main():
    """ Auto run main method """
    attack_type = "neptune"
    gan = GAN(attack_type)
    
    gan.train()
    # print(gan.discriminator())



if __name__ == "__main__":
    main()