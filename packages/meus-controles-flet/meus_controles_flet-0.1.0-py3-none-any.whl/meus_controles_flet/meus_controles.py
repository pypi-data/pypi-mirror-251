
from flet import*
from threading import Thread
from time import time, sleep

class Countdown(UserControl):
    def __init__(self, minutos, texto = ''):
        super().__init__()
        # self.page = Page
        self.minutos = minutos
        self.segundos = 60*minutos
        self.texto = texto
        self.pause = False

    def did_mount(self):
        self.running = True
        if self.minutos != '':            
            Thread(target=self.update_timer, daemon=True).start()

        else:
            self.countdown.value = self.texto
            self.update()

    def will_unmount(self):
        self.running = False

    def update_timer(self):
        while self.segundos and self.running:
            h, mins = divmod(self.segundos, 60*60)
            mins, secs = divmod(mins, 60)
            h, mins, secs = int(h), int(mins), int(secs)
            if self.texto != '':
                self.countdown.value = "{:s} {:02d}:{:02d}:{:02d}".format(self.texto,h, mins, secs)
            else:
                self.countdown.value = "{:02d}:{:02d}:{:02d}".format(h, mins, secs)

            self.update()
            sleep(1)
            self.segundos -= 1
            while self.pause:
                sleep(0.3)
          

    def build(self):
        self.countdown = Text()
        return self.countdown
'''
class Quadro(UserControl):
    def __init__(self, 
                content = None,
                #  page = Page,
                 width = None, 
                 height = None,
                 expand = 0,
                 bgcolor = None,
                 border_color = 'blue',
                 
                 ):
        super().__init__()
        # self.page = page
        self.content = content
        self.width = width
        self.height = height
        self.bgcolor = bgcolor
        self.border_color = border_color
        self.expand = expand
        self.bgcolor = bgcolor
    
    def build(self):
        return Container(
        content = self.content,
        border_radius=10,
        alignment=Alignment(0,0),
        border= border.all(0.2, color = self.border_color),
        width= self.width,
        height= self.height,
        expand = self.expand,
        bgcolor = self.bgcolor
        )
'''
class Contador(UserControl):
    def __init__(self, 
                 segundos = 10,
                 cor = 'green',
                 size = 20

    ):
        super().__init__()
        self.segundos = segundos
        self.cor = cor
        self.size = size
        self.saida = Row(visible=False)
        self.pause_contador = False
        self.parar_contador = False
    


    @property
    def Pause(self):
        return self.pause_contador
    
    @Pause.setter
    def Pause(self, valor: bool):
        self.pause_contador = valor
        self.update()

    @property
    def Parar(self):
        return self.parar_contador
    @Parar.setter
    def Parar(self, valor:bool):
        self.parar_contador = valor
        self.update()


    def did_mount(self):
        self.Cont()

    def build(self):
        return self.saida


    def Cont(self):
        self.saida.visible = True
        super().update()
        while self.segundos >= 0:
            horas2, minutos2, segundos2 = self.converter_segundos_para_horas_min_segundos(self.segundos)
            self.saida.controls = [Text(f"{horas2}:{minutos2}:{segundos2}", color  = self.cor, size = self.size)]
            super().update()
            self.segundos += -1
            sleep(1)
            while self.pause_contador:
                sleep(0.1)
            if self.parar_contador:
                self.saida.controls = [Text()]
                super().update()

                break
        # self.saida.controls = [Text()]
        self.saida.visible = False
        super().update()
        





    def converter_segundos_para_horas_min_segundos(self, segundos):
        def Algarismos(numero, qtd=2):
            numero = int(numero)
            return str(numero).zfill(qtd)
        horas = segundos // 3600  # 3600 segundos em uma hora
        horas = Algarismos(horas)
        segundos %= 3600
        minutos = segundos // 60  # 60 segundos em um minuto
        minutos = Algarismos(minutos)
        segundos %= 60
        segundos = Algarismos(segundos)

        return horas, minutos, segundos
 
