import streamlit as st
import numpy as np
import math
import matplotlib.pyplot as plt
from sympy import symbols, diff, evalf, sin,exp
from mpl_toolkits import mplot3d
import torch


st.title("Approximating univariate functions using Taylor series")


f = st.sidebar.radio("Univariate Functions",["sinx","exp(x)","coshx"])

n = st.slider("Select highest degree of Taylor polynomial.",min_value=0,max_value=10)
a = st.slider("Select the point for the approximation to be centered about.",min_value=-2,max_value=2,value=0)

x = [i*0.1 for i in range(-44,45)]
x = np.array(x)


def derivative(x,y,n):
    if (n==1):
        return np.gradient(y,x)
    else:
        return np.gradient(derivative(x,y,n-1),x)


def taylor_approx_1D(func,n,a,xi):
    y = func(x)
    ans = func(a)
    for i in range(1,n+1):
        dy_dx = derivative(x,y,n=i)
        ans += (dy_dx[x==a]*((xi-a)**i))/math.factorial(i)
    return ans

def plot_func(func,n,x,a):
    fig,ax = plt.subplots()
    f_values = []
    for xi in x:
        f_values.append(taylor_approx_1D(func,n,a,xi))
    f_true = [func(xi) for xi in x]
    plt.figure()
    ax.plot(x,f_values)
    ax.plot(x,f_true)
    if func==np.sin:
        ax.set_ylim(-2.5,2.5)
    else:
        ax.set_ylim(-0.5,5)
    st.pyplot(fig)


if f=="sinx":
    plot_func(np.sin,n,x,a)
elif f=="coshx":
    plot_func(np.cosh,n,x,a)
else:
    plot_func(np.exp,n,x,a)


st.title("Approximating bivariate functions using Taylor series")

f2 = st.sidebar.radio("Bivariate functions",["Parabolic(Z = X^2 + Y^2)","Himmelblau"])

n1 = st.slider("Select order of approximation",min_value=0,max_value=10)
a1 = st.slider("Select X-coordinate for the approximation to be centered about.",min_value=-2,max_value=2,value=1)
b1 = st.slider("Select Y-coordinate for the approximation to be centered about.",min_value=-2,max_value=2,value=1)


x1 = np.linspace(-4,4,100)
y1 = np.linspace(-4,4,100)

X,Y = symbols(["X","Y"])


# def partial_derivative(expr,a1,b1,var,n1):
#     dz_dx = diff(expr,var,n1)  # Differentiating expr with respect to var
#     evaluated = dz_dx.evalf(subs={X:a1,Y:b1})
#     return evaluated
def partial_derivative(expr, a1, b1, var, n1):
    X = torch.tensor(a1, requires_grad=True)
    Y = torch.tensor(b1, requires_grad=True)
    if var == 'X':
        z = expr.subs('X', X).subs('Y', Y)
    elif var == 'Y':
        z = expr.subs('Y', Y).subs('X', X)
    else:
        raise ValueError("var should be 'X' or 'Y'")

    for _ in range(n1):
        if var == 'X':
            dz_dx = torch.autograd.grad(z, X)[0]
        else:
            dz_dx = torch.autograd.grad(z, Y)[0]
        z = dz_dx

    if var == 'X':
        result = dz_dx.subs('X', a1).subs('Y', b1)
    else:
        result = dz_dx.subs('Y', b1).subs('X', a1)

    return result.item() if isinstance(result, torch.Tensor) else result


def taylor_approx_2D(expr,a1,b1,n1,xi,yi):
    ans = expr.evalf(subs={X:a1,Y:b1})
    for i in range(1,n1+1):
        ans += (partial_derivative(expr,a1,b1,X,i)*((xi-a1)**i) + partial_derivative(expr,a1,b1,Y,i)*((yi-b1)**i))/math.factorial(i)
    return ans

def plot_2D(expr,a1,b1,n1,x1,y1):
    X1,Y1 =np.meshgrid(x1,y1)
    Z_true=[]
    Z_values=[]
    for i in range(len(X1)):
        for j in range(len(Y1)):
            z = expr.evalf(subs={X:x1[i],Y:y1[j]})
            Z_true.append(z)
            Z_values.append(taylor_approx_2D(expr,a1,b1,n1,x1[i],y1[j]))
    Z_true = np.array(Z_true)
    Z_values = np.array(Z_values)
    Z_values = Z_values.reshape(X1.shape)
    Z_true = Z_true.reshape(X1.shape)
    
    fig = plt.figure(figsize=(10,4))
    if expr == (X**2 +Y-11)**2 + (X+Y**2 -7)**2:
        ax = fig.add_subplot(121,projection="3d")
        ax.plot_surface(X1,Y1,Z_true,cmap="plasma")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_zlim(-10,350)
        ax = fig.add_subplot(122,projection="3d")
        ax.plot_surface(X1,Y1,Z_values,cmap="plasma")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_zlim(-10,350)
    else:
        ax = plt.axes(projection="3d")
        ax.plot_surface(X1,Y1,Z_true,cmap="plasma")
        ax.plot_surface(X1,Y1,Z_values)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_zlim(-10,50)
    ax.view_init(elev=20, azim=30)
    st.pyplot(fig)

    

if f2 == "Himmelblau":
    expr2 = (X**2 +Y-11)**2 + (X+Y**2 -7)**2
    plot_2D(expr2,a1,b1,n1,x1,y1)
else:
    expr1 = X**2 + Y**2
    plot_2D(expr1,a1,b1,n1,x1,y1)


