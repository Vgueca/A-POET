from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import numpy as np

class Model:
    def __init__(self, state_size, action_size, learning_rate=0.001, discount_factor=0.95):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.model = self.build_model()

    def build_model(self):
        model = Sequential()
        model.add(Dense(64, input_dim=self.state_size, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))  # Usamos activación lineal para los Q-values
        model.compile(optimizer=Adam(lr=self.learning_rate), loss=self.custom_loss)
        return model

    def custom_loss(self, y_true, y_pred):
        # Calculamos la loss como el error cuadrático medio ponderado por el reward
        reward = y_true[:, 0]  # El reward está en la primera columna de y_true
        Q_value = y_pred  # El valor Q predicho por la red neuronal
        return np.mean(np.square(reward - Q_value))

    def get_action(self, state):
        # Supongamos que state contiene todos los parámetros del agente
        return np.argmax(self.model.predict(state))

    def train(self, X, y):
        # Entrenamos el modelo con los datos de entrada y los targets (rewards)
        self.model.fit(X, y, epochs=1, verbose=0)


