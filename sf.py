import streamlit as st
import graphviz
import pandas as pd
import numpy as np
import heapq

st.title("Shannon Fano Encoding")
sentence = st.text_input("Enter text to be encoded",value = "aaaaaaaabbbbccd")

def generate_prob(sentence):
    d={}
    special=0
    for c in sentence:
        if c=="," or c==".":
            special+=1
            continue
        elif c.lower() in d:
            d[c.lower()] += 1
        else:
            d[c.lower()] = 1
    total_char = len(sentence)-special
    for key in d:
        d[key] = d[key]/total_char
    return d
seq = generate_prob(sentence)
seq=sorted(seq.items(),key=lambda item: item[1], reverse=True)
d = dict(seq)

class Node:
    def __init__(self,char,prob):
        self.char=char
        self.p=prob
        self.code=""
        self.left=None
        self.right=None

initial=""
for c in seq:
    initial+=c[0]
root = Node(initial,1)


def split(node):
    left_subset={}
    right_subset={}
    total_p = node.p
    half_p = total_p/2
    sum=0
    index = 0
    seq=node.char
    for c in seq:
        if sum>=half_p:
            break
        sum+=d[c]
        index+=1
    left_char = seq[:index]
    right_char = seq[index:]
    for l in left_char:
        left_subset[l]=d[l]
    for r in right_char:
        right_subset[r]=d[r]
    return left_subset,right_subset

symbols=[root.char]
prob = [root.p]
def Build_tree(root):
    if len(root.char)==1:
        return
    left_subset,right_subset = split(root)
    left_char=""
    right_char=""

    for c in left_subset:
        left_char+=c
    for cr in right_subset:
        right_char+=cr
    left_prob = sum(left_subset.values())
    right_prob = sum(right_subset.values())

    left_node = Node(char=left_char,prob=left_prob)
    right_node = Node(char=right_char,prob=right_prob)
    root.left = left_node
    root.right = right_node
    symbols.append(left_node.char)
    prob.append(left_node.p)
    Build_tree(left_node)
    symbols.append(right_node.char)
    prob.append(right_node.p)
    Build_tree(right_node)

Build_tree(root)

def assign_codes(root):
    if root.left is None and root.right is None:
        return
    if root.left is not None:
        root.left.code = "0" + root.code
    if root.right is not None:
        root.right.code = "1" + root.code
    assign_codes(root.left)
    assign_codes(root.right)
assign_codes(root)

total_bits=0
data={"Character":[],"Probability":[],"Code":[]}
def print_codes(root):
    global total_bits
    if root is not None:
        if (len(root.char)==1):
          total_bits += len(root.code)*sentence.count(root.char)
          data["Character"].append(root.char)
          data["Probability"].append(root.p)
          data["Code"].append(root.code)
        print_codes(root.left)
        print_codes(root.right)
print_codes(root)

df = pd.DataFrame(data)
st.dataframe(df)
done=False
prob[0] = float(prob[0])
for p in range(len(prob)):
    prob[p] = round(prob[p],3)
if 'count' not in st.session_state:
    st.session_state.count = 0
if 'dot' not in st.session_state:
    st.session_state.dot = graphviz.Digraph()
st.session_state.dot.node(str(symbols[0])+str(" ")+str(prob[0]))

def entropy(data):
    chars = data['Character']
    prob = data['Probability']
    code = data["Code"]
    sum=0
    for i in range(len(chars)):
        sum += -prob[i]*np.log2(prob[i])
    return sum

def cross_entropy(data):
    chars = data['Character']
    prob = data['Probability']
    code = data["Code"]
    sum=0
    for i in range(len(chars)):
        sum += -prob[i]*np.log2(1/(2**(len(code[i]))))
    return sum

st.write("Entropy is ",entropy(data))
st.write("Cross entropy for Shannon-Fano is ",cross_entropy(data))

def KL_divergence(ce,e):
    return ce-e
st.write("KL Divergence for Shannon-Fano is ",KL_divergence(cross_entropy(data),entropy(data)))
st.write("---")


s = 'aaaaaaaabbbbccd'
s = s.lower()
s_len = 0
arr = [0]*26
d1 = {}
for i in range(len(s)):
  if(s[i]==' ' or s[i]==',' or s[i]=='.' or s[i]==';'):
    continue
  s_len+=1
  arr[ord(s[i])-ord('a')]+=1
for i in range(len(arr)):
  if arr[i]!=0:
    d1[chr(i+ord('a'))] = arr[i]

class Node1:
    def __init__(self, freq, symbol, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right
        self.huff = ''
    
    def __lt__(self, nxt):
        return self.freq < nxt.freq


codes = {}

def huffman_codes(node, val=''):
    newVal = val + str(node.huff)
    if not node.left and not node.right:
        # print(f"{node.symbol} -> {newVal}")
        codes[node.symbol] = newVal
    else:
        huffman_codes(node.left, newVal)
        huffman_codes(node.right, newVal)

chars = list(d1.keys())
freq = list(d1.values())
nodes = []
for x in range(len(chars)):
    heapq.heappush(nodes, Node1(freq[x], chars[x]))

while len(nodes) > 1:
    left = heapq.heappop(nodes)
    right = heapq.heappop(nodes)
    left.huff = '0'
    right.huff = '1'
    new_symbol = left.symbol + right.symbol
    new_freq = left.freq + right.freq
    new_node = Node1(new_freq, new_symbol, left, right)
    heapq.heappush(nodes, new_node)

huffman_tree_root = nodes[0]
huffman_codes(huffman_tree_root)


prob1 = {}
sum_p = 0

for i in range(len(codes)):
  prob1[list(codes.keys())[i]] = d1[list(codes.keys())[i]]/s_len
  sum_p += prob1[list(codes.keys())[i]]

q = {} # Stores q values needed to find cross entropy
for i in range(len(codes)):
  q[list(codes.keys())[i]] = np.log2(1/(2**(len(codes[list(codes.keys())[i]]))))
cross_entropy1 = 0
sym = list(q.keys())
lq = list(q.values())
for i in range(len(sym)):
  cross_entropy1 += -1*prob1[sym[i]]*q[sym[i]]

entropy1 = 0

for i in range(len(sym)):
  entropy1 += -1*prob1[sym[i]]*np.log2(prob1[sym[i]])
st.write("Cross entropy for Huffman is ",cross_entropy1)
st.write("KL Divergence for Huffman is ",cross_entropy1-entropy1)
st.write("KL Divergence of Huffman is lesser than that of Shannon-Fano")
st.write("---")
st.header("Binary Tree")
if st.button("next",type="primary"):
    st.session_state.count += 1
    if st.session_state.count>=len(symbols):
        st.write("Done")
        done=True
    else:
        st.session_state.dot.node(str(symbols[st.session_state.count])+str(" ")+str(prob[st.session_state.count]))
        parent = ""
        for i in range(st.session_state.count-1,-1,-1):
                if symbols[st.session_state.count] in symbols[i]:
                    parent = symbols[i]
                    parent_prob = prob[i]
                    break
        if st.session_state.count%2==0:
            label="1"
        else:
            label = "0"
        st.session_state.dot.edge(str(parent)+str(" ")+str(parent_prob), str(symbols[st.session_state.count])+str(" ")+str(prob[st.session_state.count]),label=label)
            
st.session_state.dot.save('test.png')
st.graphviz_chart(st.session_state.dot,use_container_width=True)
if done:
    del st.session_state.count
    del st.session_state.dot


