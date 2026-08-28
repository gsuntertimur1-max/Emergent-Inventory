import React, { useState } from 'react';
import { Plus, X, ShieldCheck, User as UserIcon } from 'lucide-react';
import { useData } from '../context/DataContext';
import { toast } from 'sonner';

const ROLE_COLOR = { 'Administrator': '#ef4444', 'Supervisor': '#a855f7', 'Operator': '#3b82f6', 'Pemantau': '#8b93a1' };

const Pengguna = () => {
  const { users, addUser } = useData();
  const [modal, setModal] = useState(false);
  const [form, setForm] = useState({ name: '', username: '', email: '', role: 'Operator' });

  const save = () => {
    if (!form.name || !form.username) { toast.error('Nama & username wajib diisi'); return; }
    addUser(form); toast.success('Pengguna ditambahkan'); setModal(false); setForm({ name: '', username: '', email: '', role: 'Operator' });
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <div className="label-mono mb-2">Kontrol Akses</div>
          <h1 className="font-display text-4xl font-bold">Pengguna</h1>
          <p className="text-[#8b93a1] mt-2">{users.length} akun terdaftar · kelola peran & akses</p>
        </div>
        <button onClick={() => setModal(true)} className="btn-primary inline-flex items-center gap-2 text-sm font-semibold px-4 py-2.5 rounded-lg"><Plus size={15} /> Tambah Pengguna</button>
      </div>

      <div className="card-surface p-6">
        <div className="overflow-x-auto">
          <table className="w-full text-sm tbl">
            <thead><tr className="text-left border-b border-[#1a222e]">{['Nama', 'Username', 'Email', 'Peran', 'Status'].map((h) => <th key={h} className="py-2.5 pr-4 font-semibold">{h}</th>)}</tr></thead>
            <tbody>
              {users.map((u) => (
                <tr key={u.id} className="tbl-row border-b border-[#131a24]">
                  <td className="py-3 pr-4"><div className="flex items-center gap-3"><div className="w-9 h-9 rounded-full bg-[#1a222e] flex items-center justify-center text-[#60a5fa]"><UserIcon size={16} /></div><span className="font-medium">{u.name}</span></div></td>
                  <td className="py-3 pr-4 font-mono text-xs text-[#8b93a1]">{u.username}</td>
                  <td className="py-3 pr-4 text-[#aab4c4]">{u.email}</td>
                  <td className="py-3 pr-4"><span className="inline-flex items-center gap-1.5 text-xs px-2.5 py-1 rounded-full font-medium" style={{ background: `${ROLE_COLOR[u.role]}22`, color: ROLE_COLOR[u.role] }}><ShieldCheck size={12} /> {u.role}</span></td>
                  <td className="py-3 pr-4"><span className={`text-xs px-2.5 py-1 rounded-full ${u.active ? 'bg-[#22c55e]/15 text-[#22c55e]' : 'bg-[#6b7688]/15 text-[#8b93a1]'}`}>{u.active ? 'Aktif' : 'Nonaktif'}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {modal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4" onClick={() => setModal(false)}>
          <div className="card-surface w-full max-w-md p-6 fade-up" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-5"><h2 className="font-display text-xl font-bold">Tambah Pengguna</h2><button onClick={() => setModal(false)} className="text-[#8b93a1] hover:text-white"><X size={20} /></button></div>
            <div className="space-y-4">
              {[['name', 'Nama Lengkap'], ['username', 'Username'], ['email', 'Email']].map(([k, l]) => (
                <div key={k}><label className="text-xs font-medium mb-1 block text-[#8b93a1]">{l}</label><input value={form[k]} onChange={(e) => setForm({ ...form, [k]: e.target.value })} className="w-full bg-[#0b0f17] border border-[#242f3d] rounded-lg px-3 py-2.5 text-sm outline-none focus:border-[#2563eb]" /></div>
              ))}
              <div><label className="text-xs font-medium mb-1 block text-[#8b93a1]">Peran</label><select value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })} className="w-full bg-[#0b0f17] border border-[#242f3d] rounded-lg px-3 py-2.5 text-sm outline-none focus:border-[#2563eb]">{['Administrator', 'Supervisor', 'Operator', 'Pemantau'].map((r) => <option key={r}>{r}</option>)}</select></div>
            </div>
            <div className="flex justify-end gap-2 mt-6"><button onClick={() => setModal(false)} className="px-4 py-2.5 rounded-lg border border-[#242f3d] text-sm hover:bg-[#141a24]">Batal</button><button onClick={save} className="btn-primary px-5 py-2.5 rounded-lg text-sm font-semibold">Simpan</button></div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Pengguna;
