import streamlit as st
import numpy as np
import scipy
from scipy import optimize
import matplotlib.pyplot as plt

# --- 1. APP CONFIG & DARK THEME SETUP ---
st.set_page_config(page_title="Drill Cost Function Optimization App", layout="wide")

plt.style.use('dark_background')
plt.rcParams.update({
    "axes.facecolor": "#121214",
    "figure.facecolor": "#121214",
    "text.color": "#e4e4e7",
    "axes.labelcolor": "#fde047",
    "xtick.color": "#d4d4d8",
    "ytick.color": "#d4d4d8",
    "grid.color": "#27272a"
})

st.markdown("""
    <style>
    .stApp {
        background-color: #0f0e0e;
        color: #e4e4e7;
    }
    section[data-testid="stSidebar"] {
        background-color: #141416;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ Drill Cost Function Optimization App")
st.write("Adjust the model parameters below to observe changes in the drill cost function, surface plot, and optimization path[cite: 1].")

# --- SIDEBAR INPUTS ---
st.sidebar.header("Model Parameters")
W_op = st.sidebar.number_input("W_op (k lbs)", value=50.0)
N_op = st.sidebar.number_input("N_op (RPM)", value=65.0)
well_depth = st.sidebar.number_input("Well Depth (ft)", value=11300.0)
rig_cost = st.sidebar.number_input("Rig Cost ($/hr)", value=1250.0)
bit_size = st.sidebar.number_input("Bit Size (in)", value=8.5)
bit_cost = st.sidebar.number_input("Bit Cost ($)", value=309.56)
trip_time = st.sidebar.number_input("Trip Time (hrs)", value=7.3)
run_time = st.sidebar.number_input("Run Time (hrs)", value=12.3)
R_i = st.sidebar.number_input("R_i (ft)", value=150.0)
R_f = st.sidebar.number_input("R_f (ft)", value=115.0)
H_f = st.sidebar.number_input("H_f (ft/ft)", value=0.875)

st.sidebar.header("5-spot Test Values")
W_1 = st.sidebar.number_input("W_values[1] (k lbs)", value=35.0)
W_2 = st.sidebar.number_input("W_values[2] (k lbs)", value=50.0)
W_3 = st.sidebar.number_input("W_values[3] (k lbs)", value=35.0)
W_4 = st.sidebar.number_input("W_values[4] (k lbs)", value=50.0)

N_1 = st.sidebar.number_input("N_values[1] (RPM)", value=80.0)
N_2 = st.sidebar.number_input("N_values[2] (RPM)", value=80.0)
N_3 = st.sidebar.number_input("N_values[3] (RPM)", value=150.0)
N_4 = st.sidebar.number_input("N_values[4] (RPM)", value=150.0)

R_1 = st.sidebar.number_input("R_values[1] (ft)", value=18.0)
R_2 = st.sidebar.number_input("R_values[2] (ft)", value=25.0)
R_3 = st.sidebar.number_input("R_values[3] (ft)", value=27.0)
R_4 = st.sidebar.number_input("R_values[4] (ft)", value=36.0)

W_values = [42.0, W_1, W_2, W_3, W_4]
N_values = [120, N_1, N_2, N_3, N_4]
R_values = [24, R_1, R_2, R_3, R_4]

# --- INTERMEDIATE VARIABLES & FUNCTIONS ---
C2 = (R_i / 3 - R_f / 3) / (R_f / 3 * H_f)
M1 = (R_values[1] * W_values[2] - R_values[2] * W_values[1]) / (R_values[1] - R_values[2])
M2 = (R_values[3] * W_values[4] - R_values[4] * W_values[3]) / (R_values[3] - R_values[4])
M = (M1 + M2) / 2
l1 = (np.log10(R_values[1] / R_values[4]) / np.log10(N_values[1] / N_values[4]))
l2 = (np.log10(R_values[2] / R_values[3]) / np.log10(N_values[2] / N_values[3]))
l = (l1 + l2) / 2
K = ((1 + C2 / 2 * H_f) * (R_i + R_f) / N_op**l / (W_op - M) / run_time)
D1 = (1 / bit_size)
A_f = (1_000 * (-D1 * W_op + 10) / (3 + 3) / (2 * N_op + 0.000087 * N_op**3) * (H_f + 6 / 2 * H_f**2))
E1 = (bit_cost + rig_cost * trip_time)
E2 = (1_000 / A_f * (1 + 6 / 2))
E3 = (1_000 * K / A_f * (6 / C2 + (C2 - 6) / C2**2 * np.log(1 + C2)))

def drill_cost(x):
    return (E1 + rig_cost * E2 * (-D1 * x[0] + 10) / (2 * x[1] + 0.000087 * x[1]**3)) / (
            E3 * (x[0] - M) * (-D1 * x[0] + 10) / (2 * x[1]**(1 - l) + 0.000087 * x[1]**(3 - l)))

# --- RUN OPTIMIZATION ---
x0 = np.array([70.0, 85.0])
res = scipy.optimize.fmin_bfgs(drill_cost, x0, disp=False, retall=True)

optimal_params = res[0]
optimal_cost = drill_cost(optimal_params)

listx = [res[1][i][0] for i in range(len(res[1]))]
listy = [res[1][i][1] for i in range(len(res[1]))]

# --- DISPLAY OPTIMIZATION METRICS ---
st.subheader("🎯 Optimization Results")
m1, m2, m3 = st.columns(3)
m1.metric("Optimal Drill Cost", f"${optimal_cost:,.2f} / ft")
m2.metric("Optimal Weight on Bit (W)", f"{optimal_params[0]:,.2f} k lbs")
m3.metric("Optimal Rotary Speed (N)", f"{optimal_params[1]:,.2f} RPM")

st.markdown("---")

# --- PLOTS ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Surface Plot")
    x = np.arange(30, 80)
    y = np.arange(50, 120)
    xgrid, ygrid = np.meshgrid(x, y)
    xy = np.stack([xgrid, ygrid])

    fig1 = plt.figure(figsize=(8, 6))
    ax1 = fig1.add_subplot(111, projection='3d')
    ax1.view_init(45, -90)
    surf = ax1.plot_surface(xgrid, ygrid, drill_cost(xy), cmap='inferno')
    ax1.set_xlabel('x (W - k lbs)')
    ax1.set_ylabel('y (N - RPM)')
    ax1.set_zlabel('drill_cost ($/ft)')
    fig1.colorbar(surf, shrink=0.5, aspect=7)
    st.pyplot(fig1)

with col2:
    st.subheader("Contour Plot & Optimization Path")
    i1 = np.arange(30, 80, 3)
    i2 = np.arange(50, 120, 3)
    x1_mesh, x2_mesh = np.meshgrid(i1, i2)
    f_mesh = (E1 + rig_cost * E2 * (-D1 * x1_mesh + 10) / (2 * x2_mesh + 0.000087 * x2_mesh**3)) / (E3 * (x1_mesh - M) * (-D1 * x1_mesh + 10) / (2 * x2_mesh**(1 - l) + 0.000087 * x2_mesh**(3 - l)))
    
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    lines = range(1, 52, 1)
    CS = ax2.contour(x1_mesh, x2_mesh, f_mesh, lines, cmap='plasma')
    ax2.clabel(CS, inline=1, fontsize=8)
    ax2.set_title('Drill cost function contour plot')
    ax2.set_xlabel('W (k lbs)')
    ax2.set_ylabel('N (rpm)')
    ax2.plot(listx, listy, 'r-o', label='Optimization Path')
    ax2.legend(loc='upper right')
    st.pyplot(fig2)
