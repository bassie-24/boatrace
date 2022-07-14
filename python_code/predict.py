#!/usr/bin/env python
# coding: utf-8

import sys, os
import pandas as pd
# from sklearn.model_selection import train_test_split
# import keras
# from keras import models, layers, regularizers
# from google.colab import drive
from datetime import date, timedelta
from datetime import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
# import seaborn as sns
import pickle

def calc_buy(sorted_combis, siki, result):  
  for m, item in enumerate(sorted_combis):
    key = item[0]
    value = item[1]
    try:
      exvalue = float(odds[key]) * value
    except:
      continue
    #print(sanrentan, key)
    if m >= select:
      break
    if exvalue > 0:
      purchase[siki] += 1
      if key == result:
        hits[siki] += 1
        #print(odds)
        #print(odds[key])
        odds_list[siki].append(float(odds[key]))


def view_buy(sorted_combis, siki, parameter):  
  print('{} {}'.format(siki, parameter))
  for m, item in enumerate(sorted_combis):
    key = item[0]
    value = item[1]
    if m >= select:
      break
    print('{}: {}'.format(key, value))


def predict_buy(test_x, odds, select):
  hits = {}
  # select = 6
  total_odds = 0
  odds_list = {}
  purchase = {}
  sikis = ['t3', 'f3', 't2', 'f2']
  for siki in sikis:
    hits[siki] = 0
    purchase[siki] = 0
    odds_list[siki] = []

  predicts = {}
  for j in range(1, 7):
    t_x = test_x.iloc[0]
    t_x['Waku'] = j
    predicts[j] = model.predict(t_x.astype('float64'))

  ## 予測値を算出
  ## combis: 各かけ式について，買い目を的中率予測の大きい順にソートしたもの
  ## exvalues: 各かけ式について，買い目を期待値の大きい順にソートしたもの
  exvalues_3t = {}
  combis_3t = {}
  exvalues_3f = {}
  combis_3f = {}
  exvalues_2t = {}
  combis_2t = {}
  exvalues_2f = {}
  combis_2f = {}
  for a in range(1, 7):
    for b in range(1, 7):
      if b == a:
        continue
      probability_2t = predicts[a][0][1] * predicts[b][0][2]
      combi_2t = '{}-{}'.format(a, b)
      combis_2t[combi_2t] = probability_2t
      try:
        combi_2t_odds = float(odds[combi_2t])
      except:
        combi_2t_odds = 0
      exvalue_2t = probability_2t * combi_2t_odds
      exvalues_2t[combi_2t] = exvalue_2t
 
      sorted_2f = sorted([a, b])
      combi_2f = '{}={}'.format(sorted_2f[0], sorted_2f[1])
      if combi_2f in combis_2f:
        combis_2f[combi_2f] += probability_2t
      else:
        combis_2f[combi_2f] = probability_2t
      try:
        combi_2f_odds = float(odds[combi_2f])
      except:
        combi_2f_odds = 0
      exvalue_2f = probability_2t * combi_2f_odds
      if combi_2f in exvalues_2f: 
        exvalues_2f[combi_2f] += exvalue_2f
      else: 
        exvalues_2f[combi_2f] = exvalue_2f
 
      for c in range(1, 7):
        if c == a or c == b:
          continue
        probability_3t = predicts[a][0][1] * predicts[b][0][2] * predicts[c][0][3]
        combi_3t = '{}-{}-{}'.format(a, b, c)
        combis_3t[combi_3t] = probability_3t
        try:
          combi_3t_odds = float(odds[combi_3t])
        except:
          combi_3t_odds = 0
        exvalue_3t = probability_3t * combi_3t_odds
        exvalues_3t[combi_3t] = exvalue_3t

        sorted_3f = sorted([a, b, c])
        combi_3f = '{}={}={}'.format(sorted_3f[0], sorted_3f[1], sorted_3f[2])
        if combi_3f in combis_3f:
          combis_3f[combi_3f] += probability_3t
        else:
          combis_3f[combi_3f] = probability_3t
        try:
          combi_3f_odds = float(odds[combi_3f])
        except:
          combi_3f_odds = 0
        exvalue_3f = probability_3t * combi_3f_odds
        if combi_3f in exvalues_3f: 
          exvalues_3f[combi_3f] += exvalue_3f
        else: 
          exvalues_3f[combi_3f] = exvalue_3f


  sorted_combis_3t = sorted(combis_3t.items(), key=lambda v: v[1], reverse=True)
  sorted_exvalues_3t = sorted(exvalues_3t.items(), key=lambda v: v[1], reverse=True)
  sorted_combis_3f = sorted(combis_3f.items(), key=lambda v: v[1], reverse=True)
  sorted_exvalues_3f = sorted(exvalues_3f.items(), key=lambda v: v[1], reverse=True)
  sorted_combis_2t = sorted(combis_2t.items(), key=lambda v: v[1], reverse=True)
  sorted_exvalues_2t = sorted(exvalues_2t.items(), key=lambda v: v[1], reverse=True)
  sorted_combis_2f = sorted(combis_2f.items(), key=lambda v: v[1], reverse=True)
  sorted_exvalues_2f = sorted(exvalues_2f.items(), key=lambda v: v[1], reverse=True)
  #print(predicts, sorted_combis)

  view_buy(sorted_combis_3t, 't3', 'Hit rate')
  view_buy(sorted_combis_3f, 'f3', 'Hit rate')
  view_buy(sorted_combis_2t, 't2', 'Hit rate')
  view_buy(sorted_combis_2f, 'f2', 'Hit rate')

  view_buy(sorted_exvalues_3t, 't3', 'Expected value')
  view_buy(sorted_exvalues_3f, 'f3', 'Expected value')
  view_buy(sorted_exvalues_2t, 't2', 'Expected value')
  view_buy(sorted_exvalues_2f, 'f2', 'Expected value')

  ## 実際の結果を出す
  # results = {}
  # for k in range(6):
  #   waku = k + 1
  #   results[waku] = test_y.iloc[i, k]
  # sorted_results = sorted(results.items(), key=lambda v: v[1])
  # for l, item in enumerate(sorted_results):
  #   key = item[0]
  #   if l == 3:
  #     first = key
  #   elif l == 4:
  #     second = key
  #   elif l == 5:
  #     third = key
  #   else:
  #     continue
  # sanrentan = '{}-{}-{}'.format(first, second, third)
  # nirentan = '{}-{}'.format(first, second)
  # sorted_3f = sorted([first, second, third])
  # sanrenfuku = '{}={}={}'.format(sorted_3f[0], sorted_3f[1], sorted_3f[2])
  # sorted_2f = sorted([first, second])
  # nirenfuku = '{}={}'.format(sorted_2f[0], sorted_2f[1])
  # #print(test_y.iloc[i], sanrentan)

  # ## 購入と的中のシミュレーション
  # calc_buy(sorted_combis_3t, 't3', sanrentan)
  # calc_buy(sorted_combis_3f, 'f3', sanrenfuku)
  # calc_buy(sorted_combis_2t, 't2', nirentan)
  # calc_buy(sorted_combis_2f, 'f2', nirenfuku)

  '''
  for m, item in enumerate(sorted_combis_3t):
    key = item[0]
    value = item[1]
    try:
      exvalue = float(odds[key]) * value
    except:
      continue
    #print(sanrentan, key)
    if m >= select:
      break
    if exvalue > 0.8:
      purchase += 1
      if key == sanrentan :
        t3 += 1
        #print(odds)
        #print(odds[key])
        odds_list.append(float(odds[key]))
  
  for m, item in enumerate(sorted_exvalues):
    key = item[0]
    exvalue = item[1]
    #print(sanrentan, key)
    if exvalue > 1:
      purchase += 1
      if key == sanrentan:
        t3 += 1
        #print(odds)
        #print(odds[key])
        odds_list.append(float(odds[key]))
  '''

  '''
  acc_t3 = t3 / datalen
  total_odds = sum(odds_list)
  mean_odds = total_odds / t3
  total_purchase = datalen * select * 100
  total_refund = total_odds * 100
  print('的中率  買い目: {}点\n3連単: {}%\n平均オッズ: {}\n総購入金額: {}\n総払戻金: {}\n収支: {}'.format(select, acc_t3*100, mean_odds, total_purchase, total_refund, total_refund - total_purchase))    
  plt.hist(odds_list, density=True)
  '''

import requests
from urllib import request
from bs4 import BeautifulSoup
import sys
import pandas as pd
import re
import numpy as np 
from datetime import date, timedelta
from datetime import datetime as date
import pickle

## 選手情報を取得
def get_personal(soup, waku):
  w400 = soup.find_all('table', class_='is-w400')

  ## 3連対率を取得
  try:
    rentai = w400[1]
  except:
    return '-', '-', '-', '-', '-'
  bars = rentai.find_all('div', class_='table1_progress2Bar')
  progresses = bars[waku].find_all('span', class_='is-progress')
  one_ren = 0
  two_ren = 0
  three_ren = 0

  if len(progresses) != 0:
    for progress in progresses:
      pro_class = progress.find('span')['class'][0]
      
      if pro_class == 'is-progress1':
        style = progress['style']
        one_ren = re.search('width: (.*?)%', style).group(1)

      if pro_class == 'is-progress2':
        style = progress['style']
        two_ren = re.search('width: (.*?)%', style).group(1)
      if pro_class == 'is-progress3':
        style = progress['style']
        three_ren = re.search('width: (.*?)%', style).group(1)

  ## コース別平均スタートタイミングを取得
  sts = w400[2]
  timing = sts.find_all('span', class_='table1_progress2Label')
  try:
    st = float(timing[waku].text)
  except:
    st = '-'

  ## コース別スタート順を取得
  stjs = w400[3]
  junban = stjs.find_all('span', class_='table1_progress2Label')
  try:
    stj = float(junban[waku].text)
  except:
    stj = '-'

  return one_ren, two_ren, three_ren, st, stj

## レース場データを取得
def get_locale(html_data, hd):
  ## 季節ごとのコース別入着率を取得
  hd = '20220123'
  tuki = int(hd[4:6])
  if tuki == 12 or tuki <= 2:
    kisetu = 5
  elif tuki <= 5:
    kisetu = 2
  elif tuki <= 8:
    kisetu = 4
  else:
    kisetu = 3
  table = html_data[kisetu]
  table = table.drop('コース', axis=1)

  for i in range(6):
    if i == 0:
      out_np = table.iloc[i].values
    else:
      out_np = np.concatenate([out_np, table.iloc[i].values])
  return out_np

## 展示情報を取得
def get_tenji(html_data, waku):
  ## 調整重量取得
  tenji = html_data[1]
  chosei = tenji['体重']['調整重量'].iloc[4*waku]
  try:
    chosei = float(chosei[:-2])
  except:
    return '-', '-', '-'

  ## 展示タイム取得
  tenji_time = tenji['展示タイム']['展示タイム'].iloc[4*waku]
  tenji_time = float(tenji_time)
  
  ## チルト取得
  tilt = tenji['チルト']['チルト'].iloc[4*waku]
  tilt = float(tilt)
  
  ## スタートタイム取得
  '''
  start = html_data[2]['スタート展示']
  st = start['ST'].iloc[waku][-3:]
  st = float(st)
  '''
  return chosei, tenji_time, tilt

## 天候情報を取得
def get_weather(soup):
  ## 天候取得
  try:
    is_weather = soup.find('div', class_='is-weather')
    weather = is_weather.find('span', class_='weather1_bodyUnitLabelTitle')
    weather = weather.text
  except:
    weather = '-'
  ## 風速取得
  try:
    is_wind = soup.find('div', class_='is-wind')
    wind = is_wind.find('span', class_='weather1_bodyUnitLabelData')
    wind = float(wind.text[:-1])
  except:
    wind = '-'
  ## 波高取得
  try:
    is_wave = soup.find('div', class_='is-wave')
    wave = is_wave.find('span', class_='weather1_bodyUnitLabelData')
    wave = float(wave.text[:-2])
  except:
    wave = '-'
    
  return weather, wind, wave