class Quadro_assync(UserControl):
    def __init__(self, 
                content = None,
                 tipo = 'r', #ou 'c'
                #  page = Page,
                 width = None, 
                 height = None,
                 expand = 1,
                 bgcolor = None,
                 border_color = 'white',
                 
                 ):
        super().__init__()
        # self._page = page
        self.tipo = tipo
        self.content = content #Row(content) if self.tipo == 'r' else Column(content)
        self.width = width
        self.height = height
        self.bgcolor = bgcolor
        self.border_color = border_color
        self.expand = expand
        self.bgcolor = bgcolor
    
    def build(self):
        return Container(
        content = self.content,
        alignment=Alignment(0,0),
        border = border.all(1, color = self.border_color),
        width= self.width,
        height= self.height,
        expand = self.expand,
        bgcolor = self.bgcolor
        )

class Drop_new(UserControl):
    def __init__(self, 
        opitions = [], 
        value = None,
        width_person = None,
        on_change = None,
        data = None,

                
                ):
        super().__init__()
        self.opitions  = opitions
        self.value = value
        self.width = 30 if opitions == [] else 80
        self.on_change = on_change
        self.data = data

        if width_person != None:
            self._width = width_person         
 
        self._drop = Dropdown(        
                alignment= Alignment(0, 0),
                options=[dropdown.Option(i) for i in self.opitions],
                text_size = 15,
                border_width = 0,
                border=None,
                content_padding = 5,
                # border_color='white',
                expand=0,
                scale=1,
                autofocus = 0,
                value = self.value,
                width = self.width,
                # aspect_ratio = 1,
                height = 25,
                dense = True,
                text_style = TextStyle(weight = 'bold'),
                on_change=self.mudou,
                                                  
        ) 

    def build(self):  
        return self._drop
    
    def mudou(self, e):
        self.value = self._drop.value
        if self.on_change != None:
            self.enviar_change(e)
        self.update()

    def enviar_change(self,e):
        self.on_change(self, e)


    @property
    def getvalue(self):
        return self._drop.value
    @getvalue.setter
    def getvalue(self, valor):
        self._drop.options.append(dropdown.Option(valor))
        self._drop.value = valor
        super().update()

class New_task(UserControl):
    def __init__(self,
        task_delete,
        nome='',
        duracao=3,
        inicio=70,
        fim=170,
        passo = 1,
        ):
        super().__init__()
        self.task_delete = task_delete
        self.nome_tarefa = TextField(hint_text = 'nome da tarefa', width = 200, capitalization = TextCapitalization.CHARACTERS, value = nome, height=30, border_width = 0,dense=True)
        self.duracao_tarefa = Drop_new([0.1,0.3,0.5]+[i for i in range(1,31)], duracao, width_person = 70)
        self.inicio_tarefa = Drop_new([i for i in range(30,301)], inicio, width_person = 70)
        self.fim_tarefa = Drop_new([i for i in range(30,311)], fim, width_person = 70)
        self.passo_tarefa = Drop_new([0,0.1,0.3,0.5,0.7,0.9]+[i for i in range(1,20)], passo, width_person = 70)



    def build(self):
        remover_tarefa = IconButton(icon_color ='blue',icon=icons.DELETE, on_click = self.clicked, data ='del', icon_size = 18)
        self.play_parefa = IconButton(icon_color ='blue',icon=icons.PLAY_ARROW, on_click = self.clicked, data ='play tarefa', icon_size = 18)
        pause_parefa = IconButton(icon_color ='blue',icon=icons.PAUSE, on_click = self.clicked, data ='pause tarefa', icon_size = 18)

        linha_tarefa = [
            remover_tarefa,
            self.nome_tarefa,
            self.duracao_tarefa,
            self.inicio_tarefa,
            self.fim_tarefa,
            self.passo_tarefa,
            self.play_parefa,
            pause_parefa
        ]
        # linha_tarefa = Row([Container(i, height=40, border= border.all(0.1, color = 'blue')) for i in linha_tarefa], alignment='center', expand=1)
        linha_tarefa = Row([Container_new2(i, 10,30,1) for i in linha_tarefa], tight=True, spacing=0,alignment='center', expand=1)
        # linha_tarefa = Container(linha_tarefa, height = 50, border= border.all(0.3, color = 'blue'), border_radius=13)
        
        return Container_new2(linha_tarefa, 10)
        # return linha_tarefa
    
    def clicked(self, e):
        self.task_delete(self,e)

class Slider_new(UserControl):
    def __init__(self,
                texto = None,
                 min = None,
                 max = None,
                 divisions = None,
                 fator = 1, #valor a ser multiplicado por value
                 digitos = 1,
                 width = 200,
                 on_change = None,
                 data = None, 
                 value = False,
    ):



        super().__init__()
        self.texto = texto
        self.min = min
        self.max = max
        self.divisions = divisions
        self.fator = fator
        self.digitos = digitos
        self.width = width
        self.on_change = on_change
        self.data = data
        self.value = value

        self.passo_fim2 = Slider(active_color = '#004499',thumb_color = '#333333',min = self.min, 
                                 max = self.max, divisions=self.divisions,value = self.value, 
                                 width=self.width,on_change=self.mudou, data = self.data)
        valor = round(self.passo_fim2.value*self.fator,self.digitos)
        if self.digitos == 0:
            valor = int(valor)
        self.texto2 = Text(f'{self.texto} ({valor})')

    def mudou(self,e):
        valor = round(self.passo_fim2.value*self.fator,self.digitos)
        if self.digitos == 0:
            valor = int(valor)
        self.texto2.value = f'{self.texto} ({valor})'
        self.value = valor
        self.on_change(e, self)
        self.update()

    def build(self):
        return Row([self.texto2, self.passo_fim2],alignment='start', tight = True, spacing=0,run_spacing = 0, height=30 )

    @property
    def getvalue(self):
        return self.passo_fim2.value
    @getvalue.setter
    def setvalue(self, valor):
        self.passo_fim2.value = valor
        self.value = valor
        valor2 = round(self.passo_fim2.value*self.fator,self.digitos)
        if self.digitos == 0:
            valor2 = int(valor2)
        self.texto2.value = f'{self.texto} ({valor2})'
        self.update()

class Slider_new2(UserControl):
    def __init__(self,
                texto = None,
                 min = None,
                 max = None,
                 divisions = None,
                 fator = 1, #valor a ser multiplicado por value
                 digitos = 1,
                 width = None,
                 on_change = None,
                 data = None, 
                 value = False,
                 col1 = 4,
                
    ):



        super().__init__()
        self.texto = texto
        self.min = min
        self.max = max
        self.divisions = divisions
        self.fator = fator
        self.digitos = digitos
        self.width = width
        self.on_change = on_change
        self.data = data
        self.value = value
        self.col1 = col1
        # self.getvalue = None

        self.texto2 = Text(f'{self.texto}', no_wrap = True)
        self.passo_fim2 = Slider(min = self.min, active_color = '#004499',thumb_color = '#333333',
                                 max = self.max, value = self.value, 
                                on_change=self.mudou, data = self.data,  col = 12-self.col1)
        self.caixa = TextField(value = f'{self.passo_fim2.value:.0f}', border_width = 1, width=50,height=45, dense=True , content_padding = 5,
                               text_align = "center", on_change = self.mudou2,)
        


    def mudou(self,e):
        # self.texto2.value = f'{self.texto} ({self.passo_fim2.value:.0f})'
        if self.digitos == 0:
            self.passo_fim2.value = int(self.passo_fim2.value)
        else:
            self.passo_fim2.value = round(float(self.passo_fim2.value), self.digitos)

        self.caixa.value = f'{self.passo_fim2.value}'
        if self.on_change != None:
            self.on_change(e, self)
        self.value = self.passo_fim2.value
        self.update()
    def mudou2(self,e):
        # self.texto2.value = f'{self.texto} ({self.passo_fim2.value:.0f})'
        self.passo_fim2.value = self.caixa.value 
        self.value = self.passo_fim2.value
        if self.on_change != None:
            self.on_change(e, self)
        self.update()       

    def build(self):
        return ResponsiveRow([Row([self.texto2, self.caixa], col = self.col1),self.passo_fim2, ],expand = 0,alignment='start', spacing=0,run_spacing = 0, height=30,)#,alignment='start', tight = True, spacing=0,run_spacing = 0, height=30 

    @property
    def getvalue(self):
        return self.passo_fim2.value
    @getvalue.setter
    def getvalue(self, valor):
        self.passo_fim2.value = valor
        self.value = valor
        valor2 = round(self.passo_fim2.value,self.digitos)
        if self.digitos == 0:
            valor2 = int(valor2)
        self.caixa.value = f'{valor}'
        # self.texto2.value = f'{self.texto} ({valor2})'
        self.update()

