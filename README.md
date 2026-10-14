# ⚡ Drill Cost Function Optimization App

An interactive Python application built with **Streamlit**, **SciPy**, and **Matplotlib** to optimize drilling parameters (Weight on Bit and Rotary Speed) for minimum cost per foot using the **BFGS optimization algorithm**[cite: 5].

---

## 📋 Overview
Optimizing drilling parameters to reduce the costs associated with drilling and completing wells is vital for maximizing profitability in the oil and gas industry[cite: 5]. Formulating accurate models for a drilling cost function requires balancing the economic trade-offs between penetration rate and bit life[cite: 5]. 

This application implements a mathematical model developed by Humble Oil and Refining Co. (and reviewed by Cristina M. Ruse), integrating tooth and bearing wear solutions alongside variable weight and rotary speed schedules[cite: 5]. It utilizes the **BFGS (Broyden-Fletcher-Goldfarb-Shanno) Quasi-Newton method** from `scipy.optimize` to find the unique minimum of the drilling cost function efficiently without calculating a complex Hessian matrix[cite: 5].

---

## ✨ Key Features
* **Interactive Parameter Controls:** Adjust operational inputs, rig costs, bit specifications, and offset well (5-spot test) data via a user-friendly Streamlit sidebar.
* **Automated Optimization:** Employs `scipy.optimize.fmin_bfgs` to compute the optimal Weight on Bit ($W$) and Rotary Speed ($N$) alongside the minimum drill cost per foot[cite: 5].
* **Dynamic Visualizations:** 
  * Renders a 3D surface plot of the drill cost function.
  * Generates a 2D contour plot tracking the exact optimization path taken by the BFGS algorithm across iterations.
* **Dark Mode Aesthetics:** Fully styled with a modern dark theme interface and customized charts for clean data presentation.

---

## 🛠️ Tech Stack & Libraries
* **Python**[cite: 5]
* **Streamlit** (Web framework & UI)
* **SciPy (`scipy.optimize.fmin_bfgs`)** (Numerical optimization)[cite: 5]
* **NumPy** (Mathematical array operations and mesh grids)[cite: 5]
* **Matplotlib** (3D surface mapping and 2D contour visualization)[cite: 5]

---

## 🚀 Getting Started Locally

### 1. Prerequisites
Ensure you have Python installed, then install the required dependencies:
```bash
pip install streamlit numpy scipy matplotlib

```

### 2. Run the App

Clone the repository, save the application code as `app.py`, and run the following command in your terminal:

```bash
streamlit run app.py

```

---

## 📐 Mathematical Model Background

The objective function minimizes the **Cost-Per-Foot** model:

$$\text{Cost, \$/ft} = \frac{\text{Bit Cost} + (\text{Rig Operating Cost} \times \text{Trip Time}) + (\text{Rig Operating Cost} \times \text{Rotating Time})}{\text{Footage Drilled}}$$

By treating the system as an unconstrained nonlinear optimization problem, the BFGS algorithm evaluates the smooth, differentiable cost function to locate the global minimum cost per foot.