## 補足情報データを作成
def make_supdata(rno, jcd, hd):
  ## get_personal用soup
  url = 'https://www.boatrace.jp/owpc/pc/data/racersearch/course?toban=4169'
  response = request.urlopen(url)
  soup_personal = BeautifulSoup(response)
  response.close

  ## レース場情報取得
  url = 'https://www.boatrace.jp/owpc/pc/data/stadium?jcd=%s' % (jcd)
  html_data = pd.read_html(url)
  out_np = get_locale(html_data, hd)

  url = 'https://www.boatrace.jp/owpc/pc/race/beforeinfo?rno=%s&jcd=%s&hd=%s' % (rno, jcd, hd)
  html_data = pd.read_html(url)
  for waku in range(6):
    chosei, tenji_time, tilt = get_tenji(html_data, waku)
    out_np = np.concatenate([out_np, [chosei, tenji_time, tilt]])
  
  url = 'https://www.boatrace.jp/owpc/pc/race/beforeinfo?rno=%s&jcd=%s&hd=%s' % (rno, jcd, hd)
  response = request.urlopen(url)
  soup = BeautifulSoup(response)
  response.close
  weather, wind, wave = get_weather(soup)      
  out_np = np.concatenate([out_np, [weather, wind, wave]])
  out_np = out_np.reshape([1, -1])
  return out_np

## 出走表データを取得
def get_data(i, racer):
  k = i * 4
  waku = racer['枠'][2 + k]
  
  boatracer1 = racer['ボートレーサー.1'][2 + k]
  try:
    number, rclass, lastname, firstname, birth, branch, age, weight = re.split('[/ \u3000]+', boatracer1)
  except:
    print(re.split('[/ \u3000]+', boatracer1))
    number, rclass, name, birth, branch, age, weight = re.split('[/ \u3000]+', boatracer1)
    lastname = name[:3]
    firstname = name[3:]

  boatracer2 = racer['ボートレーサー.2'][2 + k]
  boatracer2_list = boatracer2.split()
  F = boatracer2_list[0][1]
  L = boatracer2_list[1][1]
  ST = boatracer2_list[2]

  zenkoku = racer['全国'][2 + k]
  (zr, z2r, z3r) = map(str, zenkoku.split())
  
  touchi = racer['当地'][2 + k]
  (tr, t2r, t3r) = map(str, touchi.split())

  motor = racer['モーター'][2 + k]
  motor_list = motor.split()
  m_num = motor_list[0]
  m2r = motor_list[1]
  m3r = motor_list[2]

  boat = racer['ボート'][2 + k]
  boat_list = boat.split()
  b_num = boat_list[0]
  b2r = boat_list[1]
  b3r = boat_list[2]

  url = 'https://www.boatrace.jp/owpc/pc/data/racersearch/course?toban=%s' % (number)
  try:
    response = request.urlopen(url)
    soup = BeautifulSoup(response)
    response.close

    one_ren, two_ren, three_ren, st, stj = get_personal(soup, i)
  except:
    one_ren = '-'
    two_ren = '-'
    three_ren = '-'
    st = '-'
    stj = '-'
    
  weight = weight[:-2]

  return_data = np.array([int(waku), number, rclass, lastname, firstname, birth, branch, age, weight, F, L, ST, zr, z2r, z3r, tr, t2r, t3r, m_num, m2r, m3r, b_num, b2r, b3r, one_ren, two_ren, three_ren, st, stj])
  
  return return_data

