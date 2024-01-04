import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, Slider, CheckButtons
from scipy.signal import butter, filtfilt

'''TASK1 - HARMONIC FUNCTION + NOISE'''
def harmonic_with_noise(t, amplitude, frequency, phase, noise_mean, noise_covariance, show_noise):
    signal = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    noise = np.random.normal(noise_mean, np.sqrt(noise_covariance), len(t))
    signal_with_noise = signal + noise if show_noise else signal
    return signal_with_noise

def f(t, amplitude, frequency, phase, noise_mean, noise_covariance, show_noise):
    return harmonic_with_noise(t, amplitude, frequency, phase, noise_mean, noise_covariance, show_noise)

t = np.linspace(0, 1, 1000)

# Initial parameters
init_amplitude = 5
init_frequency = 3
init_phase = 0
init_noise_mean = 0
init_noise_covariance = 0
init_show_noise = False

# Create the figure and the line that we will manipulate
fig, ax = plt.subplots()
line, = ax.plot(t, f(t, init_amplitude, init_frequency, init_phase, init_noise_mean, init_noise_covariance, init_show_noise), lw=2)
ax.set_xlabel('Time [s]')

fig.subplots_adjust(left=0.25, bottom=0.45)

# Sliders for function parameters
axamp = fig.add_axes([0.25, 0.1, 0.65, 0.03])
amp_slider = Slider(
    ax=axamp,
    label='Amplitude',
    valmin=0,
    valmax=10,
    valinit=init_amplitude,
)

axfreq = fig.add_axes([0.25, 0.15, 0.65, 0.03])
freq_slider = Slider(
    ax=axfreq,
    label='Frequency [Hz]',
    valmin=0.1,
    valmax=30,
    valinit=init_frequency,
)

axphase = fig.add_axes([0.25, 0.20, 0.65, 0.03])
phase_slider = Slider(
    ax=axphase,
    label='Phase',
    valmin=0,
    valmax=2 * np.pi,
    valinit=init_phase,
)

# Sliders for noise parameters
axnoisemean = fig.add_axes([0.25, 0.25, 0.65, 0.03])
noisemean_slider = Slider(
    ax=axnoisemean,
    label='Noise Mean',
    valmin=-5,
    valmax=5,
    valinit=init_noise_mean,
)

axnoisecov = fig.add_axes([0.25, 0.30, 0.65, 0.03])
noisecov_slider = Slider(
    ax=axnoisecov,
    label='Noise Covariance',
    valmin=0,
    valmax=10,
    valinit=init_noise_covariance,
)

# Checkbox for show/hide noise
axcheck = fig.add_axes([0.025, 0.5, 0.15, 0.1])
check_button = CheckButtons(axcheck, labels=['Show Noise'], actives=[init_show_noise])

def update(val):
    line.set_ydata(f(t, amp_slider.val, freq_slider.val, phase_slider.val, noisemean_slider.val, noisecov_slider.val, check_button.get_status()[0]))
    fig.canvas.draw_idle()

def update_check(label):
    line.set_ydata(f(t, amp_slider.val, freq_slider.val, phase_slider.val, noisemean_slider.val, noisecov_slider.val, check_button.get_status()[0]))
    fig.canvas.draw_idle()

# register the update function with each slider
amp_slider.on_changed(update)
freq_slider.on_changed(update)
phase_slider.on_changed(update)
noisemean_slider.on_changed(update)
noisecov_slider.on_changed(update)

# register the update function with the checkbox
check_button.on_clicked(update_check)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
resetax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')

def reset(event):
    amp_slider.reset()
    freq_slider.reset()
    phase_slider.reset()
    noisemean_slider.reset()
    noisecov_slider.reset()
    check_button.set_active(init_show_noise)

button.on_clicked(reset)

plt.show()

'''TASK2 - '''


