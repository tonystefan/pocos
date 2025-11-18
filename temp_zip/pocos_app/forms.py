from django import forms
from datetime import date, timedelta

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

    max_horimetro_diario = forms.FloatField(label='Valor Máximo Diário do Horímetro', min_value=0.01)
    max_hidrometro_diario = forms.FloatField(label='Valor Máximo Diário do Hidrômetro', min_value=0.01)

    ne = forms.FloatField(label='Nível Estático (NE)', min_value=0, required=False)
    nd = forms.FloatField(label='Nível Dinâmico (ND)', min_value=0, required=False)

    PERIODICIDADE_NIVEIS = [
        ('mensal', 'Mensal (Último dia de cada mês)'),
        ('abr_out', 'Abril/Outubro (Último dia de Abr e Out)'),
    ]

    apresentar_niveis = forms.ChoiceField(
        label='Apresentar Níveis',
        choices=PERIODICIDADE_NIVEIS,
        widget=forms.RadioSelect,
        required=False,
        initial='mensal'
    )

    MESES = [
        ('jan', 'Janeiro'), ('fev', 'Fevereiro'), ('mar', 'Março'), ('abr', 'Abril'),
        ('mai', 'Maio'), ('jun', 'Junho'), ('jul', 'Julho'), ('ago', 'Agosto'),
        ('set', 'Setembro'), ('out', 'Outubro'), ('nov', 'Novembro'), ('dez', 'Dezembro'),
    ]

    meses_selecionados = forms.MultipleChoiceField(
        label='Meses para Projeção',
        choices=MESES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        initial=[m[0] for m in MESES]
    )

    registrar_sabados = forms.BooleanField(
        label='Registrar Sábados',
        required=False,
        initial=True
    )

    registrar_domingos = forms.BooleanField(
        label='Registrar Domingos',
        required=False,
        initial=True
    )

    def clean(self):
        cleaned_data = super().clean()

        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')
        if data_inicio and data_fim and data_fim < data_inicio:
            raise forms.ValidationError('A data final deve ser maior ou igual à data inicial.')

        horimetro_inicial = cleaned_data.get('horimetro_inicial')
        horimetro_final = cleaned_data.get('horimetro_final')
        if horimetro_inicial is not None and horimetro_final is not None and horimetro_final <= horimetro_inicial:
            raise forms.ValidationError('O horímetro final deve ser maior que o inicial.')

        hidrometro_inicial = cleaned_data.get('hidrometro_inicial')
        hidrometro_final = cleaned_data.get('hidrometro_final')
        if hidrometro_inicial is not None and hidrometro_final is not None and hidrometro_final <= hidrometro_inicial:
            raise forms.ValidationError('O hidrômetro final deve ser maior que o inicial.')

        max_hidrometro_diario = cleaned_data.get('max_hidrometro_diario')
        max_horimetro_diario = cleaned_data.get('max_horimetro_diario')

        if max_horimetro_diario and max_horimetro_diario > 0 and data_inicio and data_fim:
            vazao_maxima = max_hidrometro_diario / max_horimetro_diario

            meses_selecionados = cleaned_data.get('meses_selecionados', [])
            registrar_sabados = cleaned_data.get('registrar_sabados', True)
            registrar_domingos = cleaned_data.get('registrar_domingos', True)

            dias_consumo = 0
            data_atual = data_inicio
            meses_map = {
                1: 'jan', 2: 'fev', 3: 'mar', 4: 'abr', 5: 'mai', 6: 'jun',
                7: 'jul', 8: 'ago', 9: 'set', 10: 'out', 11: 'nov', 12: 'dez'
            }

            while data_atual <= data_fim:
                mes_chave = meses_map.get(data_atual.month)
                if mes_chave in meses_selecionados:
                    is_sabado = data_atual.weekday() == 5
                    is_domingo = data_atual.weekday() == 6

                    deve_consumir = True
                    if is_sabado and not registrar_sabados:
                        deve_consumir = False
                    if is_domingo and not registrar_domingos:
                        deve_consumir = False

                    if deve_consumir:
                        dias_consumo += 1
                data_atual += timedelta(days=1)

            if dias_consumo == 0:
                raise forms.ValidationError('Não há dias selecionados para projeção no período. Verifique as datas e os meses/dias da semana selecionados.')

            diferenca_hidrometro = hidrometro_final - hidrometro_inicial
            diferenca_horimetro = horimetro_final - horimetro_inicial

            consumo_medio = diferenca_hidrometro / dias_consumo
            if consumo_medio > max_hidrometro_diario:
                raise forms.ValidationError(f'O consumo médio diário necessário ({consumo_medio:.3f} m³) excede o Valor Máximo Diário do Hidrômetro ({max_hidrometro_diario:.3f} m³). Ajuste os parâmetros.')

            tempo_medio = diferenca_horimetro / dias_consumo
            if tempo_medio > max_horimetro_diario:
                raise forms.ValidationError(f'O tempo médio diário necessário ({tempo_medio:.3f} h) excede o Valor Máximo Diário do Horímetro ({max_horimetro_diario:.3f} h). Ajuste os parâmetros.')

            if diferenca_horimetro > 0:
                vazao_media_total = diferenca_hidrometro / diferenca_horimetro
                if vazao_media_total > vazao_maxima:
                    raise forms.ValidationError(f'A vazão média total necessária ({vazao_media_total:.2f} m³/h) excede a vazão máxima diária permitida ({vazao_maxima:.2f} m³/h). Ajuste os parâmetros.')

        return cleaned_data
