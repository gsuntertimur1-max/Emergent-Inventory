// Mock data for Bulog Gudang Sunter Timur I & II - Warehouse Stock Management
// NOTE: All data here is MOCKED for the frontend-only clone.

export const CATEGORIES = [
  { name: 'F&B / Bahan Makanan', color: '#f59e0b' },
  { name: 'Hardware & Perkakas', color: '#f97316' },
  { name: 'Peralatan Kantor', color: '#3b82f6' },
  { name: 'Pakaian & Tekstil', color: '#a855f7' },
  { name: 'Elektronik & Gadget', color: '#22d3ee' },
];

export const catColor = (name) => (CATEGORIES.find((c) => c.name === name)?.color || '#64748b');

export const SUPPLIERS = [
  { id: 'sup-1', name: 'PT Agro Indo Sejahtera', pic: 'Budi Santoso', phone: '021-5567-8890', email: 'sales@agroindo.co.id', address: 'Kawasan Industri Pulogadung, Jakarta Timur', category: 'F&B / Bahan Makanan' },
  { id: 'sup-2', name: 'PT Prima Perkasa Mandiri', pic: 'Andi Wijaya', phone: '021-8834-1200', email: 'order@primaperkasa.com', address: 'Jl. Raya Bekasi KM 21, Bekasi', category: 'Hardware & Perkakas' },
  { id: 'sup-3', name: 'CV Sumber Makmur Logistik', pic: 'Siti Rahayu', phone: '021-4471-9922', email: 'cs@sumbermakmur.id', address: 'Jl. Daan Mogot No. 88, Jakarta Barat', category: 'Peralatan Kantor' },
  { id: 'sup-4', name: 'PT Mega Nusantara Distribusi', pic: 'Rudi Hartono', phone: '021-2905-3311', email: 'sales@meganusantara.co.id', address: 'Sunter Agung, Jakarta Utara', category: 'Elektronik & Gadget' },
];