## レースデータを作成
def make_racedata(rno, jcd, hd):
  racelist = 'https://www.boatrace.jp/owpc/pc/race/racelist?rno=%s&jcd=%s&hd=%s' % (rno, jcd, hd)
  html_data = pd.read_html(racelist, header=0)
  table = html_data[1]
  racer1 = table[2:6]
  racer2 = table[6:10]
  racer3 = table[10:14]
  racer4 = table[14:18]
  racer5 = table[18:22]
  racer6 = table[22:26]

  racers = [racer1, racer2, racer3, racer4, racer5, racer6]

  input_data = np.empty((1, 174), dtype=object)
  for i, racer in enumerate(racers):
    input_data[0, i*29:(i+1)*29] = get_data(i, racer)

  return input_data


## レース結果を取得
def get_result_data(waku, html_data):
  try:
    result_table = html_data[1][html_data[1]['枠'] == int(waku)]
    index = result_table.index[0]
    chaku = result_table['着'][index]
    boatracer = result_table['ボートレーサー'][index]
  except:
    waku = '中止'
    number = 'None'
    lastname = 'None'
    firstname = 'None'
    chaku = '中止'
    course = 'None'
    ST = 'None'
    racetime = 'None'
    #return_data = np.array([waku, number, lastname, firstname, chaku, course, ST, racetime])
    return_data = chaku
    return return_data

  try:
    number, lastname, firstname = boatracer.split()
  except:
    print(boatracer.split())
    number, name = boatracer.split()
    lastname = name[:3]
    firstname = name[3:]
  racetime = result_table['レースタイム'][index]
  
  start_table = html_data[2]
  flag = 0
  num_of_people = len(start_table['スタート情報'])
  for i in range(num_of_people):
    kojin = start_table['スタート情報'][i]
    kojin_list = kojin[:6].split()
    if kojin_list[0] == waku:
      course = str(i+1)
      ST = kojin_list[1]
      flag = 1

  if flag == 0:
    course = 'None'
    ST = 'None'
  try:
    kimarite = html_data[5].iloc[0, 0]
  except:
    kimarite = 'None'

  try:
    chaku = int(chaku)
  except:
    chaku = 0
  #return_data = np.array([waku, number, lastname, firstname, chaku, course, ST, racetime])
  return_data = chaku
  return return_data

## レース結果データを作成
def make_resultdata(rno, jcd, hd):
  raceresult = 'https://www.boatrace.jp/owpc/pc/race/raceresult?rno=%s&jcd=%s&hd=%s' % (rno, jcd, hd)
  html_data = pd.read_html(raceresult, header=0)
 
  wakus = ['1', '2', '3', '4', '5', '6']

  output_data = np.empty((1, 6), dtype=object)
  for i, waku in enumerate(wakus):
    output_data[0, i] = get_result_data(waku, html_data)
  return output_data
#make_resultdata(5, 17, 20210623)

## オッズデータを作成
def make_oddsdata(rno, jcd, hd):
  sikis = ['3t', '3f', '2tf']
  odds_np = np.empty(0, dtype=float)
  for siki in sikis:   
      odds = 'https://www.boatrace.jp/owpc/pc/race/odds%s?rno=%s&jcd=%s&hd=%s' % (siki, rno, jcd, hd)
      html_data = pd.read_html(odds, header=0)

      if siki == '3t':
        table = html_data[1]
        for i in range(6):
          for j in range(20):
            odds_np = np.hstack([odds_np, table.iloc[j, 2+(i*3)]])
      elif siki == '3f':
        table = html_data[1]
        begins = [0, 4, 7, 9]
        for i, begin in enumerate(begins):
          for j in range(begin, 10):
            odds_np = np.hstack([odds_np, table.iloc[j, 2+(i*3)]]) 
      elif siki == '2tf':
        table1 = html_data[1]
        for i in range(6):
          for j in range(5):
            odds_np = np.hstack([odds_np, table1.iloc[j, 1+(i*2)]])
        table2 = html_data[2]
        for i in range(5):
          for j in range(i, 5):
            odds_np = np.hstack([odds_np, table2.iloc[j, 1+(i*2)]])

  odds_np = odds_np.reshape(1, -1)
  return odds_np