class Saidas(UserControl):
    def __init__(self,
        texto1 = '',
        texto2 = '',
        texto3 = '',
        texto4 = '',
        texto5 = '',
        texto6 = '',  
        cor = 'white',
        size = 20,                              
                  ):
        super().__init__()
        # self.t1 = texto1
        # self.t2 = texto2
        # self.t3 = texto3
        # self.t4 = texto4
        # self.t5 = texto5
        # self.t6 = texto6
        self._texto1a = Text(texto1, color = cor, size = size, visible=False)
        self._texto2a = Text(texto2, color = cor, size = size, visible=False)
        self._texto3a = Text(texto3, color = cor, size = size, visible=False)
        self._texto4a = Text(texto4, color = cor, size = size, visible=False)
        self._texto5a = Text(texto5, color = cor, size = size, visible=False)
        self._texto6a = Text(texto6, color = cor, size = size, visible=False)
        self.Visibles(                
                 texto1,
                 texto2,
                 texto3,
                 texto4,
                 texto5,
                 texto6
                 )
      
    def build(self):
        self.saida = Row(
            alignment= MainAxisAlignment.START,
            vertical_alignment = 'center',
            
            # height=300,
            tight = True,
            wrap = True,
            expand=1,
            run_spacing = 2,
            # runs_count=1,
            # max_extent=300,
            # child_aspect_ratio=8,
            # spacing=1,
            # run_spacing=10,
            # padding = 0, 
            controls=[
                        self._texto1a, self._texto2a, self._texto3a,self._texto4a,self._texto5a,self._texto6a
                    #   Column([self._texto1a, self._texto2a, self._texto3a],alignment = MainAxisAlignment.START),
                    #   Column([self._texto4a,self._texto5a,self._texto6a],alignment = MainAxisAlignment.START),
                    #   Row([],alignment = MainAxisAlignment.SPACE_AROUND),  
                                     
                      ],                                            
        )
        # self.saida = Container(self.saida, margin=margin.all(6))
        
        return self.saida
    
    def Visibles(self,                 
                 texto1,
                 texto2,
                 texto3,
                 texto4,
                 texto5,
                 texto6
                 ):
        if texto1 != '':
            self._texto1a.visible = True
        if texto2 != '':
            self._texto2a.visible = True
        if texto3 != '':
            self._texto3a.visible = True
        if texto4 != '':
            self._texto4a.visible = True
        if texto5 != '':
            self._texto5a.visible = True
        if texto6 != '':
            self._texto6a.visible = True 
    
      
    @property
    def texto1(self):       
        return self._texto1a.value
    
    @texto1.setter
    def texto1(self, texto):
        self._texto1a.value = texto 
        self._texto1a.size = 20
        self._texto1a.visible = True 
        self._texto1a.no_wrap = True
  
    @texto1.setter
    def texto1_color(self, color):
        self._texto1a.color = color
    @texto1.setter
    def texto1_size(self, size):
        self._texto1a.size = size 
    
    @property
    def texto2(self):       
        return self._texto2a.value
    
    @texto2.setter
    def texto2(self, texto):
        self._texto2a.value = texto 
        self._texto2a.size = 20
        self._texto2a.visible = True 
        self._texto2a.no_wrap = True
  
    @texto2.setter
    def texto2_color(self, color):
        self._texto2a.color = color
    @texto2.setter
    def texto2_size(self, size):
        self._texto2a.size = size 
    
    @property
    def texto3(self):       
        return self._texto3a.value
    
    @texto3.setter
    def texto3(self, texto):
        self._texto3a.value = texto 
        self._texto3a.size = 20
        self._texto3a.visible = True 
        self._texto3a.no_wrap = True
  
    @texto3.setter
    def texto3_color(self, color):
        self._texto3a.color = color
    @texto3.setter
    def texto3_size(self, size):
        self._texto3a.size = size 
    
    @property
    def texto4(self):       
        return self._texto4a.value
    
    @texto4.setter
    def texto4(self, texto):
        self._texto4a.value = texto 
        self._texto4a.size = 20
        self._texto4a.visible = True 
        self._texto4a.no_wrap = True
  
    @texto4.setter
    def texto4_color(self, color):
        self._texto4a.color = color
    @texto4.setter
    def texto4_size(self, size):
        self._texto4a.size = size 
    
    @property
    def texto5(self):       
        return self._texto5a.value
    
    @texto5.setter
    def texto5(self, texto):
        self._texto5a.value = texto 
        self._texto5a.size = 20
        self._texto5a.visible = True 
        self._texto5a.no_wrap = True
  
    @texto5.setter
    def texto5_color(self, color):
        self._texto5a.color = color
    @texto5.setter
    def texto5_size(self, size):
        self._texto5a.size = size 
    
    @property
    def texto6(self):       
        return self._texto6a.value
    
    @texto6.setter
    def texto6(self, texto):
        self._texto6a.value = texto 
        self._texto6a.size = 20
        self._texto6a.visible = True 
        self._texto6a.no_wrap = True
  
    @texto6.setter
    def texto6_color(self, color):
        self._texto6a.color = color
    @texto6.setter
    def texto6_size(self, size):
        self._texto6a.size = size 

