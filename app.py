from cmd import PROMPT
import streamlit as st
import random
import joblib
import matplotlib.pyplot as plt
import math
from stylia.colors.colors import NamedColors

#st.title("Fast Forward Cohort Network")

plt.rcParams['figure.facecolor'] = '#273346'

EDGES_FILE = "edges.joblib"
PROMPT_FILE = "prompt.joblib"
FROM_PERSON_FILE = "fromperson.joblib"

people = [
    "Ngan",
    "Danny",
    "Steven",
    "Adrian",
    "Miquel",
    "Gemma",
    "Achint",
    "Jessica",
    "Chris",
    "Nathan",
    "Michael",
    "Diana"
]

prompts = [
    "In one year, I see them...",
    "In ten years, I see them...",
    "An inspiring fact about their tech nonprofit is...",
    "Their pitch is powerful because...",
    "The biggest change I've seen in them is...",
    "Describe their product in one line",
    "The main strength of their tech nonprofit is...",
    "One word to describe their tech nonprofit",
    "I would like to know more about their...",
    "I thank you for...",

]

def circles(c_list, n):
    g_d_list = []  # graph data list
    for g in c_list:
        # create length of circle list. In this instance
        # i'm multiplying by 8 each time but could be any number.
        lg = [g] * (n*g)
        ang = 360/len(lg)  # calculate the angle of each entry in circle list.
        ang_list = []
        for i in range(len(lg)+1):
            ang_list.append(ang*i)
        for i, c in enumerate(lg):
            # calculate the x and y axis points or each circle. in this instance
            # i'm expanding circles by multiples of ten but could be any number.
            x_axis = 0 + (10*g) * math.cos(math.radians(ang_list[i+1]))
            y_axis = 0 + (10*g) * math.sin(math.radians(ang_list[i+1]))
            # tuple structure ((axis tuple), circle size, circle colour)
            g_d_list.append(((x_axis, y_axis), 1, '#273346'))
    return g_d_list

def plot(people_nodes, edges):
    g_d_list = [people_nodes[k] for k in people]
    fig, ax = plt.subplots(1,1, figsize=(10,10))
    for c in range(len(g_d_list)):
        circle = plt.Circle(g_d_list[c][0], radius=g_d_list[c][1], fc=g_d_list[c][2], zorder=10000)
        ax.add_patch(circle)
    for k,v in people_nodes.items():
        ax.text(v[0][0], v[0][1], k, ha="center", va="center", color='white', zorder=1000000)
    
    for e in edges:
        n1 = people_nodes[e[0]][0]
        n2 = people_nodes[e[1]][0]
        ax.plot([n1[0], n2[0]], [n1[1], n2[1]], color="white", lw=0.8, zorder=1)
    ax.set_facecolor("black")
    plt.axis('scaled')
    plt.axis('off')  # optional if you don't want to show axis
    return fig

# nodes
nodes = circles([1], len(people))
people_nodes = dict((k, nodes[i]) for i,k in enumerate(people))

# edges
cols = st.columns(4)

if cols[0].button("Random person"):
    from_person = random.choice(people)
    joblib.dump(from_person, FROM_PERSON_FILE)

from_person = joblib.load(FROM_PERSON_FILE)

cols[0].write(from_person)

if from_person != "...":
    to_person = cols[1].selectbox("Pulls a thread to...", options=people)

if cols[2].button('Random thread'):
    prompt = random.choice(prompts)
    joblib.dump(prompt, PROMPT_FILE)

prompt = joblib.load(PROMPT_FILE)
st.subheader(prompt)

edges = joblib.load(EDGES_FILE)
if cols[3].button('Connect'):
    edges += [(from_person, to_person)]

joblib.dump(edges, EDGES_FILE)
fig = plot(people_nodes, edges)

st.pyplot(fig)


cols = st.columns(3)
if cols[0].button("Migrate"):
    random.shuffle(people)
    edges = []
    joblib.dump(edges, EDGES_FILE)
    joblib.dump("...", PROMPT_FILE)
    joblib.dump("...", FROM_PERSON_FILE)

if cols[1].button("Save figure"):
    plt.savefig("network.png", dpi=600)