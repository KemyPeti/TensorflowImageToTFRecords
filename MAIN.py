# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 11:38:13 2019

@author: KemyPeti
"""
import sys
import os
sys.path.append(os.getcwd() + "\\code\\TFRecordCreator")

import numpy as np
import tensorflow as tf

import TFFuncLib as TFEC

#%% write TFRecord with image

TFRGenerator = TFEC.TFRecordGenerator.generate(path = "TFRecord_container",
                                               filename = "2019_06_13_try")
for idx in range(10):
    #--------------------------------EXAMPLE INPUT----------------------------#
    A = np.array([idx*1.0, idx*2.0], dtype = np.float32) #the decode type have to be the same!!!
    np.save('example_image' + str(idx) + '.npy', A)
    #--------------------------------EXAMPLE END------------------------------#
    
    #--------------------CREATE EXAMPLE FROM NUMPY ARRAY----------------------#
    feature_dict = TFEC.ImageToTfFeature.create('example_image' + str(idx) + '.npy')
    
    feature_dict = TFEC.AddFeatureToDict(feature_dict = feature_dict,
                                         data_to_add_key = "label",
                                         data_to_add_value = 0.22*idx, #example_value
                                         type_ = "float")
    example = TFEC.FeatureDict2TfExample(feature_dict)
    
    
    #-----------------------------WRITE TFRECORDS-----------------------------#
    #own function (it saves the tfrecord file and a pickle that contains the 
    #tfrecord informations for read)
    TFRGenerator.write(example, feature_dict)

TFRGenerator.close()
#%%
#--------------------------------READ TFRECORD DATASET------------------------#
TFRecReader = TFEC.TFRecordReader.read_keys(path = "TFRecord_container",
                                            filename = "2019_06_13_try")

dataset = TFRecReader.get_dataset()

#------------------------CALL THE EXAMPLES FROM THE DATASET-------------------#
#(NO ITERATOR ANYMORE!)
dataset = dataset.repeat(3)         #epoch_size
dataset = dataset.shuffle(10000)    #shuffle_buffer_size
dataset = dataset.batch(5)          #batch size
dataset = dataset.prefetch(1)       #buffer_size
for serialized_examples in dataset:
    parsed = TFRecReader.parse_examples(serialized_examples)
    image =  tf.io.decode_raw(parsed['image/encoded'],
                              out_type=tf.float32, #the decode type have to be the same as the input type!!!
                              little_endian=True)
    #print(image.numpy())