class Saidas2(UserControl):
    def __init__(self, 
                 texto1 = '',
                 texto2 = '',
                 texto3 = '',
                 texto4 = '',
                 texto5 = '',
                 texto6 = ''
                 ):
        super().__init__()

        self.texto1 = Text(texto1, size = 20, visible=False)
        self.texto2 = Text(texto1, size = 20, visible=False)
        self.texto3 = Text(texto1, size = 20, visible=False)
        self.texto4 = Text(texto1, size = 20, visible=False)
        self.texto5 = Text(texto1, size = 20, visible=False)
        self.texto6 = Text(texto1, size = 20, visible=False)
        self.Visibles(                
                 texto1,
                 texto2,
                 texto3,
                 texto4,
                 texto5,
                 texto6
                 )
    def build(self):
        self.saida = Row(
            alignment= MainAxisAlignment.START,
            vertical_alignment = 'center',
            
            # height=300,
            tight = True,
            wrap = True,
            expand=1,
            run_spacing = 2,
            # runs_count=1,
            # max_extent=300,
            # child_aspect_ratio=8,
            # spacing=1,
            # run_spacing=10,
            # padding = 0, 
            controls=[
                      self.texto1,self.texto2,self.texto6o3,
                      self.texto4,self.texto5,self.texto6
                    #   Row([],alignment = MainAxisAlignment.SPACE_AROUND),  
                                     
                      ],                                            
        )
        # self.saida = Container(self.saida, margin=margin.all(6))
        
        return self.saida

    def Visibles(self,                 
                 texto1 ,
                 texto2,
                 texto6o3,
                 texto6o4,
                 texto6o5,
                 texto6
                 ):
        if texto1 != '':
            self.texto1.visible = True
        if texto2 != '':
            self.texto2.visible = True
        if texto6o3 != '':
            self.texto3.visible = True
        if texto6o4 != '':
            self.texto4.visible = True
        if texto6o5 != '':
            self.exto5.visible = True
        if texto6 != '':
            self.texto6.visible = True                                                            



    '''
class Pomodoro(UserControl):
    def __init__(self):
        super().__init__()
        self.pomodoro_control_thread = True
        self.tempo_pomodoro_set = 0.1
        self.Metro_normal = Metronomo()
        self.Metro_normal.pause = False
        self.parar = False
        self.tempo_descanso_value = 6
        self.quado_saida = Row()
        self.saida_respiro = Column(visible=False)



    def did_mount(self):
        self.Pomodoro()

    def build(self):
        return  Row([self.quado_saida, self.saida_respiro])  
    def Pomodoro(self):
        texto = 'Pomodoro inciado...'
        self.quado_saida.visible = True        
        self.quado_saida.controls = [Text(texto)]
        super().update()

        while self.pomodoro_control_thread:
            self.quado_saida.visible = True
            
            segundos = self.tempo_pomodoro_set*60
            while segundos >= 0:
                h, mins = divmod(segundos, 60*60)
                mins, secs = divmod(mins, 60)
                h, mins, secs = int(h), int(mins), int(secs)
                if texto != '':
                    contador = "{:s} {:02d}:{:02d}:{:02d}".format(texto,h, mins, secs)
                else:
                    contador = "{:02d}:{:02d}:{:02d}".format(h, mins, secs)

                self.quado_saida.controls = [Text(contador)]
                sleep(1)
                super().update()
                segundos -= 1
                while self.Metro_normal.pause:
                    sleep(0.3)
                if self.parar or not self.pomodoro_control_thread:
                    break

            if self.parar or not self.pomodoro_control_thread:
                self.quado_saida.visible = False
                self.quado_saida.controls = None
                break

            MessageBeep(MB_ICONHAND)

            self.Respiro()
            
            if not self.pomodoro_control_thread:
                break
            MessageBeep(MB_ICONHAND)

            if not self.pomodoro_control_thread:
                break
            texto = 'Volte a treinor por '

        self.quado_saida.controls =  None

    def Respiro(self):
        # self.Metro_normal.pause = True
        # estado_saida_treinamento = self.saida_treinamento.visible
        # estado_saida_quado = self.quado_saida.visible
        # self.saida_treinamento.visible = False
        self.quado_saida.visible = False
        self.saida_respiro.visible = True
        descan = int(self.tempo_descanso_value*60/19.4)
        # print(descan)
        # self.Metro_normal.pause = False
        self.parar = False
        width_max = 740
        respiro = Container(content=Text(),bgcolor= colors.YELLOW,width = 0, border_radius=40)
        def Inspire(d):
            # self.quado_saida.content = Text(f'INSPIRE ({d})')
            s = Saidas(f'INSPIRE ({d})', cor = colors.YELLOW, size = 50)
            # s.saida_tempo_de_treino.visible = True
            # self.saida.texto1_size = 50
            # self.saida.texto1_color= colors.YELLOW
            self.saida_respiro.controls = [Column([s, respiro])]
            # self.quado_saida.content.alignment= MainAxisAlignment.CENTER

        def Expire(d):
            s = Saidas(f'EXPIRE  ({d})', cor = colors.GREEN, size = 50)

            # s.saida_tempo_de_treino.visible = True
            # self.saida.texto1_size = 50
            # self.saida.texto1_color= colors.GREEN
            self.saida_respiro.controls = [Column([s, respiro])]
            # self.quado_saida.content.alignment= MainAxisAlignment.CENTER


        for d in range(descan,0,-1):
            a = time()
            Inspire(d)
            super().update()
            for i in range(0,width_max,6*2):
                respiro.width = i
                sleep(0.001)
                if self.parar:
                    break
                super().update()
            respiro.bgcolor = colors.GREEN
            Expire(d)
            super().update()
            if self.parar:
                break             
            for i in range(width_max,0,-1*2):
                respiro.width = i
                if self.parar:
                    break                    
                sleep(0.01567)
                super().update()
            respiro.bgcolor = colors.YELLOW
            b = time()-a
            print(b)

        # self.saida_treinamento.visible = estado_saida_treinamento
        # self.quado_saida.visible = estado_saida_quado
        # self.saida_respiro.controls = None
        self.saida_respiro.visible = False
        self.quado_saida.visible = True
        self.Metro_normal.pause = False
        respiro.width = 0
        super().update()
    '''

