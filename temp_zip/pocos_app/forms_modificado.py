from django import forms
from datetime import date

class ParametrosForm(forms.Form):
    data_inicio = forms.DateField(
        label='Data Início', 
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='Data de início da projeção (formato: DD/MM/AAAA)'
    )
    data_fim = forms.DateField(
        label='Data Fim', 
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='Data de fim da projeção (formato: DD/MM/AAAA)'
    )
    horimetro_inicial = forms.FloatField(label='Horímetro Inicial', min_value=0)
    horimetro_final = forms.FloatField(label='Horímetro Final', min_value=0)
    hidrometro_inicial = forms.FloatField(label='Hidrômetro Inicial', min_value=0)
    hidrometro_final = forms.FloatField(label='Hidrômetro Final', min_value=0)
    
    # Valores máximos diários
    max_horimetro_diario = forms.FloatField(label='Valor Máximo Diário do Horímetro', min_value=0.01)
    max_hidrometro_diario = forms.FloatField(label='Valor Máximo Diário do Hidrômetro', min_value=0.01)
    
    # Valores mensais
    MESES = [
        ('jan', 'Janeiro'),
        ('fev', 'Fevereiro'),
        ('mar', 'Março'),
        ('abr', 'Abril'),
        ('mai', 'Maio'),
        ('jun', 'Junho'),
        ('jul', 'Julho'),
        ('ago', 'Agosto'),
        ('set', 'Setembro'),
        ('out', 'Outubro'),
        ('nov', 'Novembro'),
        ('dez', 'Dezembro'),
    ]

    meses_selecionados = forms.MultipleChoiceField(
        label='Meses para Projeção',
        choices=MESES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        initial=[m[0] for m in MESES] # Todos os meses selecionados por padrão
    )
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Validar que a data final é maior ou igual à data inicial
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')
        if data_inicio and data_fim and data_fim < data_inicio:
            raise forms.ValidationError('A data final deve ser maior ou igual à data inicial.')
        
        # Validar que o horímetro final é maior que o inicial
        horimetro_inicial = cleaned_data.get('horimetro_inicial')
        horimetro_final = cleaned_data.get('horimetro_final')
        if horimetro_inicial and horimetro_final and horimetro_final <= horimetro_inicial:
            raise forms.ValidationError('O horímetro final deve ser maior que o inicial.')
        
        # Validar que o hidrômetro final é maior que o inicial
        hidrometro_inicial = cleaned_data.get('hidrometro_inicial')
        hidrometro_final = cleaned_data.get('hidrometro_final')
        if hidrometro_inicial and hidrometro_final and hidrometro_final <= hidrometro_inicial:
            raise forms.ValidationError('O hidrômetro final deve ser maior que o inicial.')
        
        return cleaned_data

