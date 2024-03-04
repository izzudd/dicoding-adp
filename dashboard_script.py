# %% [markdown]
# # Proyek Analisis Data: Bike Sharing Dataset
# - **Nama:** Rahmatulloh Daffa Izzuddin Wahid
# - **Email:** 
# - **ID Dicoding:** zudd_in

# %% [markdown]
# ## Menentukan Pertanyaan Bisnis

# %% [markdown]
# - Bagaimana tingkat mobilitas kota pada waktu tertentu, kapan cenderung terjadi keramaian?
# - Apa saja faktor yang menyebabkan ramainya mobilitas kota dengan sepeda?

# %% [markdown]
# ## Import Semua Packages/Library yang Digunakan

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()

# %% [markdown]
# ## Data Wrangling

# %% [markdown]
# ### Gathering Data

# %%
!rm -rf data
!gdown 1RaBmV6Q6FYWU4HWZs80Suqd7KQC34diQ -O dataset.zip
!unzip dataset.zip -d data
!rm dataset.zip

# %%
df = pd.read_csv('data/hour.csv')

# %% [markdown]
# ### Assessing Data
# 
# Kondisi data dilihat dengan mendaftar kolom apa saya yang ada berikut ringkasan setiap kolom dan mengecek apakah ada nilai null, nan, dan duplikat pada data.
# 
# Terdapat 17 kolom pada data dengan rincian sebagai berikut:
# - `instant`: record index
# - `dteday` : date
# - `season` : season (1:winter, 2:spring, 3:summer, 4:fall)
# - `yr` : year (0: 2011, 1:2012)
# - `mnth` : month ( 1 to 12)
# - `hr` : hour (0 to 23)
# - `holiday` : weather day is holiday or not (extracted from http://dchr.dc.gov/page/holiday-schedule)
# - `weekday` : day of the week
# - `workingday` : if day is neither weekend nor holiday is 1, otherwise is 0.
# - `weathersit` : 
#   - 1: Clear, Few clouds, Partly cloudy, Partly cloudy
#   - 2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist
#   - 3: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds
#   - 4: Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog
# - `temp` : Normalized temperature in Celsius. The values are derived via (t-t_min)/(t_max-t_min), t_min=-8, t_max=+39 (only in hourly scale)
# - `atemp`: Normalized feeling temperature in Celsius. The values are derived via (t-t_min)/(t_max-t_min), t_min=-16, t_max=+50 (only in hourly scale)
# - `hum`: Normalized humidity. The values are divided to 100 (max)
# - `windspeed`: Normalized wind speed. The values are divided to 67 (max)
# - `casual`: count of casual users
# - `registered`: count of registered users
# - `cnt`: count of total rental bikes including both casual and registered

# %%
df.describe(include='all')

# %% [markdown]
# Tidak terdapat nilai null, nan, dan duplikat pada data.

# %%
print('How many data is null?', df.isnull().sum().sum())
print('How many data is nan?', df.isna().sum().sum())
print('How many data duplicated?', df.duplicated().sum())

# %% [markdown]
# Hasil pengecekan terhadap tipe data memperlihatkan adanya data dteday dengan tipe object, data ini dapat diubah menjadi tipe datetime.

# %%
df.info()

# %% [markdown]
# ### Cleaning Data

# %% [markdown]
# Mengubah format data beberapa kolom:
# - `detday` menjadi `datetime`
# - `yt` menjadi tahun 2011 dan 2012
# - `mnth`, `weekday`, `season` menjadi ordinal `string` (category)
# - `holiday`, `workingday` menjadi `boolean`
# - mengembalikan suhu ke celsius

# %%
from pandas.api.types import CategoricalDtype

cat_weekday = CategoricalDtype(categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], ordered=True)
cat_season = CategoricalDtype(categories=['winter', 'spring', 'summer', 'fall'], ordered=True)
cat_month = CategoricalDtype(categories=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], ordered=True)
clean_df = df.copy()
clean_df['dteday'] = pd.to_datetime(df['dteday'])
clean_df['yr'] = clean_df['dteday'].dt.year

clean_df['mnth'] = clean_df['dteday'].dt.month_name().astype(cat_month)
clean_df['weekday'] = clean_df['dteday'].dt.day_name().astype(cat_weekday)
clean_df['season'] = clean_df['season'].map({1:'winter', 2:'spring', 3:'summer', 4:'fall'}).astype(cat_season)

