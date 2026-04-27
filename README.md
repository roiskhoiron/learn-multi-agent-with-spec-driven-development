# 🍳 Mini ChefGenie: Robot Koki yang Pintar!

Halo! Ini adalah proyek keren tentang **Robot Koki** yang bisa membuat kodenya sendiri hanya dengan membaca "Buku Resep" (Spesifikasi).

---

## 👶 Penjelasan Sederhana

Bayangkan kamu punya dua robot pintar:

1.  **Robot Penulis (SpecAwareCoder)**: Robot ini sangat jago menulis kode komputer. Kalau kita kasih dia catatan tentang apa yang kita mau (misalnya: "Robot, buatkan alat untuk mencatat telur dan tepung"), dia akan langsung menulis kodenya.
2.  **Robot Pemeriksa (SpecValidator)**: Robot ini seperti guru yang teliti. Dia akan membaca kode yang ditulis Robot Penulis dan mengecek, "Eh, ini kodenya sudah benar belum ya? Sesuai tidak dengan permintaan?"

**Gimana cara kerjanya?**
Kita kasih mereka **Buku Resep (Spec)**. Robot Penulis membuat kodenya, lalu Robot Pemeriksa mengeceknya. Kalau sudah oke, kodenya disimpan dan siap dipakai! Kita tidak perlu mengetik kodenya sendiri, robot-robot ini yang bekerja sama untuk kita. ✨

---

## 🏗️ Apa yang Ada di Dalam?

- `specs/`: Ini adalah "Buku Resep" atau catatan tugas untuk robot.
- `agents/`: Ini adalah otak dari Robot Penulis dan Robot Pemeriksa.
- `generated/`: Ini adalah kotak hasil kerja robot (kode Python yang sudah jadi).
- `main_spec_driven.py`: Ini adalah tombol "START" untuk menyuruh robot mulai bekerja.

## 🛠️ Cara Menjalankan

1. **Siapkan Kandang Robot (Venv):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Kasih Makan Robot (Install Dependencies):**
   ```bash
   pip install -r chefgenie-autogen/requirements.txt
   ```

3. **Mulai Kerja!**
   ```bash
   python chefgenie-autogen/main_spec_driven.py
   ```

## 🧠 Yang Kita Pelajari
Kita belajar bahwa kita bisa menyuruh AI (Kecerdasan Buatan) untuk bekerja sama seperti tim manusia. Ada yang bagian membuat, ada yang bagian memeriksa, supaya hasilnya sempurna!
