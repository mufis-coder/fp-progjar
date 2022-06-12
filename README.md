# Final Pratikum - Pemrograman Jaringan

Repository Final Project - mata kuliah Pemrograman Jaringan

Format data yang dikirim:

```txt
{"Player":PLAYER, "Action": ACTION, "Value":None}
```

## Player

- PLAYER: merupakan data untuk menyimpan player mana pengirim informasi!

```txt
PLAYER = {0:"Player1", 1:"Player2"}
```

## Action

- ACTION: merupakan data untuk menyimpan aksi apa yang dilakukan player!

```txt
ACTION = {-2:"Init Thread", -1:"End", 0:"Start in", 
            1:"Start", 2:"Jump", 3:"Add Pipe", 4:"Height Pipe", 5:"Bird Height"}
```

### Penjelasan Action

- "Init Thread": digunakan client/player untuk memberitahu server bahwa ada player yang login.

- "End": digunakan client/player untuk memberitahu server bahwa ada player yang keluar dari game atau karakternya mati.

- "Start in": digunakan server untuk memberitahu tiap player bahwa game akan dimulai.

- "Start": digunakan server untuk memberitahu tiap player bahwa game dimulai.

- "Jump": digunakan client/player untuk memberitahu server bahwa ada player yang melakukan jump karakter.

- "Add Pipe": digunakan client/player untuk memberi tahu server untuk membuat angka tinggi pipe selanjutnya.

- "Height Pipe": digunakan server untuk mengirim data tinggi pipe selanjutnya.

- "Bird Height": digunakan client/player untuk mengirim data sinkronisasi tinggi burung.

Khusus pada action "Start in", "Height Pipe", dan "Bird Height" data memiliki value yang tidak None.

- "Start in": berisi value waktu (dalam detik) untuk memulai game. Digenerate oleh ```server.py```.

- "Height Pipe": berisi value int (random) untuk membuat tinggi pipa. Digenerate oleh ```server.py```.

- "Bird Height": berisi value int (tinggi burung) untuk sinkronisasi burung antar player. Digenerate oleh ```main{1/2}.py```.

## Perbedaan ```main.py``` dan ```main2.py```

Pada ```main.py``` yang digunakan untuk player1, memiliki perbedaan code berikut:

```txt
PLAYER = 0
KEYJUMP = pygame.K_SPACE
```

Pada ```main2.py``` yang digunakan untuk player2, memiliki perbedaan code berikut:

```txt
PLAYER = 1
KEYJUMP = pygame.K_UP
```