## オッズのカラムを作成
def make_odds_cols():  
  cols = []
  for i in range(1, 7):
    for j in range(1, 7):
      if j == i:
        continue
      for k in range(1, 7):
        if k == i or k == j:
          continue
        col = '{}-{}-{}'.format(i, j, k)
        cols.append(col)
  for i in range(1, 5):
    for j in range(i+1, 6):
      for k in range(j+1, 7):
        col = '{}={}={}'.format(i, j, k)
        cols.append(col)
  for i in range(1, 7):
    for j in range(1, 7):
      if j == i:
        continue
      col = '{}-{}'.format(i, j)
      cols.append(col)
  for i in range(1, 6):
    for j in range(i+1, 7):
      col = '{}={}'.format(i, j)
      cols.append(col)
  return cols

## データセット全体を作成 (main)
def prepare_dataset(rno, jcd, hd):
  racedata = make_racedata(rno, jcd, hd)
  supdata = make_supdata(rno, jcd, hd)
  oddsdata = make_oddsdata(rno, jcd, hd)
  condata = np.concatenate([racedata, supdata], axis=1)

  cols = (["Waku_1", "Num_1", "Class_1", "Lastname_1", "Firstname_1", "Birth_1", "Branch_1", "Age_1", "Weight_1",               "F_1", "L_1", "ST_1", "zr_1", "z2r_1", "z3r_1", "tr_1", "t2r_1", "t3r_1", "m_num_1", "m2r_1", "m3r_1", "b_num_1", "b2r_1", "b3r_1",               "Ren1_1", "Ren2_1", "Ren3_1", "WST_1", "WSTJ_1",              "Waku_2", "Num_2", "Class_2", "Lastname_2", "Firstname_2", "Birth_2", "Branch_2", "Age_2", "Weight_2",               "F_2", "L_2", "ST_2", "zr_2", "z2r_2", "z3r_2", "tr_2", "t2r_2", "t3r_2", "m_num_2", "m2r_2", "m3r_2", "b_num_2", "b2r_2", "b3r_2",               "Ren1_2", "Ren2_2", "Ren3_2", "WST_2", "WSTJ_2",              "Waku_3", "Num_3", "Class_3", "Lastname_3", "Firstname_3", "Birth_3", "Branch_3", "Age_3", "Weight_3",               "F_3", "L_3", "ST_3", "zr_3", "z2r_3", "z3r_3", "tr_3", "t2r_3", "t3r_3", "m_num_3", "m2r_3", "m3r_3", "b_num_3", "b2r_3", "b3r_3",              "Ren1_3", "Ren2_3", "Ren3_3", "WST_3", "WSTJ_3",              "Waku_4", "Num_4", "Class_4", "Lastname_4", "Firstname_4", "Birth_4", "Branch_4", "Age_4", "Weight_4",               "F_4", "L_4", "ST_4", "zr_4", "z2r_4", "z3r_4", "tr_4", "t2r_4", "t3r_4", "m_num_4", "m2r_4", "m3r_4", "b_num_4", "b2r_4", "b3r_4",               "Ren1_4", "Ren2_4", "Ren3_4", "WST_4", "WSTJ_4",              "Waku_5", "Num_5", "Class_5", "Lastname_5", "Firstname_5", "Birth_5", "Branch_5", "Age_5", "Weight_5",               "F_5", "L_5", "ST_5", "zr_5", "z2r_5", "z3r_5", "tr_5", "t2r_5", "t3r_5", "m_num_5", "m2r_5", "m3r_5", "b_num_5", "b2r_5", "b3r_5",               "Ren1_5", "Ren2_5", "Ren3_5", "WST_5", "WSTJ_5",              "Waku_6", "Num_6", "Class_6", "Lastname_6", "Firstname_6", "Birth_6", "Branch_6", "Age_6", "Weight_6",               "F_6", "L_6", "ST_6", "zr_6", "z2r_6", "z3r_6", "tr_6", "t2r_6", "t3r_6", "m_num_6", "m2r_6", "m3r_6", "b_num_6", "b2r_6", "b3r_6",               "Ren1_6", "Ren2_6", "Ren3_6", "WST_6", "WSTJ_6",              "Lo1-1", "Lo1-2", "Lo1-3", "Lo1-4", "Lo1-5", "Lo1-6", "Lo2-1", "Lo2-2", "Lo2-3", "Lo2-4", "Lo2-5", "Lo2-6",               "Lo3-1", "Lo3-2", "Lo3-3", "Lo3-4", "Lo3-5", "Lo3-6", "Lo4-1", "Lo4-2", "Lo4-3", "Lo4-4", "Lo4-5", "Lo4-6",               "Lo5-1", "Lo5-2", "Lo5-3", "Lo5-4", "Lo5-5", "Lo5-6", "Lo6-1", "Lo6-2", "Lo6-3", "Lo6-4", "Lo6-5", "Lo6-6",               "Chosei_1", "Tenji_1", "Tilt_1", "Chosei_2", "Tenji_2", "Tilt_2", "Chosei_3", "Tenji_3", "Tilt_3",               "Chosei_4", "Tenji_4", "Tilt_4", "Chosei_5", "Tenji_5", "Tilt_5", "Chosei_6", "Tenji_6", "Tilt_6",               "Weather", "Wind", "Wave"])

  outdf = pd.DataFrame(condata, columns=cols)
  odds_cols=make_odds_cols()
  odds_outdf = pd.DataFrame(oddsdata, columns=odds_cols)

  return outdf, odds_outdf


