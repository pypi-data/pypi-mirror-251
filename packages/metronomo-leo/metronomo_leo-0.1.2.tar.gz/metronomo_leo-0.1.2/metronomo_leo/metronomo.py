
from time import sleep, time


# from googlesheets import AtualizarCelulas, LerCelulas
from threading import Lock

import pygame as pg
from os import environ, path, makedirs, getcwd
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

pg.mixer.init()


def gen_pygame_sound(sound_name, volume):
    try:
        sound = pg.mixer.Sound(sound_name)
        sound.set_volume(volume)
        return sound
    except FileNotFoundError as f:
        # print(f)
        print("o arquivo '*.wav' não foi encontrado")



class Metronomo:
        #para bloquear a criação e mais de uma intãncia da classe Metronomo
    _instancia = None
    _lock = Lock()
    def __new__(cls,window = None):
        with cls._lock:
            if cls._instancia is None:
                cls._instancia = super(Metronomo, cls).__new__(cls)
                # Inicialize os atributos da instância aqui
        return cls._instancia 
    


    temp = 2
    def __init__(self, pasta):

        self.pasta = pasta
        # parâmetros do metrônomo
        self.__bpm = 120
        self.__volume = 1
        self.__on = False
        self.__att = False
        self.tipo_compasso = 4
        self.qtd_compassos = 1
        self.cont_tempos = 0
        self.cont_compassos = 0
        self.pause = False

       
    @classmethod       
    def Juntar(self, a, b):
        return path.join(a, b)
    # @classmethod
    # @property
    # def Pasta(self):
    #     try:
    #         return path.join(getcwd(), "sound_files")
    #     # pasta = r'C:\Users\leani\metronomo\Metronomo-main\Metronomo-main\sound_files'
    #     except:
    #         makedirs(path.join(getcwd(), "sound_files"))
    #         return path.join(getcwd(), "sound_files")

    @property
    def __sound_data(self):
        self.__sound_name = path.join(self.pasta, "1.wav")
        # self.__sound_name = r'C:\Users\leani\flet\metronomoflet\metronomoleo\assets\sound_files\1.wav'
        som = gen_pygame_sound(self.__sound_name, self.__volume)
        return som    
    @__sound_data.setter
    def __sound_data(self, volume):
        self.__sound_name = path.join(self.pasta, "1.wav")
        # self.__sound_name = r'C:\Users\leani\flet\metronomoflet\metronomoleo\assets\sound_files\1.wav'

        som = gen_pygame_sound(self.__sound_name, volume)
            


    @property
    def __sound_data2(self):
        self.__sound_name2 = path.join(self.pasta, "2.wav")
        # self.__sound_name2 = r'C:\Users\leani\flet\metronomoflet\metronomoleo\assets\sound_files\2.wav'
        som =  gen_pygame_sound(self.__sound_name2, self.__volume) 
        return som    
    @__sound_data2.setter
    def __sound_data2(self, volume):
        self.__sound_name2 = path.join(self.pasta, "2.wav")
        # self.__sound_name2 = r'C:\Users\leani\flet\metronomoflet\metronomoleo\assets\sound_files\2.wav'

        som =  gen_pygame_sound(self.__sound_name2, volume)    
           
    # Getters & Setters
    @classmethod    
    @property
    def nometarefastxt(self):
        return self.Juntar(getcwd(), 'tarefas.txt')
    # @classmethod    
    @property
    def getBpm(self):
        return self.__bpm
    # @classmethod
    def setBpm(self, bpm):
        self.__bpm = bpm
        self.__att = True
        # print(f'setou - {bpm}')
    @property
    def getVolume(self):
        return self.__volume
    # @classmethod
    def setVolume(self, volume):
        self.__volume = volume
        self.reload
    # @classmethod
    def getOn(self):
        return self.__on
    @property
    def setOn(self, on):
        return self.__on
      
    @setOn.setter
    def setOn(self, on):
        self.__on = on

    # Methods
    # @classmethod
    @property
    def reload(self):
        self.__sound_data = self.__volume
        self.__sound_data2 = self.__volume
        # print(self.__sound_data)
    # @classmethod
    def Atualizar(self, valor=True):
        self.__att = valor
    # @classmethod
    def beep(self):
        t = 60/self.__bpm
        self.cont_tempos = 0
        self.cont_compassos = 0
        while self.__on:
            # a = time()
            while self.pause:
                # print(f'pause = True')
                sleep(0.1)

            if self.__att:
                t = 60/self.__bpm
            self.__att = False
# 
            # self.__sound_data2.play()
            if self.cont_tempos in [0, 4, 8, 12, 16, 20, 24, 28, 32,36,40,44,48,52,56,60]:
                self.__sound_data2.play()
                # print('aqui')
            else:
                self.__sound_data.play()

            # sleep(t)

            if self.cont_tempos == self.tipo_compasso*self.qtd_compassos:
                sleep(t)
                self.cont_tempos = 0
            else:
                sleep(t)
            self.cont_tempos += 1
            # print(f'{time()-a}')
        # if not self.__on:
        #     print('self.__on = False')

if __name__ == '__main__':
    m = Metronomo()
    m.setBpm(60)
    m.setOn = True
    m.beep()

