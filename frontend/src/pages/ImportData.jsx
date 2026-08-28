import React, { useState } from 'react';
import { UploadCloud, FileSpreadsheet, Download, CheckCircle2 } from 'lucide-react';
import { useData } from '../context/DataContext';
import { toast } from 'sonner';

const ImportData = () => {
  const { loadSample } = useData();
  const [file, setFile] = useState(null);

  return (
    <div className="space-y-6">
      <div>
        <div className="label-mono mb-2">Master Data</div>
        <h1 className="font-display text-4xl font-bold">Import Data SKU</h1>
        <p className="text-[#8b93a1] mt-2 max-w-2xl">Unggah file Excel/CSV untuk menambahkan banyak produk sekaligus. Gunakan template resmi agar kolom terbaca dengan benar.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="card-surface p-6 lg:col-span-2">
          <label className="block border-2 border-dashed border-[#242f3d] rounded-2xl p-12 text-center cursor-pointer hover:border-[#2563eb] transition-colors">
            <input type="file" accept=".xlsx,.csv" className="hidden" onChange={(e) => setFile(e.target.files[0])} />
            <UploadCloud size={44} className="mx-auto mb-4 text-[#60a5fa]" />
            <div className="font-display font-bold text-lg">{file ? file.name : 'Tarik & lepas file di sini'}</div>
            <div className="text-sm text-[#8b93a1] mt-1">atau klik untuk memilih file (.xlsx, .csv — maks 5MB)</div>
          </label>
          <button onClick={() => { if (!file) { toast.error('Pilih file terlebih dahulu'); return; } loadSample(); toast.success('Import berhasil — 15 SKU dimuat (mock)'); }} className="btn-primary w-full mt-4 flex items-center justify-center gap-2 py-3 rounded-lg font-semibold text-sm"><FileSpreadsheet size={16} /> Proses Import</button>
        </div>

        <div className="card-surface p-6">
          <h2 className="font-display text-lg font-bold mb-4">Panduan</h2>
          <ul className="space-y-3 text-sm text-[#aab4c4]">
            {['Unduh template terlebih dahulu', 'Kolom wajib: Nama, SKU, Kategori, Stok', 'Format harga tanpa titik/koma', 'SKU harus unik per produk'].map((t) => (
              <li key={t} className="flex items-start gap-2"><CheckCircle2 size={16} className="text-[#22c55e] mt-0.5 shrink-0" /> {t}</li>
            ))}
          </ul>
          <button onClick={() => toast.success('Template diunduh (mock)')} className="w-full mt-5 inline-flex items-center justify-center gap-2 text-sm font-medium px-4 py-2.5 rounded-lg border border-[#242f3d] hover:bg-[#141a24]"><Download size={15} /> Unduh Template Excel</button>
        </div>
      </div>
    </div>
  );
};

export default ImportData;
