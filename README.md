# xpilot-agents
Final Project for class COM 407 Computational Intelligence (Prof. Gary Parker) built by Bill Tran, William Mears, and Tyler Maguire. 

## Abstract
Compare the performance of X-Pilot controllers trained with Artificial Neural Network and with Fuzzy Logic when both use Genetic Algorithm to learn their associated parameters.

## Methods
In this project, we evolved two controllers in X-Pilot, one with Neural Network and the other with Fuzzy Logic. For both approaches, we used Genetic Algorithm in the learning process. For the controller with the Neural Network, we used Genetic Algorithm to learn the weights associated with the network. On the other hand, for the Fuzzy controller, Genetic Algorithm helped us learn the thresholds for the Fuzzy sets.

We had the two controllers compete individually against a well-trained aggressive bot made by Cam and Nikesh to evaluate the performance. In addition, we also had a competition between the neural network and the fuzzy controllers for head-to-head results.

## User Manual
### Install X-Pilot AI
Follow the instructions [here](https://oak.conncoll.edu/parker/com407/Xpilot-AI_setup.txt) and start a map.
### Training
0. Start an opponent
Start an opponent of yours before starting the training agent. Example:
```python
> python3 Dumbo.py
```
1. Neural Network + Genetic Algorithm
```python
> python3 training/neural_network/nn_training.py
```
2. Fuzzy + Genetic Algorithm
```python
> python3 training/fuzzy/fuzzy_training.py
```
### Testing
The chosen chromosomes (aka best trained agents) are in the `testing` folder. To play them against each other, run
```python
> python3 testing/nn_chosen.py & python3 testing/fuzzy_chosen.py
```
## More details
For more details on our methodology and technicality, please visit [our website](https://billtrn.com/com407/).
