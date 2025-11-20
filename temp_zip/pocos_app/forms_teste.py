from django import forms
from datetime import datetime, timedelta

class TesteBombeamentoForm(forms.Form):
    # Parâmetros do Teste de Bombeamento
    data_inicio = forms.DateField(
        label='Data de Início do Teste',
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=datetime.now().date()
    )
    hora_inicial = forms.TimeField(
        label='Hora de Início do Teste',
        widget=forms.TimeInput(attrs={'type': 'time'}),
        initial=datetime.now().time()
    )
    nivel_inicial = forms.FloatField(label='Nível Inicial (m)', min_value=0)
    nivel_final = forms.FloatField(label='Nível Final (m)', min_value=0)
    vazao_inicial = forms.FloatField(label='Vazão Inicial (m³/h)', min_value=0)
    vazao_final = forms.FloatField(label='Vazão Final (m³/h)', min_value=0)
    
    # Tempo de estabilização (em minutos)
    tempo_estabilizacao_min = forms.IntegerField(
        label='Tempo para Estabilização (min)',
        min_value=1,
        help_text='Período para que os valores de nível e vazão finais se estabilizem.'
    )
    
    # Tempo total do teste (em horas)
    tempo_total_horas = forms.IntegerField(
        label='Tempo Total do Teste (h)',
        min_value=1,
        help_text='Período total do teste de bombeamento.'
    )

    def clean(self):
        cleaned_data = super().clean()
        nivel_inicial = cleaned_data.get('nivel_inicial')
        nivel_final = cleaned_data.get('nivel_final')
        vazao_inicial = cleaned_data.get('vazao_inicial')
        vazao_final = cleaned_data.get('vazao_final')
        
        if nivel_inicial is not None and nivel_final is not None and nivel_final <= nivel_inicial:
            raise forms.ValidationError('O Nível Final deve ser maior que o Nível Inicial para simular a descida do nível.')
            
        if vazao_inicial is not None and vazao_final is not None and vazao_inicial <= vazao_final:
            raise forms.ValidationError('A Vazão Inicial deve ser maior que a Vazão Final para simular a regressão da vazão.')
            
        return cleaned_data

class TesteRecuperacaoForm(forms.Form):
    # Parâmetros do Teste de Recuperação
    data_inicio = forms.DateField(
        label='Data de Início da Recuperação',
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=datetime.now().date()
    )
    hora_inicial = forms.TimeField(
        label='Hora de Início da Recuperação',
        widget=forms.TimeInput(attrs={'type': 'time'}),
        initial=datetime.now().time()
    )
    hora_final = forms.TimeField(
        label='Hora de Fim da Recuperação',
        widget=forms.TimeInput(attrs={'type': 'time'}),
        initial=(datetime.now() + timedelta(hours=1)).time()
    )
    
    # Nível Inicial e Final serão herdados do Teste de Bombeamento
    # nivel_inicial_rec = nivel_final_bombeamento
    # nivel_final_rec = nivel_inicial_bombeamento
    
    tempo_estabilizacao_min = forms.IntegerField(
        label='Tempo de Estabilização (min)',
        min_value=1,
        help_text='Tempo decorrido até os valores atingirem o Nível Final.'
    )
    
    num_leituras = forms.IntegerField(
        label='Número de Leituras até o Nível Final',
        min_value=1,
        help_text='Quantidade de simulações a serem feitas até o Nível Final.'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        hora_inicial = cleaned_data.get('hora_inicial')
        hora_final = cleaned_data.get('hora_final')
        
        if hora_inicial and hora_final and hora_final <= hora_inicial:
            raise forms.ValidationError('A Hora Final deve ser maior que a Hora Inicial.')
            
        return cleaned_data