clean_df['holiday'] = clean_df['holiday'].astype(bool)
clean_df['workingday'] = clean_df['workingday'].astype(bool)

clean_df['temp'] = clean_df['temp'] * (39 + 8) - 8
clean_df['atemp'] = clean_df['atemp'] * (50+16) - 16
clean_df['windspeed'] = clean_df['windspeed'] * 67
clean_df['hum'] = clean_df['hum'] * 100

clean_df.info()

# %%
clean_df.head()

# %% [markdown]
# ## Exploratory Data Analysis (EDA)

# %% [markdown]
# ### Explore jumlah pesepeda pada tiap harinya

# %%

all_day_cnt = clean_df.groupby('dteday')[['casual', 'registered', 'cnt']].sum().reset_index()
all_day_cnt = all_day_cnt.melt(id_vars=['dteday'], var_name='kind', value_name='sum')
plt.figure(figsize=(16, 4))
sns.lineplot(all_day_cnt, hue='kind', x='dteday', y='sum')
plt.ylabel('Ride count')
plt.xlabel('Date')
plt.show()

# %% [markdown]
# Hasil plot menunjukkan adanya pola jumlah pesepeda yang naik turun dengan interval tertentu. Asumsi awal yang dihasilkan adalah faktor hari libur, pada hari libur pesepeda akan cenderung menurun. Dapat dilihat juga bahwa terjadi kenaikan jumlah pesepeda pada tahun 2012 relatif terhadap tahun 2011.
# 
# Keramaian pesepeda cenderung berada pada pertengahan tahun, dapat diasumsikan hal ini terjadi karena musim panas yang terjadi, sedangkan pada musim salju (akhir dan awal tahun) pengunaan sepeda relatif lebih sedikit.

# %% [markdown]
# ### Explore hubungan antara fitur alam (temp, atemp, hum, dan windspeed) dengan banyaknya pesepeda

# %%
natural_cols = ['temp', 'atemp', 'hum', 'windspeed']
correlation = clean_df[[*natural_cols, 'cnt']].corr()
sns.heatmap(correlation, annot=True)
plt.show()

# %% [markdown]
# Dari heatmap tersebut didapatkan bahwa banyaknya pesepeda berbanding lurus dengan temperatur dan cenderung berbanding terbalik dengan kelembaban. Dengan kata lain:
# - Semakin tinggi temperatur semakin banyak pesepeda
# - Semakin rendah kelembaban semakin banyak pesepeda
# - Kecepatan angin tidak memiliki kontribusi signifikan pada jumlah pesepeda

# %% [markdown]
# ### Explore distribusi fitur alam (temp, atemp, hum, dan windspeed)

