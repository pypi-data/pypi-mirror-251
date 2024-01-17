"""
  Documentacion de este player
"""


class Player:
    """
    Esta clase crea un reproductor de musica
    """

    def play(self, song):
        """Reproduce la cancion que recibio en el constructor

        Args:
            song (str): este es un string con el path de la cancion
        Returns:
            Devuelve 1 se reproduce con exito, devuelve 0 se ocurrio un error
        """
        print("Reproduciendo la Cancion")

    def stop(self):
        print("stopping")
