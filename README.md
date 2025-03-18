# sEMG
sEMG Data Procession

## How to sync with motion capture system

🔗：[delsys-vicon-nexus.pdf](https://delsyseurope.com/downloads/TUTORIAL/delsys-vicon-nexus.pdf)

🔗：[Trigno Wireless Biofeedback System User's Guide](https://delsys.com/downloads/USERSGUIDE/trigno/wireless-biofeedback-system.pdf)

## EMG Analysis

How to analysis EMG data with EMGworks?

🔗：[EMGworks Analysis: Getting Started](https://www.youtube.com/watch?v=qgowNLHLN0U)

### Timing Analysis

🔗：[Electromyography (EMG) Analysis: Timing Analysis](https://www.youtube.com/watch?v=QAqmVzTOCG0)

Activation timing analysis is helpful to analysis of **co-odination** patterns of the muscle.

How to conduct activation timing analysis with Delsys EMGworks Analysis?

`EMG Threshold`

### Amplitude Analysis

🔗：[Electromyography (EMG) Analysis: Amplitude Analysis](https://www.youtube.com/watch?v=4j_U7vPP2as)

## Experiment Protocol

* Speeds (m/s): 0.8 / 1.0 / 1.2 / 1.4 / 1.6
* Weight (%Body Weight): 0 / 10 / 20 / 30
* Slope (degree): 0 / 5 / 10 / 15
* Muscles: Rectus Femoris (RF), Vastus Lateralis (VASL), Vastus Medialis (VASM), Biceps Femoris short head (BFsh), Biceps Femoris long head (BFlh), Gastrocnemius Lateral head (GASL),  Gastrocnemius Medial head (GASM), Soleus (SOL), Tibialis Anterior (TA)

## scripts

* `originalDataProcession`：处理由Delsys Analysis导出的一个步态周期内肌电均值数据的脚本；

* `plotEMG`：绘制肌电以及误差带图；
