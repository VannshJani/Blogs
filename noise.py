import streamlit as st
import random
from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt
from math import factorial as f




st.title("Noisy Channel Coding")

nbits = st.number_input("Enter the number of bits", min_value=1, max_value=100, value=4, step=1)

bits = st.text_input("Enter the bits", value="1010")

def transmit(bits, bit_prob):
    noisy_bits = ""
    for bit in bits:
        if random.random() < bit_prob:
            if bit == '0':
                noisy_bits += '1'
            else:
                noisy_bits += '0'
        else:
            noisy_bits += bit
    return noisy_bits

def decode(bits, n):
    decoded_bits = ""
    for i in range(0, len(bits), n):
        bit = bits[i:i+n]
        if bit.count('1') > bit.count('0'):
            decoded_bits += '1'
        else:
            decoded_bits += '0'
    return decoded_bits
def nck(n,k):
    if (n<k):
        return
    return f(n)/(f(k)*f(n-k))

# n is number of repeatations of each bit
# p is bit probability error when n=1
def bit_probability_error(n,p):
    min_bits = (n+1)//2
    prob_sum = 0
    for bits in range(min_bits,n+1):
        n_choose_k = nck(n,bits)
        prob_sum += n_choose_k * (p**bits) * ((1-p)**(n-bits))
    return prob_sum
def channel_capacity(p):
        return 1 - (p*np.log2(1/p) + (1-p)*np.log2(1/1-p))
def f1(p,c):
    x = np.linspace(c,1.0,10)
    m = p/(1-c)
    return m*(x-c)
def plot_achievable(c,p):
    fig, ax = plt.subplots()
    x1 = np.linspace(c,1.0,10)
    x2 = np.linspace(0,c,10)
    y1 = f1(bit_prob,c)
    y2 = np.zeros(x2.shape)
    ax.plot(x2,y2,color="orange")
    ax.plot(x1,y1,color="orange")
    ax.set_xlabel("Rate")
    ax.set_ylabel("Bit Probability error")
    ax.set_title('Rate vs Bit Probability error')
    x = np.concatenate((x2,x1))
    y = np.concatenate((y2,y1))
    ax.fill_between(x, y, max(y), where=(y <= max(y)), color='blue', alpha=0.3,label="Achievable")
    ax.fill_between(x1, y1, color='red', alpha=0.3, label="Not-Achievable")
    ax.scatter(c, 0, color='black', label='Channel-Capacity',s=30)
    ax.legend()
    st.pyplot(fig)
    st.set_option('deprecation.showPyplotGlobalUse', False)

if (len(bits) != nbits):
    st.warning("The number of bits entered does not match the number of bits specified.")
else:
    bit_prob = st.slider("Enter the probability of bit error", min_value=0.1, max_value=1.0, value=0.2, step=0.1)
    n = st.number_input("Select value of n for Rn strategy", min_value=1, max_value=21, value=3, step=2)
    encoded_bit = ""
    for bit in bits:
        encoded_bit += bit*n
    st.write("The original message is", bits)
    st.write("The encoded message is",encoded_bit)
    transmitted_bits = transmit(encoded_bit, bit_prob)
    st.write("The transmitted message is", transmitted_bits)
    decoded_bits = decode(transmitted_bits, n)
    st.write("The decoded message is", decoded_bits)

    fig, ax = plt.subplots()
    n_range = np.arange(1,22,2)
    rate = 1/n_range
    reduced_probability = [bit_probability_error(i,bit_prob) for i in n_range]
    reduced_probability = np.array(reduced_probability)
    interp = interp1d(rate, reduced_probability, kind='cubic')
    fine_rate = np.linspace(rate.min(), rate.max(), 5000)
    smooth_reduced_probability = interp(fine_rate)
    ax.plot(fine_rate, smooth_reduced_probability, color='b')
    ax.scatter(rate, reduced_probability, color='r',  marker='o')
    for i in range(8):
        ax.annotate(f"n={i+1}",(rate[i],reduced_probability[i]),textcoords="offset points",xytext=(-30,4),ha="left")
    ax.set_xlabel('Rate')
    ax.set_ylabel('Bit Probability error')
    ax.set_title('Rate vs Bit Probability error')
    ax.grid(True)
    st.pyplot(fig)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    c = channel_capacity(bit_prob)
    plot_achievable(c,bit_prob)
    