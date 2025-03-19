# sEMG
sEMG Data Procession

## How to sync with motion capture system

🔗：[delsys-vicon-nexus.pdf](https://delsyseurope.com/downloads/TUTORIAL/delsys-vicon-nexus.pdf)

🔗：[Trigno Wireless Biofeedback System User's Guide](https://delsys.com/downloads/USERSGUIDE/trigno/wireless-biofeedback-system.pdf)

1. Connect the `Delsys base` to the `NI USB 6218` with DC-A22
2. Connect the `USB` of the  `Delsys base` to computer
3. Open the `Delsys Control Utility` software and click `Start Analog Output`
4. Open `Cortex` and connect to device

 :warning:ATTENTION:

* Analog output of Delsys only have original EMG data, do not have acceleration or gyro data
* About the wire connection:

| COM  | Channel | EMG NO | COM  | Channel | EMG NO |
| ---- | ------- | ------ | ---- | ------- | ------ |
| 47   | CH17    | 1      | 53   | CH20    | 7      |
| 48   | CH25    | 2      | 54   | CH28    | 8      |
| 49   | CH18    | 3      | 56   | CH21    | 9      |
| 50   | CH26    | 4      | 57   | CH29    | 9      |
| 51   | CH19    | 5      | 58   | CH22    | 10     |
| 52   | CH27    | 6      | 59   | CH30    | 11     |



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

## Author

* Haolan Xian
