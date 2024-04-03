import pandas as pd
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Baca data dari file Excel
data = pd.read_excel('DATA KESEHATAN.xlsx')
print(data.shape)

# Input variables
tekanan_darah = ctrl.Antecedent(np.arange(80, 181, 1), 'tekanan_darah')
kolesterol = ctrl.Antecedent(np.arange(100, 301, 1), 'kolesterol')
glukosa_darah = ctrl.Antecedent(np.arange(70, 201, 1), 'glukosa_darah')

#Output variable
risiko_jantung = ctrl.Consequent(np.arange(0, 101, 1), 'risiko_jantung')

# Fungsi keanggotaan untuk tekanan_darah
tekanan_darah.automf(3)
kolesterol.automf(3)
glukosa_darah.automf(3)

# Fungsi keanggotaan untuk risiko_jantung
risiko_jantung['rendah'] = fuzz.trimf(risiko_jantung.universe, [0, 25, 50])
risiko_jantung['sedang'] = fuzz.trimf(risiko_jantung.universe, [40, 60, 80])
risiko_jantung['tinggi'] = fuzz.trimf(risiko_jantung.universe, [60, 75, 100])

# Rules
rule1 = ctrl.Rule(tekanan_darah['poor'] | kolesterol['poor'] | glukosa_darah['poor'], risiko_jantung['rendah'])
rule2 = ctrl.Rule(tekanan_darah['average'] | kolesterol['average'] | glukosa_darah['average'], risiko_jantung['sedang'])
rule3 = ctrl.Rule(tekanan_darah['good'] | kolesterol['good'] | glukosa_darah['good'], risiko_jantung['tinggi'])

# Control system
risiko_jantung_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
risiko_jantung_sim = ctrl.ControlSystemSimulation(risiko_jantung_ctrl)

# List untuk menyimpan hasil
hasil = []

# Loop melalui setiap record data dan lakukan simulasi kontrol untuk masing-masing
for idx, row in data.iterrows():
    tekanan_darah_val = row['tekanan_darah']
    kolesterol_val = row['kolestrol']
    glukosa_darah_val = row['glukosa_darah']
    # Set nilai input berdasarkan record saat ini
    risiko_jantung_sim.input['tekanan_darah'] = tekanan_darah_val
    risiko_jantung_sim.input['kolesterol'] = kolesterol_val
    risiko_jantung_sim.input['glukosa_darah'] = glukosa_darah_val

    # Lakukan perhitungan
    risiko_jantung_sim.compute()

    # Simpan hasil untuk record saat ini
    tingkat_risiko = risiko_jantung_sim.output['risiko_jantung']
    if tingkat_risiko <= 33:
        keterangan = 'Aman'
    elif tingkat_risiko <= 66:
        keterangan = 'Waspada'
    else:
        keterangan = 'Gawat nih'
    hasil.append({'Record': idx+1, 'Tingkat Risiko Jantung': tingkat_risiko, 'Keterangan': keterangan})

# Buat dataframe dari hasil
hasil_df = pd.DataFrame(hasil)

# Simpan dataframe ke dalam file Excel
hasil_df.to_excel('hasil_risiko_jantung.xlsx', index=False)

print("Hasil telah disimpan dalam file 'hasil_risiko_jantung.xlsx'")