class SaveSelectFile(UserControl):
    def __init__(self, tipo = 'txt'):
        super().__init__()
        self.tipo = tipo
        self.pick_files_dialog = FilePicker(on_result=self.pick_files_result)
        self.nome_arquivo = None
        self.func = None

    def pick_files_result(self, e: FilePickerResultEvent):
        if self.func == 'select':
            self.nome_arquivo = f'{e.files[0].path}'
        else:
            self.nome_arquivo = f'{e.path}.{self.tipo}'
        super().update()

        
    # @property
    def Save(self):
        self.func = 'save'
        self.pick_files_dialog.save_file(file_type = FilePickerFileType.CUSTOM, allowed_extensions = [self.tipo])
        while not self.nome_arquivo:
            sleep(0.3)
        self.update()
        return self.nome_arquivo
    
    def Select(self):
        self.func = 'select'
        self.pick_files_dialog.pick_files(file_type = FilePickerFileType.CUSTOM, allowed_extensions = [self.tipo])
        while not self.nome_arquivo:
            sleep(0.3)
        self.update()
        return self.nome_arquivo    
    
    def build(self):
        return self.pick_files_dialog    

class Container_new3(UserControl):
    def __init__(self,
                 content = None, 
                 gradiente = ('black', 'white'),
                 height = None,
                 scale = 1,
                 border_radius = None,
                 rotação = 0.3,
                 ShadowColor = 'blue,0.6',
                 page = None,
                
        ):
        super().__init__()
        self.page = page
        self.content = content
        self.gradiente = gradiente
        self.height = height
        self.scale = scale
        self.border_radius = border_radius
        self.rot = rotação
        self.ShadowColor = ShadowColor

        self.horizontal = BorderSide(3, colors.with_opacity(0.4,'blue'))
        self.vertical = BorderSide(3, colors.with_opacity(0.9,'gray'))
        
        self.bor = Border(left=self.horizontal, top=self.horizontal, right=self.vertical, bottom=self.vertical)
        self.bor = border.all(5, colors.with_opacity(0.3,'red'))
    
        self.sombra =  BoxShadow(
            spread_radius=0,
            blur_radius=15,
            color=self.ShadowColor,
            offset=Offset(3, 3),
            blur_style=ShadowBlurStyle.NORMAL)  


        self.gradient =  gradient=LinearGradient(
            begin=Alignment(0, 1),
            end=Alignment(0, -1),
            
            colors=[
                self.gradiente[0],
                self.gradiente[0],
                self.gradiente[0],
                self.gradiente[0],
                self.gradiente[0],
                self.gradiente[1],
                        ],
            tile_mode=GradientTileMode.MIRROR,
            rotation=self.rot*3.14/180,
        )
        self.saida = Container(content=self.content,   
                         border=self.bor, 
                         shadow = self.sombra, 
                         scale = self.scale, 
                         height = self.height,
                         border_radius = self.border_radius,
                         gradient=self.gradient, 
                         padding = 0
                         )
    def build(self):
        return self.saida