# In[ ]:

if __name__ == '__main__':
  filename = './model.pkl'
  with open(filename, 'rb') as f:
    model = pickle.load(f)
  
  rno = sys.stdin.readline().strip()  # レースナンバー
  jcd = sys.stdin.readline().strip()  # レース場
  hd = sys.stdin.readline().strip()  # 日付
  select = sys.stdin.readline().strip()  # 買い目
  select = int(select)

  # rno = '1'  # レースナンバー
  # jcd = '05'  # レース場
  # hd = '20220401'  # 日付
  # select = 6  # 買い目
  # print(rno, jcd, hd, select)
  outdf, odds_outdf = prepare_dataset(rno, jcd, hd)

  drop_cols = (["Waku_1", "Lastname_1", "Firstname_1", "Birth_1", "Branch_1", "Age_1", "m_num_1", "b_num_1", "Waku_2", "Lastname_2", "Firstname_2", "Birth_2", "Branch_2", "Age_2",                 "m_num_2", "b_num_2",                   "Waku_3", "Lastname_3", "Firstname_3", "Birth_3", "Branch_3", "Age_3",                   "m_num_3", "b_num_3",                  "Waku_4", "Lastname_4", "Firstname_4", "Birth_4", "Branch_4", "Age_4",                  "m_num_4", "b_num_4",                  "Waku_5", "Lastname_5", "Firstname_5", "Birth_5", "Branch_5", "Age_5",                  "m_num_5", "b_num_5",                  "Waku_6", "Lastname_6", "Firstname_6", "Birth_6", "Branch_6", "Age_6",                  "m_num_6", "b_num_6",                  "Weather", "Wind", "Wave"])
  dataset = outdf.drop(columns=drop_cols)
  dataset = dataset.replace(['-'], np.nan)
  #dataset = dataset.dropna()
  weights = ["Weight_1", "Weight_2", "Weight_3", "Weight_4", "Weight_5", "Weight_6"]
  for weight in weights:
    #dataset[weight] = dataset[weight].apply(lambda x: x[:-2])
    dataset[weight] = dataset[weight].astype(float)
  classes = ["Class_1", "Class_2", "Class_3", "Class_3", "Class_4", "Class_5", "Class_6"]
  for cs in classes:
    le = LabelEncoder()
    le.fit(dataset[cs])
    dataset[cs] = le.transform(dataset[cs])
  predict_buy(dataset, odds_outdf, select)

