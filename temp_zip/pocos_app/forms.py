from django import forms

class ParametrosForm(forms.Form):
    ano_inicio = forms.IntegerField(label='Ano Início', min_value=2000, max_value=2100)
    ano_fim = forms.IntegerField(label='Ano Fim', min_value=2000, max_value=2100)
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
    
    # Campos dinâmicos para cada mês
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for codigo, nome in self.MESES:
            self.fields[f'vazao_{codigo}'] = forms.FloatField(
                label=f'Vazão m³/h ({nome})', 
                min_value=0,
                initial=0.03
            )
            self.fields[f'horas_{codigo}'] = forms.FloatField(
                label=f'Horas/Dia ({nome})', 
                min_value=0,
                initial=0.40
            )
            self.fields[f'dias_{codigo}'] = forms.IntegerField(
                label=f'Dias ({nome})', 
                min_value=0, 
                max_value=31,
                initial=30
            )
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Validar que o ano final é maior ou igual ao ano inicial
        ano_inicio = cleaned_data.get('ano_inicio')
        ano_fim = cleaned_data.get('ano_fim')
        if ano_inicio and ano_fim and ano_fim < ano_inicio:
            raise forms.ValidationError('O ano final deve ser maior ou igual ao ano inicial.')
        
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