export const PRODUCTS = [
  { id: 'p1', name: 'Beras Premium Pandan Wangi', sku: 'FNB-RCE-25K', category: 'F&B / Bahan Makanan', stock: 2440, damaged: 0, cost: 15500, exp: '', location: 'Rak C-01', supplier: 'PT Agro Indo Sejahtera', min: 500, unit: 'Pcs', weight: 25, secondary: 'Karung' },
  { id: 'p2', name: 'Bor Listrik Impact 13mm', sku: 'HRD-DRL-13', category: 'Hardware & Perkakas', stock: 67, damaged: 0, cost: 685000, exp: '', location: 'Rak E-01', supplier: 'PT Prima Perkasa Mandiri', min: 20, unit: 'Unit', weight: 3.2, secondary: 'Dus' },
  { id: 'p3', name: 'Filing Cabinet 4 Drawer', sku: 'OFF-CAB-4D', category: 'Peralatan Kantor', stock: 8, damaged: 0, cost: 1950000, exp: '', location: 'Zona Barat', supplier: 'CV Sumber Makmur Logistik', min: 5, unit: 'Unit', weight: 32, secondary: 'Pallet' },
  { id: 'p4', name: 'Gula Kristal Putih 1kg', sku: 'FNB-SGR-1K', category: 'F&B / Bahan Makanan', stock: 660, damaged: 0, cost: 14200, exp: '', location: 'Rak C-03', supplier: 'PT Agro Indo Sejahtera', min: 200, unit: 'Pcs', weight: 1, secondary: 'Dus' },
  { id: 'p5', name: 'Kain Katun Roll 50m', sku: 'APP-FAB-R50', category: 'Pakaian & Tekstil', stock: 16, damaged: 0, cost: 875000, exp: '', location: 'Rak D-02', supplier: 'CV Sumber Makmur Logistik', min: 20, unit: 'Roll', weight: 22, secondary: 'Bal' },
  { id: 'p6', name: 'Kaos Polos Cotton Combed 30s', sku: 'APP-TSH-30S', category: 'Pakaian & Tekstil', stock: 520, damaged: 0, cost: 42000, exp: '', location: 'Rak D-01', supplier: 'CV Sumber Makmur Logistik', min: 100, unit: 'Pcs', weight: 0.18, secondary: 'Bal' },
  { id: 'p7', name: 'Kertas HVS A4 80gr', sku: 'OFF-PPR-A480', category: 'Peralatan Kantor', stock: 625, damaged: 0, cost: 178000, exp: '', location: 'Rak B-01', supplier: 'CV Sumber Makmur Logistik', min: 150, unit: 'Box', weight: 12.5, secondary: 'Pallet' },
  { id: 'p8', name: 'Kunci Set Tool Kit 108pcs', sku: 'HRD-TLK-108', category: 'Hardware & Perkakas', stock: 50, damaged: 0, cost: 415000, exp: '', location: 'Rak E-02', supplier: 'PT Prima Perkasa Mandiri', min: 15, unit: 'Set', weight: 5.5, secondary: 'Dus' },
  { id: 'p9', name: 'Laptop ThinkPad T14 Gen 4', sku: 'ELEC-TP-001', category: 'Elektronik & Gadget', stock: 48, damaged: 0, cost: 14500000, exp: '', location: 'Rak A-01', supplier: 'PT Mega Nusantara Distribusi', min: 10, unit: 'Unit', weight: 1.5, secondary: 'Dus' },
  { id: 'p10', name: 'Minyak Goreng Kemasan 2L', sku: 'FNB-OIL-2L', category: 'F&B / Bahan Makanan', stock: 796, damaged: 0, cost: 34000, exp: '', location: 'Rak C-02', supplier: 'PT Agro Indo Sejahtera', min: 250, unit: 'Pcs', weight: 2, secondary: 'Dus' },
  { id: 'p11', name: 'Monitor LED 24" IPS', sku: 'ELEC-MON-024', category: 'Elektronik & Gadget', stock: 92, damaged: 0, cost: 1850000, exp: '', location: 'Rak A-02', supplier: 'PT Mega Nusantara Distribusi', min: 20, unit: 'Unit', weight: 4.5, secondary: 'Dus' },
  { id: 'p12', name: 'Mouse Wireless Ergonomis', sku: 'ELEC-MSE-110', category: 'Elektronik & Gadget', stock: 350, damaged: 0, cost: 145000, exp: '', location: 'Rak A-03', supplier: 'PT Mega Nusantara Distribusi', min: 80, unit: 'Pcs', weight: 0.12, secondary: 'Dus' },
  { id: 'p13', name: 'Printer Laser Mono A4', sku: 'ELEC-PRN-A4', category: 'Elektronik & Gadget', stock: 12, damaged: 0, cost: 2450000, exp: '', location: 'Rak A-04', supplier: 'PT Mega Nusantara Distribusi', min: 15, unit: 'Unit', weight: 8, secondary: 'Dus' },
  { id: 'p14', name: 'Pulpen Gel Hitam 0.5mm', sku: 'OFF-PEN-G05', category: 'Peralatan Kantor', stock: 1040, damaged: 0, cost: 32000, exp: '', location: 'Rak B-02', supplier: 'CV Sumber Makmur Logistik', min: 300, unit: 'Pack', weight: 0.24, secondary: 'Dus' },
  { id: 'p15', name: 'Semen Portland 40kg', sku: 'HRD-CMT-40', category: 'Hardware & Perkakas', stock: 920, damaged: 0, cost: 62000, exp: '', location: 'Zona Timur', supplier: 'PT Prima Perkasa Mandiri', min: 300, unit: 'Pcs', weight: 40, secondary: 'Pallet' },
];

const now = new Date('2026-08-28T11:10:00');
const dOffset = (days, h = 11, m = 10) => {
  const d = new Date(now); d.setDate(d.getDate() - days); d.setHours(h, m, 0, 0); return d.toISOString();
};

