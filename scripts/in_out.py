from tkinter import *
import pandas as pd
import numpy as np
import pickle

def set_color(serve):
   if serve:
      root.configure(background = ['green'])
   else:
      root.configure(background = ['red'])

labels = ['IMU','index','Xacc', 'Yacc', 'Zacc', 'Xori', 'Yori', 'Zori', 'Xmag', 'Ymag' , 'Zmag', 'Xgyro', 'Ygyro', 'Zgyro', 'Xrot','Yrot', 'Zrot' , 'Xlin' ,'Ylin', 'Zlin', 'Xgrav', 'Ygrav', 'Zgrav']

filename = "../data/SERVE_20_03_2023_13-41-50"

file = filename+'.csv'
webcamFileName = filename+'_webcam.csv'
df_imu = pd.read_csv(file,skiprows=4,header=None,names=labels)
df_cam = pd.read_csv(webcamFileName,names=['index','x','y'])

df = pd.merge(df_imu, df_cam, on='index')

df_imu1 = df.loc[df['IMU'] == 1]
df_imu1.columns = ['IMU','index','X1acc', 'Y1acc', 'Z1acc', 'X1ori', 'Y1ori', 'Z1ori', 'X1mag', 'Y1mag' , 'Z1mag', 'X1gyro', 'Y1gyro', 'Z1gyro', 'X1rot','Y1rot', 'Z1rot' , 'X1lin' ,'Y1lin', 'Z1lin', 'X1grav', 'Y1grav', 'Z1grav', 'Xcam', 'Ycam']
df_imu2 = df.loc[df['IMU'] == 2]
df_imu2.columns = ['IMU','index','X2acc', 'Y2acc', 'Z2acc', 'X2ori', 'Y2ori', 'Z2ori', 'X2mag', 'Y2mag' , 'Z2mag', 'X2gyro', 'Y2gyro', 'Z2gyro', 'X2rot','Y2rot', 'Z2rot' , 'X2lin' ,'Y2lin', 'Z2lin', 'X2grav', 'Y2grav', 'Z2grav', 'Xcam', 'Ycam']

merged_df = pd.merge(df_imu1, df_imu2, on='index')
merged_df.drop(columns=['index', 'IMU_x'], inplace=True)

serve_data = np.array(merged_df.to_numpy())

print(f'Data Loaded. {serve_data.shape}')

model_file = '../models/rf.sav'
model = pickle.load(open(model_file, 'rb'))

print('Pre-trained model weights loaded.')

root = Tk()
root.title("Serve In or Out")
root.resizable(False, False)
root.attributes("-fullscreen", True)

serve = model.predict(np.array([serve_data]).reshape(1, -1))[0]
print(f'Serve outcome predicted: {serve}')

set_color(serve)

root.mainloop()