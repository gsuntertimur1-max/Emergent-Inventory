import React, { createContext, useContext, useEffect, useState } from 'react';
import { PRODUCTS, SUPPLIERS, SURAT_JALAN, PURCHASE_ORDERS, USERS, buildTransactions } from '../mock';

const DataContext = createContext(null);
export const useData = () => useContext(DataContext);

const LS_AUTH = 'bulog_auth';
const LS_DATA = 'bulog_data';

export const DataProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    try { return JSON.parse(localStorage.getItem(LS_AUTH)) || null; } catch { return null; }
  });

  const emptyState = { products: [], suppliers: SUPPLIERS, suratJalan: [], purchaseOrders: [], users: USERS, transactions: [], loaded: false };

  const [state, setState] = useState(() => {
    try {
      const saved = JSON.parse(localStorage.getItem(LS_DATA));
      if (saved) return saved;
    } catch {}
    return emptyState;
  });

  useEffect(() => { localStorage.setItem(LS_DATA, JSON.stringify(state)); }, [state]);

  const login = (username, password) => {
    if (username === 'admin' && password === 'admin123') {
      const u = { name: 'Administrator Gudang', role: 'Administrator', username: 'admin' };
      setUser(u); localStorage.setItem(LS_AUTH, JSON.stringify(u)); return true;
    }
    return false;
  };
  const loginGoogle = () => {
    const u = { name: 'Pengguna Google', role: 'Pemantau', username: 'google_user' };
    setUser(u); localStorage.setItem(LS_AUTH, JSON.stringify(u));
  };
  const logout = () => { setUser(null); localStorage.removeItem(LS_AUTH); };

  const loadSample = () => {
    setState({
      products: JSON.parse(JSON.stringify(PRODUCTS)),
      suppliers: SUPPLIERS,
      suratJalan: JSON.parse(JSON.stringify(SURAT_JALAN)),
      purchaseOrders: JSON.parse(JSON.stringify(PURCHASE_ORDERS)),
      users: USERS,
      transactions: buildTransactions(),
      loaded: true,
    });
  };

  const addProduct = (p) => setState((s) => ({ ...s, products: [...s.products, { ...p, id: 'p' + Date.now(), damaged: p.damaged || 0 }] }));
  const updateProduct = (id, patch) => setState((s) => ({ ...s, products: s.products.map((p) => (p.id === id ? { ...p, ...patch } : p)) }));
  const deleteProduct = (id) => setState((s) => ({ ...s, products: s.products.filter((p) => p.id !== id) }));

  const addTransaction = ({ type, items, party, ref, polisi, kondisi, keterangan }) => {
    setState((s) => {
      const products = s.products.map((p) => ({ ...p }));
      const newTxns = [];
      items.forEach((it) => {
        const prod = products.find((p) => p.id === it.productId);
        if (!prod) return;
        const delta = type === 'MASUK' ? it.qty : -it.qty;
        if (kondisi === 'RUSAK') { prod.damaged = (prod.damaged || 0) + Math.abs(delta) * (type === 'MASUK' ? 1 : -1); }
        else { prod.stock = prod.stock + delta; }
        newTxns.push({ id: 't' + Date.now() + Math.random(), time: new Date().toISOString(), ref: ref || (type === 'MASUK' ? 'IN-' : 'OUT-') + Date.now().toString().slice(-4), antrian: type === 'KELUAR' ? 'A-' + String(s.suratJalan.length + 1).padStart(3, '0') : '', type, kondisi: kondisi || 'BAIK', product: prod.name, sku: prod.sku, change: delta, penerima: party || '-', polisi: polisi || '', operator: 'Administrator Gudang' });
      });
      let suratJalan = s.suratJalan;
      if (type === 'KELUAR') {
        const sjItems = items.map((it) => { const prod = products.find((p) => p.id === it.productId); return { name: prod?.name, qty: it.qty, unit: prod?.unit, berat: (prod?.weight || 0) * it.qty, sec: '' }; });
        const totalUnit = items.reduce((a, it) => a + it.qty, 0);
        const totalBerat = sjItems.reduce((a, i) => a + i.berat, 0);
        suratJalan = [{ id: 'sj' + Date.now(), no: 'SJ-2026' + String(s.suratJalan.length + 11).padStart(2, '0'), antrian: 'A-' + String(s.suratJalan.length + 1).padStart(3, '0'), time: new Date().toISOString(), penerima: party || '-', polisi: polisi || '', operator: 'Administrator Gudang', status: 'Menunggu', ref: ref || '', items: sjItems, berat: totalBerat, unit: totalUnit }, ...s.suratJalan];
      }
      return { ...s, products, transactions: [...newTxns, ...s.transactions], suratJalan };
    });
  };

  const updateSJStatus = (id, status) => setState((s) => ({ ...s, suratJalan: s.suratJalan.map((sj) => (sj.id === id ? { ...sj, status } : sj)) }));
  const addSupplier = (sup) => setState((s) => ({ ...s, suppliers: [...s.suppliers, { ...sup, id: 'sup' + Date.now() }] }));
  const addUser = (u) => setState((s) => ({ ...s, users: [...s.users, { ...u, id: 'u' + Date.now(), active: true }] }));
  const addPO = (po) => setState((s) => ({ ...s, purchaseOrders: [{ ...po, id: 'po' + Date.now() }, ...s.purchaseOrders] }));

  return (
    <DataContext.Provider value={{ user, login, loginGoogle, logout, ...state, loadSample, addProduct, updateProduct, deleteProduct, addTransaction, updateSJStatus, addSupplier, addUser, addPO }}>
      {children}
    </DataContext.Provider>
  );
};
