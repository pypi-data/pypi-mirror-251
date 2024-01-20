import tensorflow as tf 
import keras as k
import pandas as pd
import os    
from tqdm.notebook import tqdm   
import numpy as np
from sklearn.preprocessing import LabelEncoder

class classification:

    def create_dataframe(self,dir):
        image_paths=[]
        labels = []
        for label in os.listdir(dir):
            dirs = os.path.join(dir,label)
            for imagename in os.listdir(dirs):
                image_paths.append(os.path.join(dir,label,imagename))
                labels.append(label)
            print(f"{label}, completed")

        train = pd.DataFrame()
        train['Images'], train['Labels'] = image_paths,labels
        self.df=train
            
        return train
    
    def prep_x_train(self,images_paths,h=100,w=100):
        self.features=[]
        self.h = h
        self.w = w
        for images in tqdm(images_paths):
            img = k.preprocessing.image.load_img(images,grayscale=True)
            img.resize((h,w))
            img = np.array(img)
            self.features.append(img)
        self.features = np.array(self.features)
        self.features = self.features.reshape(len(self.features),h,w,1)
        feature = self.features/255.0
        return feature
    def prep_y_train(self,labels,num_classes):
        le = LabelEncoder()
        le.fit(labels)
        y_train = le.transform(labels)
        y_train = k.utils.to_categorical(y_train,num_classes=num_classes)
        self.y_train = y_train
        return y_train
    def make_model(self,unit,num_classes):
        input_shape=(self.h,self.w,1)
        from keras.models import Sequential
        from keras.layers import Dense,MaxPooling2D,Conv2D,Dropout,Flatten

        model = Sequential()
        model.add(Conv2D(unit,(3,3),input_shape=input_shape,activation='relu'))
        model.add(MaxPooling2D(pool_size=(2,2)))
        model.add(Dropout(0.4))
        unit2=unit*2
        model.add(Conv2D(unit2,(3,3),input_shape=input_shape,activation='relu'))
        model.add(MaxPooling2D((2,2)))
        model.add(Dropout(0.4))
        unit3=unit*3
        model.add(Conv2D(unit3,(3,3),input_shape=input_shape,activation='relu'))
        model.add(MaxPooling2D((2,2)))
        model.add(Dropout(0.4))
        model.add(Conv2D(unit3,(3,3),input_shape=input_shape,activation='relu'))
        model.add(MaxPooling2D((2,2)))
        model.add(Dropout(0.4))
        model.add(Flatten())
        model.add(Dense(unit3,activation='relu'))
        model.add(Dropout(0.45))
        model.add(Dense(unit2,activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(num_classes,activation='softmax'))
        self.model = model
        model.summary()
        return model
    def train_model(self,model,x_train,y_train,batch_size,epochs):
        model.compile(loss='categorical_crossentropy',optimizer='adam',metrics='accuracy')
        model.fit(x_train,y_train,epochs=epochs,batch_size=batch_size)
        self.model = model
        return model

    def create(self,train_dir,numclasses,unit=16,batch_size=32,epochs=10,h=100,w=100):
        df = self.create_dataframe(train_dir)
        x_train = self.prep_x_train(df['Images'],h=h,w=w)
        y_train = self.prep_y_train(df['Labels'],num_classes=numclasses)
        input_shape=self.features.shape
        model = self.make_model(unit=unit,num_classes=numclasses)
        fit_model = self.train_model(model,x_train,y_train,batch_size,epochs)
        return fit_model

            