// Delivery notes (Surat Jalan)
export const SURAT_JALAN = [
  { id: 'sj7', no: 'SJ-202608-007', antrian: 'A-001', time: dOffset(0), penerima: 'Rumah Makan Selera', polisi: '', operator: 'Operator Gudang Siang', status: 'Selesai', ref: 'REF-030',
    items: [ { name: 'Beras Premium Pandan Wangi', qty: 60, unit: 'Pcs', berat: 1500, sec: '60 Karung' }, { name: 'Minyak Goreng Kemasan 2L', qty: 24, unit: 'Pcs', berat: 48, sec: '4 Dus' } ], berat: 1548, unit: 84 },
  { id: 'sj8', no: 'SJ-202608-008', antrian: 'A-002', time: dOffset(0), penerima: 'Toko Bangunan Jaya Abadi', polisi: '', operator: 'Operator Gudang Siang', status: 'Sedang Dimuat', ref: 'REF-031',
    items: [ { name: 'Semen Portland 40kg', qty: 120, unit: 'Pcs', berat: 4800, sec: '4 Pallet' }, { name: 'Kunci Set Tool Kit 108pcs', qty: 3, unit: 'Set', berat: 16.5, sec: '0.5 Dus' }, { name: 'Bor Listrik Impact 13mm', qty: 2, unit: 'Unit', berat: 6.4, sec: '0.25 Dus' } ], berat: 4822.9, unit: 125 },
  { id: 'sj9', no: 'SJ-202608-009', antrian: 'A-003', time: dOffset(0), penerima: 'Bengkel Motor Rapi', polisi: '', operator: 'Operator Gudang Siang', status: 'Menunggu', ref: 'REF-032',
    items: [ { name: 'Kunci Set Tool Kit 108pcs', qty: 4, unit: 'Set', berat: 22, sec: '0.67 Dus' }, { name: 'Bor Listrik Impact 13mm', qty: 1, unit: 'Unit', berat: 3.2, sec: '0.12 Dus' } ], berat: 25.2, unit: 5 },
  { id: 'sj10', no: 'SJ-202608-010', antrian: 'A-004', time: dOffset(0), penerima: 'Kantor Notaris Amanah', polisi: '', operator: 'Operator Gudang Siang', status: 'Menunggu', ref: 'REF-033',
    items: [ { name: 'Pulpen Gel Hitam 0.5mm', qty: 40, unit: 'Pack', berat: 9.6, sec: '1.67 Dus' }, { name: 'Kertas HVS A4 80gr', qty: 15, unit: 'Box', berat: 187.5, sec: '0.38 Pallet' } ], berat: 197.1, unit: 55 },
  { id: 'sj6', no: 'SJ-202608-006', antrian: 'A-001', time: dOffset(2), penerima: 'PT Karya Griya', polisi: '', operator: 'Operator Gudang Siang', status: 'Selesai', ref: 'REF-027',
    items: [ { name: 'Semen Portland 40kg', qty: 80, unit: 'Pcs', berat: 3200, sec: '2.67 Pallet' }, { name: 'Bor Listrik Impact 13mm', qty: 4, unit: 'Unit', berat: 12.8, sec: '0.5 Dus' } ], berat: 3212.8, unit: 84 },
  { id: 'sj5', no: 'SJ-202608-005', antrian: 'A-001', time: dOffset(4), penerima: 'Distro Anak Muda', polisi: '', operator: 'Operator Gudang Siang', status: 'Selesai', ref: 'REF-025',
    items: [ { name: 'Kaos Polos Cotton Combed 30s', qty: 40, unit: 'Pcs', berat: 7.2, sec: '0.67 Bal' }, { name: 'Kain Katun Roll 50m', qty: 2, unit: 'Roll', berat: 44, sec: '0.5 Bal' } ], berat: 51.2, unit: 42 },
  { id: 'sj4', no: 'SJ-202608-004', antrian: 'A-001', time: dOffset(6), penerima: 'Warung Sembako Berkah', polisi: '', operator: 'Operator Gudang Siang', status: 'Selesai', ref: 'REF-022',
    items: [ { name: 'Beras Premium Pandan Wangi', qty: 250, unit: 'Pcs', berat: 6250, sec: '250 Karung' }, { name: 'Minyak Goreng Kemasan 2L', qty: 90, unit: 'Pcs', berat: 180, sec: '15 Dus' }, { name: 'Gula Kristal Putih 1kg', qty: 120, unit: 'Pcs', berat: 120, sec: '5 Dus' } ], berat: 6550, unit: 460 },
  { id: 'sj3', no: 'SJ-202608-003', antrian: 'A-001', time: dOffset(9), penerima: 'Sekolah Tunas Bangsa', polisi: '', operator: 'Operator Gudang Siang', status: 'Selesai', ref: 'REF-018',
    items: [ { name: 'Kertas HVS A4 80gr', qty: 80, unit: 'Box', berat: 1000, sec: '2 Pallet' }, { name: 'Pulpen Gel Hitam 0.5mm', qty: 60, unit: 'Pack', berat: 14.4, sec: '2.5 Dus' } ], berat: 1014.4, unit: 140 },
  { id: 'sj2', no: 'SJ-202608-002', antrian: 'A-001', time: dOffset(12), penerima: 'CV Digital Kreatif', polisi: '', operator: 'Operator Gudang Siang', status: 'Selesai', ref: 'REF-014',
    items: [ { name: 'Monitor LED 24" IPS', qty: 8, unit: 'Unit', berat: 36, sec: '8 Dus' }, { name: 'Mouse Wireless Ergonomis', qty: 20, unit: 'Pcs', berat: 2.4, sec: '2 Dus' } ], berat: 38.4, unit: 28 },
  { id: 'sj1', no: 'SJ-202608-001', antrian: 'A-001', time: dOffset(15), penerima: 'Startup Nusantara', polisi: '', operator: 'Operator Gudang Siang', status: 'Selesai', ref: 'REF-010',
    items: [ { name: 'Laptop ThinkPad T14 Gen 4', qty: 5, unit: 'Unit', berat: 7.5, sec: '5 Dus' } ], berat: 7.5, unit: 5 },
];

