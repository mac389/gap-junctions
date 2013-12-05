import utils as tech
import matplotlib.pyplot as plt

from brian import *
from numpy.random import random_sample

N = 10
v0=1.05
tau=10*ms

eqs = '''
dv/dt=(v0-v+Igap)/tau : 1
Igap : 1 # gap junction current
'''

neurons = NeuronGroup(N, model=eqs, threshold=1, reset=0)
neurons.v=linspace(0,1,N)
trace = StateMonitor(neurons, 'v', record=True)
stimulus = StateMonitor(neurons,'Igap',record=True)
raster = SpikeMonitor(neurons,record=True)
S=Synapses(neurons,model='''w:1 # gap junction conductance
                            Igap=w*(v_pre-v_post): 1''')
S[:,:]=True #Every neuron is connected to every other neuron
neurons.Igap=S.Igap
g=0.1*random_sample(size=(N*N,))
S.w=g

run(500*ms)

#Better file management add a .info file
savetxt('stimulus.data',stimulus.values, fmt='%.04f', delimiter='\t')
savetxt('voltages.data',trace.values, fmt = '%.04f',delimiter = '\t')

vmin = -1#min(trace.values.min(), stimulus.values.min())
vmax = 1# max(trace.values.max(), stimulus.values.max())

fig,(voltages,stim) = plt.subplots(nrows=2,ncols=1,sharex=True)
voltages.imshow(trace.values,interpolation='nearest',aspect='auto', 
		vmin = vmin,vmax = vmax, cmap = plt.cm.binary)
tech.adjust_spines(voltages)
voltages.set_xlabel(tech.format('Time (ms)'))
voltages.set_ylabel(tech.format('Neuron'))

im = stim.imshow(stimulus.values, interpolation='nearest',aspect='auto', 
		vmin=vmin, vmax=vmax,cmap = plt.cm.binary)

fig.tight_layout()
fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
fig.colorbar(im, cax=cbar_ax)
tech.adjust_spines(stim)
stim.set_xlabel(tech.format('Time (ms)'))
stim.set_ylabel(tech.format('Neuron'))


#Gap junctions
f = plt.figure()
ax = f.add_subplot(111)
ax.hist(g,color='k',histtype='stepfilled',alpha=0.8)
tech.adjust_spines(ax)
ax.set_xlabel(r'\Large $V_{gap}$')
ax.set_ylabel(tech.format(r'No. of neurons'))
f.tight_layout()
plt.show()
