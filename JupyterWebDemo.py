#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import libraries
from ipywidgets.widgets import Label, FloatProgress, FloatSlider, Button
from ipywidgets.widgets import Layout, HBox, VBox
from IPython.display import display
import numpy as np
import bqplot as bq
import time
import threading


# In[2]:


# flag to control
flag = True

# data to plot
x = np.linspace(0, 2*np.pi, 500)
dx = x[1] - x[0]
y = 1 + np.sin(x)


# In[3]:


# GUI elements
# STOP button to stop the app
b_stop = Button(
    description='Stop',
    icon='stop',
    button_style='warning',
    layout=Layout(width='120px')
)

def stop_click(b):
    global flag
    flag = False
    
b_stop.on_click(stop_click)

# progreess bar
p1 = FloatProgress(
    value=y[-1],
    min=0,
    max=2,
    description='PV:',
    style={'description_width': 'initial'},
    layout=Layout(width='375px')
)
p2 = Label(
    value=str(np.round(y[-1],2)),
    layout=Layout(margin='0 10px 0 31px')
)

p12= HBox(
    children=(p1,p2),
    layout=Layout(margin='0 10px 0 31px')
)

# slider 
pA = FloatSlider(
    value=0,
    min=0,
    max=0.5,
    step=0.01,
    description='Noise:',
    layout=Layout(width='500px',margin='0 0 5px 0')  
)


# In[4]:


# plot elements

x_scale = bq.LinearScale()
y_scale = bq.LinearScale()

# axis
x_ax = bq.Axis(
    label='x(t)',
    scale=x_scale
)
y_ax = bq.Axis(
    label='y(t)',
    scale=y_scale,
    orientation='vertical'
)

#Lines

Line = bq.Lines(
    x=x,
    y=y,
    scales={'x':x_scale, 'y':y_scale}
)

# Figure
fig = bq.Figure(
    layout=Layout(width='500px', height='300px'),
    axes=[x_ax,y_ax],
    marks=[Line],
    fig_margin=dict(top=10,bottom=10,left=50, right=10)
)


# In[5]:


#join everything
box = VBox(
    children=(fig, p12, pA),
    layout=Layout(border='solid 3px gray', width='510px')
)
app = VBox(
    children=(b_stop, box)
)


# In[6]:


# LOOPING FUNCTION

def work():
    global x
    global y
    
    while flag:
        # get latest value of slider
        A = pA.value
        
        x = np.delete(x, 0)
        y = np.delete(y, 0)
        
        x= np.append(x, x[-1]+dx)
        noise = A*np.random.rand()
        y = np.append(y, 1 + np.sin(x[-1]) + noise)
        
        p1.value = y[-1]
        p2.value = str(np.round(y[-1],2))
        
        Line.x = x
        Line.y = y
        
        time.sleep(0.05)


# In[8]:


flag = True

thread = threading.Thread(target=work)

display(app)

thread.start()


# In[ ]:




