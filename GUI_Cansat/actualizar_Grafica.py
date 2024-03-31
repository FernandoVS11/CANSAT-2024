from abc import ABC, abstractclassmethod


class ActualizarGrafica(ABC):
    @abstractclassmethod
    def actualizar(self):
        pass