# %%
fig, ax = plt.subplots(2, 2, figsize=(14, 8))
natural_dist = clean_df[natural_cols]
for i, col in enumerate(natural_cols):
  _ax = ax[i//2,i%2]
  plot = sns.histplot(natural_dist, x=col, kde=True, ax=_ax)

# %% [markdown]
# Hasil plotting memperlihakan bahwa semua data cenderung terdistribusi normal kecuali `windspeed` yang right skewed, hal ini sekaligus menjelaskan mengapa kecepatan angin tidak berpengaruh secara signifikan pada jumlah pesepeda.

# %% [markdown]
# ### Explore klaster peserbaran musim berdasarkan temperatur dan jumlah pesepeda

# %%
sns.scatterplot(clean_df, x='temp', y='cnt', hue='season')
plt.ylabel('Ride count')
plt.xlabel('Temperature (Celcius)')
plt.plot()

# %% [markdown]
# Hasil plot menunjukkan klaster berdasarkan suhu dan jumlah pesepeda cukup terlihat jelas pada musim panas dan dingin. Musim semi dan gugur memiliki persebarab suhu dan jumlah pesepeda yang cukup seragam

# %% [markdown]
# ### Explore jumlah sampel pada tiap musim dan jam

# %%
fig, ax = plt.subplots(1, 2, figsize=(14, 4))
season_dist = clean_df['season'].astype(str)
hour_dist = clean_df['hr'].astype(str)

sns.histplot(season_dist, ax=ax[0])
ax[0].set_ylabel('Ride count')
ax[0].set_xlabel('Season')

sns.histplot(hour_dist, ax=ax[1])
ax[1].set_ylabel('Ride count')
ax[1].set_xlabel('Time (24 hour)')

plt.show()

# %% [markdown]
# Hasil plotting terlihat beberapa jumlah sampel yang tidak seimbang, diantaranya:
# - Terdapat lebih banyak sampel pada musim panas dan semi
# - Terdapat lebih sedikit sampel yang diambil pada pukul 02.00 hingga 05.00

# %% [markdown]
# ### Explore jumlah workingday dan holiday

# %%
def convert_holyworkday(x):
  work = 'work' if x['workingday'] else 'off'
  holiday = '(holiday)' if x['holiday'] else ''
  return f'{work} {holiday}'.strip()
workholy_day = clean_df[['workingday', 'holiday']].agg(convert_holyworkday, axis=1)
sns.histplot(workholy_day)
plt.ylabel('Ride count')
plt.xlabel('Kind of day')
plt.show()

# %% [markdown]
# Hasil plot menunjukkan terdapat 3 jenis hari, yaitu:
# - Hari kerja
# - Hari libur kerja
# - Hari libur holiday
# 
# Terlihat tidak ada hari kerja holiday

# %% [markdown]
# ## Visualization & Explanatory Analysis

# %% [markdown]
# ### Waktu cenderung terjadi keramaian

# %% [markdown]
# #### 1. Berdasarkan musim

# %%
count_cols = ['casual', 'registered', 'cnt']
seasonal_cnt = clean_df.groupby(['season'])[count_cols].mean().reset_index()
seasonal_cnt = seasonal_cnt.melt(id_vars=['season'], var_name='kind', value_name='mean')
sns.pointplot(seasonal_cnt, hue='kind', x='season', y='mean')
plt.ylabel('Average bike ride')
plt.xlabel('Season')
plt.show()

# %% [markdown]
# Hasil diagram tersebut terlihat bahwa tingginya mobilitas cenderung terjadi pada musim panas dan musim semi. Hal ini juga mendukung hasil eksplorasi sebelumnya yang memperlihatkan korelasi positif antara suhu dan jumlah pesepeda.
# 
# Dari diagram tersebut juga bisa diambil kesimpulan bahwa pesepeda kasual lebih sedikit dibanding pesepeda yang terdaftar.

# %% [markdown]
# #### 2. Berdasarkan jam

# %%

hourly_count = clean_df.groupby(['hr'])[count_cols].mean().reset_index()
hourly_count = hourly_count.melt(id_vars=['hr'], var_name='kind', value_name='mean')
sns.pointplot(hourly_count, hue='kind', x='hr', y='mean')
plt.ylabel('Average bike ride')
plt.xlabel('Time (24 hour)')
plt.show()

# %% [markdown]
# Hasil plotting terlihat bahwa tingginya mobilitas dengan sepeda terjadi pada pukul 07.00 hingga 09.00 dan pukul 16.00 hingga 19.00. Peningkatan jumlah mobilitas ini menjadi pertanda waktu berangkat dan pulangnya orang-orang.
# 
# Dari hasil plotting didapatkan juga bahwa pengguna sepeda kasual memiliki kecenderungan bersepeda sepanjang hari, yaitu pukul 07.00 hingga 21.00. Ini bisa jadi disebabkan karena pengguna sepeda kasual lebih fleksibel dalam penggunaan sepedanya sehingga dapat menggunakan sepeda sepanjang hari tanpa perlu dititipkan dan bergantian.

# %% [markdown]
# #### 3. Berdsarkan jam pada setiap musim

# %%
hourly_seasonal_cnt = clean_df.pivot_table(values='cnt', index=['season', 'hr'], aggfunc='mean').reset_index()
sns.pointplot(hourly_seasonal_cnt, hue='season', x='hr', y='cnt')
plt.ylabel('Average bike ride')
plt.xlabel('Time (24 hour)')
plt.show()

# %% [markdown]
# Hasil plot menunjukkan kecenderungan lonjakan jumlah pesepeda pada tiap musim tidak jauh berbeda. Diagram ini menunjukkan kekonsistenan 2 diagram sebelumnya.

# %% [markdown]
# #### 4. Berdasarkan bulan

# %%

monthly_cnt = clean_df.groupby(['mnth'])[count_cols].mean().reset_index()
monthly_cnt = monthly_cnt.melt(id_vars=['mnth'], var_name='kind', value_name='mean')
sns.pointplot(monthly_cnt, hue='kind', x='mnth', y='mean')
plt.xticks(rotation=90)
plt.ylabel('Average bike ride')
plt.xlabel('Month')
plt.show()

# %% [markdown]
# ### Faktor yang mempengaruhi keramaian pesepeda

# %% [markdown]
# #### 1. Berdasarkan hari (weekend, weekday, holiday)

# %%
holyworking_cnt = clean_df[['holiday', 'workingday', *count_cols]].copy()
holyworking_cnt['holyworkday'] = holyworking_cnt.agg(convert_holyworkday, axis=1)
holyworking_cnt = holyworking_cnt[['holyworkday', *count_cols]].groupby('holyworkday').mean().reset_index()
holyworking_cnt = holyworking_cnt.melt(id_vars=['holyworkday'], var_name='kind', value_name='mean')

sns.barplot(holyworking_cnt, hue='kind', x='holyworkday', y='mean')
plt.ylabel('Average bike ride')
plt.xlabel('Kind of day')
plt.show()

# %%

day_cnt = clean_df[['weekday', *count_cols]].groupby('weekday').mean().reset_index()
day_cnt = day_cnt.melt(id_vars=['weekday'], var_name='kind', value_name='mean')
sns.pointplot(day_cnt, hue='kind', x='weekday', y='mean')
plt.xticks(rotation=30)
plt.ylabel('Average bike ride')
plt.xlabel('Weekday')
plt.show()

# %% [markdown]
# Hasil plotting menunjukkan bahwa penggunaan sepeda paling tinggi terjadi pada hari kerja, walaupun tidak berselisih jauh dengan ketika hari libur. Temuan lain menunjukkan bahwa pada hari libur pengguna sepeda kasual mengalami peningkatan dan penyewa sepeda mengalami penurunan.

# %% [markdown]
# #### 3. Berdsarkan kondisi cuaca

# %%

weather_cnt = clean_df[['weathersit', 'cnt']].groupby('weathersit').mean().reset_index()
plot = sns.barplot(weather_cnt, hue='weathersit', x='weathersit', y='cnt', legend=False)
plt.ylabel('Average bike ride')
plt.xlabel('Weather condition')
plt.show()

wheathersit = {
  1: 'Clear, Few clouds, Partly cloudy, Partly cloudy',
  2: 'Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist',
  3: 'Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds',
  4: 'Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog'
}
for key, val in wheathersit.items():
  print(key, val)

# %% [markdown]
# Diagram menunjukkan kecenderungan orang-orang menggunakan sepeda ketika kondisi cerah hingga sedikit berkabut. Sebaliknya, pesepeda ketika hujan dan bersalju relatif lebih sedikit.

# %% [markdown]
# ## Conclusion

# %% [markdown]
# ### Conclusion pertanyaan 1: 
# - Keramaian pesepeda cenderung terjadi pada musim semi dan musim panas.
# - Keramaian pesepeda cenderung terjadi pada siang hari, dengan lonjakan pada pukul 07.00 hingga 09.00 dan 16.00 hingga 19.00, sekaligus menandakan waktu berangkat dan pulangnya orang-orang.
# - Tren perbedaan pesepeda menurut jam pada musim yang berbeda menunjukkan pola yang bersesuaian dengan 2 pernyataan sebelumnya.
# - Keramaian pesepeda berdasarkan bulan cenderung mengikuti musim yang ada, yaitu penurunan terjadi pada bulan november hingga februari (musim dingin).
# 
# ### Conclusion pertanyaan 2:
# - Semakin tinggi suhu udara maka semakin banyak pesepeda, sebaliknya semakin rendah kelembaban maka semakin banyak jumlah pesepeda. Kecepatan angin tidak memiliki kontribusi signifikan terhadap jumlah pesepeda.
# - Keramaian pesepeda cenderung terjadi pada hari kerja dan hari libur kerja, dengan perbedaan yang tidak signifikan. Pada hari libur tertentu (hari raya, peringatan, dll) jumlah pesepeda relatif lebih sedikit walaupun tidak signifikan.
# - Pada weekday (senin hingga jumat) kebanyakan sepeda yang dipakai merupakan sepeda sewa (registerd), sedangkan pada weekend (sabtu dan minggu) terjadi kenaikan penggunaan sepeda kasual.
# - Sepeda lebih banyak digunakan pada kondisi cuaca cerah hingga berkabut, sedangkan relatif lebih jarang digunakan pada cuaca hujan hingga badai salju.


