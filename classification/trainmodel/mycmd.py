#!/usr/bin/python

import sys
sys.path.insert(0,"D:\\09Limited_buffer\\earlywarningbyci\\classification\\trainmodel\\src")
sys.path.insert(0,"D:\\09Limited_buffer\\earlywarningbyci\\classification\\trainmodel\\")
import tms
#_*_ coding: utf-8 _*_
tms.tms_train("D:\\09Limited_buffer\\earlywarningbyci\\classification\\trainmodel\\data\\ad.txt",\
              main_save_path="./data/",\
              seg=1,indexes=[2],\
              str_splitTag=" ",\
              stopword_filename="./chinese_stopword.txt",\
              ratio=1)

tms.tms_predict("D:\\09Limited_buffer\\earlywarningbyci\\classification\\trainmodel\\data\\adtrain3.txt","D:\\09Limited_buffer\\earlywarningbyci\\classification\\trainmodel\\data\\model\\tms.config",\
                result_save_path="./data/pre.result",\
                seg=1,\
                indexes=[2])

tms. tms_analysis(".\\data\\pre.result")