def Container_new2(i, border_radius =20, height = None, scale = None, gradiente = ("black", "#777777")):
    horizontal = BorderSide(3, colors.with_opacity(0.4,'blue'))
    vertical = BorderSide(3, colors.with_opacity(0.9,'gray'))
    
    bor = Border(left=horizontal, top=horizontal, right=vertical, bottom=vertical)
    bor = border.all(5, colors.with_opacity(0.3,'red'))
    
    sombra =  BoxShadow(
        spread_radius=0,
        blur_radius=15,
        color=colors.with_opacity(0.6,'blue'),
        offset=Offset(3, 3),
        blur_style=ShadowBlurStyle.NORMAL)        
    gradiente =  gradient=LinearGradient(
        begin=Alignment(0, 1),
        end=Alignment(0, -1),
        
        colors=[
            gradiente[0],
            gradiente[0],
            gradiente[0],
            gradiente[0],
            gradiente[0],
            gradiente[1],
                    ],
        tile_mode=GradientTileMode.MIRROR,
        rotation=0*3.14/180,
    )
    return Container(content=i,   border=bor, shadow = sombra, scale = scale, height = height,border_radius = border_radius,gradient=gradiente, padding = 0)

def Botao( texto = None,  icon = None,size = 30,width = 80, height = 30,on_click = None, data = None, color  = 'blue', rot = 30, gradiente = ("black", "#777777")):   
    return Container_new2(TextButton(content = Text(texto, size=20, weight='bold', no_wrap=True, color=color), data = data,on_click=on_click, 
                                     width = width,height = height), gradiente = gradiente   )
