
# Menghitung luas lingkaran

Library Python sederhana untuk menghitung luas lingkaran.



## Installastion

```
pip install lingkar33423314
```
## Implementasi

```python
from lingkaran.luas_lingkaran import Lingkaran

def main():
    jari_jari = float(input("Masukkan jari-jari lingkaran: "))
    
    lingkaran_saya = Lingkaran(jari_jari)
    luas = lingkaran_saya.hitung_luas()
    
    print(f"Luas lingkaran dengan jari-jari {jari_jari} adalah: {luas:.2f}")

if __name__ == "__main__":
    main()

```
