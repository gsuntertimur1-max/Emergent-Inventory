import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Eye, EyeOff, LogIn } from 'lucide-react';
import { useData } from '../context/DataContext';
import { toast } from 'sonner';

const Login = () => {
  const { login, loginGoogle } = useData();
  const navigate = useNavigate();
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('admin123');
  const [show, setShow] = useState(false);

  const submit = (e) => {
    e.preventDefault();
    if (login(username, password)) { toast.success('Berhasil masuk'); navigate('/'); }
    else toast.error('Username atau password salah');
  };

  return (
    <div className="app-bg flex flex-col items-center justify-center min-h-screen px-4">
      <div className="flex items-center gap-3 mb-8">
        <div className="w-14 h-14 rounded-2xl bg-white flex items-center justify-center font-display font-bold text-[#1e40af] shadow-xl">bulog</div>
        <div>
          <div className="font-display font-bold text-xl tracking-tight">Bulog Gudang Sunter Timur I &amp; II</div>
          <div className="label-mono">Sistem Manajemen Stok</div>
        </div>
      </div>

      <div className="card-surface w-full max-w-md p-8 fade-up">
        <h1 className="font-display text-2xl font-bold mb-1">Masuk ke Akun Anda</h1>
        <p className="text-sm text-[#8b93a1] mb-6">Gunakan akun yang diberikan administrator gudang.</p>

        <form onSubmit={submit} className="space-y-4">
          <div>
            <label className="text-sm font-medium mb-1.5 block">Username</label>
            <input value={username} onChange={(e) => setUsername(e.target.value)} className="w-full bg-[#0b0f17] border border-[#242f3d] rounded-lg px-3.5 py-2.5 text-sm outline-none focus:border-[#2563eb] focus:ring-2 focus:ring-[#2563eb]/30 transition" placeholder="admin" />
          </div>
          <div>
            <label className="text-sm font-medium mb-1.5 block">Password</label>
            <div className="relative">
              <input type={show ? 'text' : 'password'} value={password} onChange={(e) => setPassword(e.target.value)} className="w-full bg-[#0b0f17] border border-[#242f3d] rounded-lg px-3.5 py-2.5 pr-11 text-sm outline-none focus:border-[#2563eb] focus:ring-2 focus:ring-[#2563eb]/30 transition" />
              <button type="button" onClick={() => setShow(!show)} className="absolute right-3 top-1/2 -translate-y-1/2 text-[#8b93a1] hover:text-white">{show ? <EyeOff size={17} /> : <Eye size={17} />}</button>
            </div>
            <p className="text-xs text-[#6b7688] mt-1.5">Password peka huruf besar/kecil. Ketuk ikon mata untuk memeriksa ketikan Anda.</p>
          </div>
          <button type="submit" className="btn-primary w-full flex items-center justify-center gap-2 py-2.5 rounded-lg font-semibold text-sm"><LogIn size={16} /> Masuk</button>
        </form>

        <div className="flex items-center gap-3 my-5"><div className="flex-1 h-px bg-[#1e2733]" /><span className="label-mono text-[10px]">Atau</span><div className="flex-1 h-px bg-[#1e2733]" /></div>

        <button onClick={() => { loginGoogle(); navigate('/'); }} className="w-full flex items-center justify-center gap-2.5 py-2.5 rounded-lg border border-[#242f3d] text-sm font-medium hover:bg-[#141a24] transition-colors">
          <svg width="17" height="17" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 01-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84A11 11 0 0012 23z"/><path fill="#FBBC05" d="M5.84 14.1a6.6 6.6 0 010-4.2V7.06H2.18a11 11 0 000 9.88l3.66-2.84z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84C6.71 7.31 9.14 5.38 12 5.38z"/></svg>
          Masuk dengan Google
        </button>

        <div className="mt-6 p-3 rounded-lg bg-[#0b0f17] border border-[#1a222e] text-xs text-[#8b93a1] leading-relaxed">
          Akun administrator bawaan: <span className="font-mono text-[#c7d0dc]">admin</span> / <span className="font-mono text-[#c7d0dc]">admin123</span> — segera ganti password di halaman Pengguna. Akun Google baru selain pemilik aplikasi masuk sebagai <span className="text-[#c7d0dc]">Pemantau</span> sampai admin menaikkan perannya.
        </div>
      </div>
    </div>
  );
};

export default Login;