def Botao2( texto = None,  icon = None,size = 30,width = 80, height = 50,on_click = None, data = None, color  = 'blue', rot = 30):
    bor2 = border.BorderSide(20, colors.with_opacity(1,color))
    bor = border.all(0, colors.with_opacity(0.3,'#995555')) 
    sombra =  BoxShadow(
        spread_radius=0,
        blur_radius=30,
        color=colors.with_opacity(0.6,color),
        offset=Offset(3, 3),
        blur_style=ShadowBlurStyle.NORMAL)
    gradiente =  gradient=LinearGradient(
        begin=Alignment(-1, -1),
        end=Alignment(-0.1, -0.1),
        
        colors=[
            "#777777",
            "#000000",
            "#000000",
                    ],
        tile_mode=GradientTileMode.MIRROR,
        rotation=rot*3.14/180,
    )


    if icon == None:
        conteudo = ElevatedButton(content = Text(texto, size=25, weight='bold', no_wrap=True, color=color),bgcolor = colors.with_opacity(0,'black'))
    else:
        conteudo = Icon(icon, color=color)
    return Container( 
        content= conteudo,
            # [
                # Text("1", color=colors.WHITE),
                # Text("2", color=colors.WHITE, right=0),
                # Text("3", color=colors.WHITE, right=0, bottom=0),
                # Text("4", color=colors.WHITE, left=0, bottom=0),
            # ]
        # ),
        # top = 5,
        alignment=Alignment(0, 0),
        bgcolor='green',
        width=width,
        height=height,
        # height=220,
        border_radius=15,
        on_click = on_click,
        shadow=sombra,
        gradient=gradiente,
        border= bor, 
        data = data,    
            

        )


def Slider_new3(texto,min = 10, max = 240, width=150 ):
    return Row([Row([Text(texto),Slider(min = min, max = max, width=width,active_color = '#004499',thumb_color = '#333333',)])],alignment='start', tight = True, spacing=0,run_spacing = 0, height=30 )

def main_test(page: Page):
    page.window_width = 1500
    page.window_height = 750


    t = Contador(3600, cor= 'blue', size = 15)
    # t.continuar_treinando = True
    def Parar(e):
        t.segundos = int(b.value)
    b = TextField( on_submit=Parar)

    def atualizar(e,slider):
        # Tempo_de_estudo = Slider_new2('Tempo de estudo', 10, 240,data = 'Tempo_de_estudo', width=200, value = 10, on_change = atualizar).bunda()
        print(slider)
        page.update()
   
    Tempo_de_estudo = Slider_new2('Tempo de estudo', 0, 5.0,data = 'Tempo_de_estudo', value = 4.3, on_change = atualizar, col1=2)
    # Tempo_de_estudo = Row([Text('asldjfshldkajl'),Slider(min = 10, max = 240, width=350)])
    # Tempo_de_estudo = Slider_new3('casa', 10,250,130)
    # Tempo_de_estudo = ResponsiveRow([
    # Column(col=6, controls=[Text("Column 1")]),
    # Column(col=6, controls=[Text("Column 2")])
    # ])
    largura  = Text()
    def page_resize(e):
        print("New page size:", page.window_width, page.window_height)
        print("New page size:", page.window_width, page.window_height)
        print("New page size:", page.window_width, page.window_height)
        largura.value = page.window_width
        sleep(5)
        page.update()


    page.on_resize = page_resize
    page.on_close = page_resize


            
    conta = Container_new3(content = Text('casadas'), border_radius = 15, rotação=50, ShadowColor='blue,0.2')

    conta = Slider_new2

    page.add(conta)
    page.update()



if __name__ == '__main__':
    app(target=main_test)            
