# Parser Bahasa JavaScript (Node.js)
## Tugas Besar IF2124 Teori Bahasa Formal dan Otomata

## Daftar Isi
* [Deskripsi Permasalahan](#deskripsi-permasalahan)
* [Struktur](#struktur)
* [Cara Menjalankan Program](#cara-menjalankan-program)
* [Identitas Kelompok](#identitas-kelompok)

## Deskripsi Permasalahan
Dalam proses pembuatan program dari sebuah bahasa menjadi instruksi yang dapat dieksekusi oleh mesin, terdapat pemeriksaan sintaks bahasa atau parsing yang dibuat oleh programmer untuk memastikan program dapat dieksekusi tanpa menghasilkan error. Parsing ini bertujuan untuk memastikan instruksi yang dibuat oleh programmer mengikuti aturan yang sudah ditentukan oleh bahasa tersebut. Baik bahasa berjenis interpreter maupun compiler, keduanya pasti melakukan pemeriksaan sintaks. Perbedaannya terletak pada apa yang dilakukan setelah proses pemeriksaan (kompilasi/compile) tersebut selesai dilakukan.

Dibutuhkan grammar bahasa dan algoritma parser untuk melakukan parsing. Sudah sangat banyak grammar dan algoritma yang dikembangkan untuk menghasilkan compiler dengan performa yang tinggi. Terdapat CFG, CNF-e, CNF+e, 2NF, 2LF, dll untuk grammar yang dapat digunakan, dan terdapat LL(0), LL(1), CYK, Earley’s Algorithm, LALR, GLR, Shift-reduce, SLR, LR(1), dll untuk algoritma yang dapat digunakan untuk melakukan parsing.

## Struktur
```bash
└───pharserr
    ├───tox.ini
    │ 
    └───src
        ├───finite_automaton.py
        ├───js_parser.py
        ├───test_parser.py
        ├───tokenizer.py
        ├───word_cfg.py
        │ 
        └───test
            ├───backus_naur.txt
            ├───inputAcc.js
            └───inputReject.js
```

## Cara Menjalankan Program
1. Clone repository ini menggunakan menggunakan command `git clone https://github.com/sofyanfirdaus/pharserr.git`.
2. Ketik source code JavaScript yang hendak di-parsing pada suatu file dengan directory yang sama dengan program `js_parser.py`, kemudian save file tersebut.
3. Jalankan program parsing menggunakan command `python js_parser.py <source_code>`.

## Identitas Kelompok
### Nama Kelompok : pharserr
| NIM  | Nama |
| ------------- | ------------- |
| 13521075 | Muhammad Rifko Favian  |
| 13521083  | Moch Sofyan Firdaus  |
| 13521098 | Fazel Ginanda  |