export const PURCHASE_ORDERS = [
  { id: 'po1', no: 'PO-2026-011', supplier: 'PT Prima Perkasa Mandiri', date: dOffset(5), status: 'Diterima', items: [ { name: 'Kunci Set Tool Kit 108pcs', qty: 30, cost: 415000 } ], total: 12450000 },
  { id: 'po2', no: 'PO-2026-012', supplier: 'CV Sumber Makmur Logistik', date: dOffset(2), status: 'Dikirim', items: [ { name: 'Kain Katun Roll 50m', qty: 24, cost: 875000 } ], total: 21000000 },
  { id: 'po3', no: 'PO-2026-013', supplier: 'PT Mega Nusantara Distribusi', date: dOffset(1), status: 'Menunggu', items: [ { name: 'Printer Laser Mono A4', qty: 18, cost: 2450000 } ], total: 44100000 },
  { id: 'po4', no: 'PO-2026-014', supplier: 'PT Agro Indo Sejahtera', date: dOffset(0), status: 'Draft', items: [ { name: 'Gula Kristal Putih 1kg', qty: 500, cost: 14200 } ], total: 7100000 },
];

export const USERS = [
  { id: 'u1', name: 'Administrator Gudang', username: 'admin', role: 'Administrator', email: 'admin@bulog.co.id', active: true },
  { id: 'u2', name: 'Operator Gudang Siang', username: 'operator_siang', role: 'Operator', email: 'operator.siang@bulog.co.id', active: true },
  { id: 'u3', name: 'Operator Gudang Malam', username: 'operator_malam', role: 'Operator', email: 'operator.malam@bulog.co.id', active: true },
  { id: 'u4', name: 'Kepala Gudang', username: 'kepala', role: 'Supervisor', email: 'kepala@bulog.co.id', active: true },
  { id: 'u5', name: 'Auditor Internal', username: 'auditor', role: 'Pemantau', email: 'auditor@bulog.co.id', active: false },
];

// Build transaction history (audit trail) from surat jalan + some inbound
export const buildTransactions = () => {
  const txns = [];
  let seq = 30;
  const skuOf = (name) => PRODUCTS.find((p) => p.name === name)?.sku || '';
  SURAT_JALAN.forEach((sj) => {
    sj.items.forEach((it) => {
      txns.push({ id: `t-${sj.id}-${it.name}`, time: sj.time, ref: sj.ref, antrian: sj.antrian, type: 'KELUAR', kondisi: 'BAIK', product: it.name, sku: skuOf(it.name), change: -it.qty, penerima: sj.penerima, polisi: sj.polisi, operator: sj.operator });
    });
  });
  // Some inbound from PO
  const inbound = [
    { name: 'Kunci Set Tool Kit 108pcs', qty: 30, days: 5, ref: 'PO-2026-011', party: 'PT Prima Perkasa Mandiri' },
    { name: 'Beras Premium Pandan Wangi', qty: 500, days: 6, ref: 'PO-2026-009', party: 'PT Agro Indo Sejahtera' },
    { name: 'Laptop ThinkPad T14 Gen 4', qty: 10, days: 8, ref: 'PO-2026-008', party: 'PT Mega Nusantara Distribusi' },
    { name: 'Semen Portland 40kg', qty: 300, days: 10, ref: 'PO-2026-007', party: 'PT Prima Perkasa Mandiri' },
    { name: 'Minyak Goreng Kemasan 2L', qty: 200, days: 12, ref: 'PO-2026-006', party: 'PT Agro Indo Sejahtera' },
  ];
  inbound.forEach((ib, i) => {
    txns.push({ id: `tin-${i}`, time: dOffset(ib.days), ref: ib.ref, antrian: '', type: 'MASUK', kondisi: 'BAIK', product: ib.name, sku: skuOf(ib.name), change: ib.qty, penerima: ib.party, polisi: '', operator: 'Administrator Gudang' });
  });
  return txns.sort((a, b) => new Date(b.time) - new Date(a.time));
};

export const formatRp = (n) => 'Rp ' + Math.round(n || 0).toLocaleString('id-ID');
export const formatRpShort = (n) => {
  if (n >= 1e12) return 'Rp ' + (n / 1e12).toFixed(1) + ' T';
  if (n >= 1e9) return 'Rp ' + (n / 1e9).toFixed(1) + ' M';
  if (n >= 1e6) return 'Rp ' + (n / 1e6).toFixed(1) + ' Jt';
  return 'Rp ' + Math.round(n || 0).toLocaleString('id-ID');
};
export const formatNum = (n) => (n || 0).toLocaleString('id-ID');
export const formatDate = (iso) => {
  const d = new Date(iso);
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'];
  return `${d.getDate()} ${months[d.getMonth()]} ${d.getFullYear()}, ${String(d.getHours()).padStart(2, '0')}.${String(d.getMinutes()).padStart(2, '0')}`;
};
