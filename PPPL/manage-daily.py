#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Aplikasi Catatan Keuangan Pribadi
Mencatat pemasukan dan pengeluaran dengan kategori
"""

import csv
from datetime import datetime
from typing import List, Dict, Optional


class FinancialTracker:
    """Class untuk mencatat transaksi keuangan"""
    
    def __init__(self, filename: str = "transactions.csv"):
        """Inisialisasi tracker dengan file CSV"""
        self.filename = filename
        self.transactions: List[Dict[str, str]] = []
        self.categories = {
            'income': ['gaji', 'bonus', 'investasi', 'hibah'],
            'expense': ['makanan', 'transportasi', 'hiburan', 'belanja', 'kesehatan']
        }
        self._load_transactions()
    
    def _load_transactions(self) -> None:
        """Memuat transaksi dari file CSV"""
        try:
            with open(self.filename, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.transactions = list(reader)
        except FileNotFoundError:
            # File belum ada, buat file baru dengan header
            with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self._get_fieldnames())
                writer.writeheader()
    
    def _save_transactions(self) -> None:
        """Menyimpan transaksi ke file CSV"""
        with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self._get_fieldnames())
            writer.writeheader()
            writer.writerows(self.transactions)
    
    def _get_fieldnames(self) -> List[str]:
        """Mendapatkan nama kolom untuk CSV"""
        return ['date', 'type', 'category', 'amount', 'description']
    
    def add_transaction(
        self,
        transaction_type: str,
        category: str,
        amount: float,
        description: str = ""
    ) -> Dict[str, str]:
        """Menambahkan transaksi baru"""
        if transaction_type not in ['income', 'expense']:
            raise ValueError("Jenis transaksi harus 'income' atau 'expense'")
        
        if category not in self.categories[transaction_type]:
            raise ValueError(f"Kategori tidak valid. Pilih: {', '.join(self.categories[transaction_type])}")
        
        if amount <= 0:
            raise ValueError("Jumlah harus lebih besar dari 0")
        
        transaction = {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'type': transaction_type,
            'category': category,
            'amount': f"{amount:.2f}",
            'description': description
        }
        
        self.transactions.append(transaction)
        self._save_transactions()
        return transaction
    
    def get_balance(self) -> float:
        """Menghitung saldo saat ini"""
        balance = 0.0
        for transaction in self.transactions:
            amount = float(transaction['amount'])
            if transaction['type'] == 'income':
                balance += amount
            else:
                balance -= amount
        return balance
    
    def get_transactions(
        self,
        transaction_type: Optional[str] = None,
        category: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """Mendapatkan daftar transaksi dengan filter opsional"""
        filtered = self.transactions
        
        if transaction_type:
            filtered = [t for t in filtered if t['type'] == transaction_type]
        
        if category:
            filtered = [t for t in filtered if t['category'] == category]
        
        return filtered
    
    def get_summary(self) -> Dict[str, float]:
        """Mendapatkan ringkasan keuangan"""
        summary = {
            'total_income': 0.0,
            'total_expense': 0.0,
            'balance': 0.0
        }
        
        for transaction in self.transactions:
            amount = float(transaction['amount'])
            if transaction['type'] == 'income':
                summary['total_income'] += amount
            else:
                summary['total_expense'] += amount
        
        summary['balance'] = summary['total_income'] - summary['total_expense']
        return summary


def display_menu() -> None:
    """Menampilkan menu aplikasi"""
    print("\n=== Aplikasi Catatan Keuangan ===")
    print("1. Tambah Pemasukan")
    print("2. Tambah Pengeluaran")
    print("3. Lihat Saldo")
    print("4. Lihat Riwayat Transaksi")
    print("5. Lihat Ringkasan Keuangan")
    print("6. Keluar")


def display_categories(tracker: FinancialTracker, transaction_type: str) -> None:
    """Menampilkan kategori yang tersedia"""
    print(f"\nKategori {transaction_type}:")
    for i, category in enumerate(tracker.categories[transaction_type], 1):
        print(f"{i}. {category}")


def get_category_choice(tracker: FinancialTracker, transaction_type: str) -> str:
    """Mendapatkan pilihan kategori dari pengguna"""
    while True:
        display_categories(tracker, transaction_type)
        try:
            choice = int(input("Pilih kategori (nomor): "))
            if 1 <= choice <= len(tracker.categories[transaction_type]):
                return tracker.categories[transaction_type][choice - 1]
            print("Pilihan tidak valid. Silakan coba lagi.")
        except ValueError:
            print("Masukkan angka yang valid.")


def display_transactions(transactions: List[Dict[str, str]]) -> None:
    """Menampilkan daftar transaksi"""
    if not transactions:
        print("Tidak ada transaksi.")
        return
    
    print("\nDaftar Transaksi:")
    print("-" * 70)
    print("Tanggal           | Jenis     | Kategori    | Jumlah    | Deskripsi")
    print("-" * 70)
    
    for t in transactions:
        print(
            f"{t['date'][:16]} | {t['type']:<8} | {t['category']:<11} | "
            f"{t['amount']:>9} | {t['description']}"
        )


def main() -> None:
    """Fungsi utama untuk menjalankan aplikasi"""
    tracker = FinancialTracker()
    
    while True:
        display_menu()
        choice = input("Pilih menu (1-6): ").strip()
        
        if choice == '1':
            # Tambah pemasukan
            try:
                amount = float(input("Jumlah pemasukan: "))
                category = get_category_choice(tracker, 'income')
                description = input("Deskripsi (opsional): ").strip()
                tracker.add_transaction('income', category, amount, description)
                print("Pemasukan berhasil dicatat!")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == '2':
            # Tambah pengeluaran
            try:
                amount = float(input("Jumlah pengeluaran: "))
                category = get_category_choice(tracker, 'expense')
                description = input("Deskripsi (opsional): ").strip()
                tracker.add_transaction('expense', category, amount, description)
                print("Pengeluaran berhasil dicatat!")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == '3':
            # Lihat saldo
            balance = tracker.get_balance()
            print(f"\nSaldo saat ini: {balance:.2f}")
        
        elif choice == '4':
            # Lihat riwayat transaksi
            print("\nFilter transaksi:")
            print("1. Semua transaksi")
            print("2. Hanya pemasukan")
            print("3. Hanya pengeluaran")
            filter_choice = input("Pilih filter (1-3): ").strip()
            
            if filter_choice == '1':
                transactions = tracker.get_transactions()
            elif filter_choice == '2':
                transactions = tracker.get_transactions('income')
            elif filter_choice == '3':
                transactions = tracker.get_transactions('expense')
            else:
                print("Pilihan tidak valid. Menampilkan semua transaksi.")
                transactions = tracker.get_transactions()
            
            display_transactions(transactions)
        
        elif choice == '5':
            # Lihat ringkasan keuangan
            summary = tracker.get_summary()
            print("\nRingkasan Keuangan:")
            print(f"Total Pemasukan: {summary['total_income']:.2f}")
            print(f"Total Pengeluaran: {summary['total_expense']:.2f}")
            print(f"Saldo: {summary['balance']:.2f}")
        
        elif choice == '6':
            # Keluar
            print("Terima kasih telah menggunakan aplikasi!")
            break
        
        else:
            print("Pilihan tidak valid. Silakan pilih 1-6.")


if __name__ == "__main__":
    main()