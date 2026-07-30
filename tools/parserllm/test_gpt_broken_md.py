import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

text = """
28<br><br>35<br><br>61<br><br>57<br><br>93<br><br>79<br><br>64<br><br>81<br><br>98<br><br>119<br><br>121<br><br>93<br><br>170<br><br>83<br><br>189<br><br>197<br><br>196<br><br>107<br><br>175<br><br>179<br><br>232<br><br>123<br><br>297<br><br>189<br><br>191<br><br>252<br><br>224<br><br>418<br><br>154<br><br>411<br><br>217<br><br>745<br><br>759<br><br>1.037<br><br>7.474<br><br>7<br><br>17<br><br>-<br><br>11<br><br>-<br><br>4<br><br>18<br><br>20<br><br>15<br><br>7<br><br>19<br><br>8<br><br>11<br><br>14<br><br>1<br><br>10<br><br>8<br><br>3<br><br>11<br><br>10<br><br>20<br><br>37<br><br>10<br><br>221<br><br>189<br><br>103<br><br>98<br><br>36<br><br>176<br><br>36<br><br>217<br><br>162<br><br>75<br><br>104<br><br>1.678<br><br>18<br><br>28<br><br>56<br><br>50<br><br>58<br><br>77<br><br>109<br><br>112<br><br>120<br><br>126<br><br>114<br><br>153<br><br>114<br><br>234<br><br>189<br><br>187<br><br>194<br><br>327<br><br>277<br><br>323<br><br>250<br><br>375<br><br>143<br><br>193<br><br>240<br><br>292<br><br>398<br><br>304<br><br>663<br><br>682<br><br>871<br><br>681<br><br>784<br><br>851<br><br>9.593<br><br>-<br><br>-<br><br>-<br><br>2<br><br>-<br><br>-<br><br>6<br><br>-<br><br>-<br><br>2<br><br>11<br><br>15<br><br>19<br><br>5<br><br>3<br><br>-<br><br>11<br><br>1<br><br>3<br><br>-<br><br>11<br><br>20<br><br><br>122<br><br>5<br><br>-<br><br>45<br><br>3<br>4<br><br><br>-<br><br>34<br><br>-<br><br>68<br><br>251<br><br>158<br><br>799<br><br>Papua Barat<br><br>Papua<br><br>Maluku Utara<br><br>Kalimantan Utara<br><br>Gorontalo<br><br>Maluku<br><br>Kep. Bangka Belitung<br><br>Sulawesi Utara<br><br>Sulawesi Barat<br><br>Bali<br><br>DI Yogyakarta<br><br>Kepulauan Riau<br><br>Kalimantan Tengah<br><br>Riau<br><br>Kalimantan Barat<br><br>Aceh<br><br>Jambi<br><br>Nusa Tenggara Barat<br><br>Kalimantan Selatan<br><br>Bengkulu<br><br>Sumatera Selatan<br><br>Lampung<br><br>DKI Jakarta<br><br>Kalimantan Timur<br><br>Sulawesi Tenggara<br><br>Banten<br><br>Sumatera Barat<br><br>Sumatera Utara<br><br>Nusa Tenggara Timur<br><br>Sulawesi Selatan<br><br>Sulawesi Tengah<br><br>Jawa Timur<br><br>Jawa Tengah<br><br>Jawa Barat<br><br>Indonesia<br><br>Puskesmas Perusahaan POS UKK GP2SP<br><br>|
"""

prompt = f"""
Teks berikut ini adalah tabel yang rusak dari PDF, di mana kolom-kolomnya digabung dan dipisah dengan <br><br>.
Urutan angka di blok pertama sesuai dengan urutan nama provinsi di blok terakhir.
Bisakah Anda mengekstrak jumlah untuk 'Sulawesi Barat', 'Sulawesi Selatan', 'Gorontalo'?
Teks: {text}
"""

res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}], temperature=0)
print(res.choices[0].message.content)
