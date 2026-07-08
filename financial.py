# import streamlit as st
# import pandas as pd
# import plotly.graph_objects as go
# from datetime import datetime, timedelta
# import plotly.express as px

# # ============================================================
# # KONFIGURASI HALAMAN
# # ============================================================
# st.set_page_config(
#     page_title="Finance Dashboard",
#     page_icon="📊",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ============================================================
# # FUNGSI UTILITY
# # ============================================================
# def format_rupiah(amount):
#     return f"Rp{amount:,.0f}".replace(",", ".")

# def get_df():
#     """Ambil data dari session_state dan konversi ke DataFrame"""
#     if 'transactions' not in st.session_state or not st.session_state.transactions:
#         return pd.DataFrame(columns=['id', 'desc', 'amount', 'type', 'date'])
    
#     df = pd.DataFrame(st.session_state.transactions)
    
#     # Pastikan kolom yang diperlukan ada
#     required_cols = ['id', 'desc', 'amount', 'type', 'date']
#     for col in required_cols:
#         if col not in df.columns:
#             df[col] = None
    
#     # Konversi tipe data
#     if 'amount' in df.columns:
#         df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0)
    
#     if 'date' in df.columns:
#         df['date'] = pd.to_datetime(df['date'])
    
#     return df

# # ============================================================
# # INISIALISASI DATA
# # ============================================================
# def init_data():
#     """Inisialisasi data awal jika belum ada"""
#     if 'transactions' not in st.session_state:
#         st.session_state.transactions = [
#             {"id": 1, "desc": "Gaji Pokok", "amount": 9800000, "type": "in", "date": datetime.now() - timedelta(days=5)},
#             {"id": 2, "desc": "Dana Hibah", "amount": 1422340, "type": "in", "date": datetime.now() - timedelta(days=10)},
#             {"id": 3, "desc": "Jual Workshop", "amount": 833333, "type": "in", "date": datetime.now() - timedelta(days=15)},
#             {"id": 4, "desc": "THR", "amount": 816667, "type": "in", "date": datetime.now() - timedelta(days=20)},
#             {"id": 5, "desc": "Gaji 13", "amount": 816667, "type": "in", "date": datetime.now() - timedelta(days=25)},
#             {"id": 6, "desc": "Jual Jasa", "amount": 1000000, "type": "in", "date": datetime.now() - timedelta(days=30)},
#             {"id": 7, "desc": "Gym", "amount": 565000, "type": "out", "date": datetime.now() - timedelta(days=3)},
#             {"id": 8, "desc": "Kost", "amount": 800000, "type": "out", "date": datetime.now() - timedelta(days=8)},
#             {"id": 9, "desc": "Makan", "amount": 1500000, "type": "out", "date": datetime.now() - timedelta(days=12)},
#             {"id": 10, "desc": "Entertain", "amount": 1500000, "type": "out", "date": datetime.now() - timedelta(days=18)},
#             {"id": 11, "desc": "Paket", "amount": 100000, "type": "out", "date": datetime.now() - timedelta(days=22)},
#             {"id": 12, "desc": "Transportasi", "amount": 750000, "type": "out", "date": datetime.now() - timedelta(days=28)},
#         ]
#         st.session_state.next_id = 13

# def calculate_summary(df):
#     """Hitung summary dari DataFrame"""
#     if df.empty:
#         return 0, 0, 0, 0
    
#     total_in = df[df['type'] == 'in']['amount'].sum() if 'type' in df.columns else 0
#     total_out = df[df['type'] == 'out']['amount'].sum() if 'type' in df.columns else 0
#     balance = total_in - total_out
    
#     # Monthly Save (30 hari terakhir)
#     cutoff = datetime.now() - timedelta(days=30)
#     if 'date' in df.columns and not df.empty:
#         recent = df[df['date'] >= cutoff]
#         recent_in = recent[recent['type'] == 'in']['amount'].sum() if 'type' in recent.columns else 0
#         recent_out = recent[recent['type'] == 'out']['amount'].sum() if 'type' in recent.columns else 0
#         monthly_save = recent_in - recent_out
#     else:
#         monthly_save = 0
    
#     return total_in, total_out, balance, monthly_save

# # ============================================================
# # SIDEBAR - FORM TAMBAH TRANSAKSI
# # ============================================================
# def sidebar_form():
#     st.sidebar.header("✏️ Tambah Transaksi")
    
#     with st.sidebar.form("add_transaction_form"):
#         desc = st.text_input("Deskripsi", placeholder="Contoh: Gaji, Makan, dll")
#         amount = st.number_input("Jumlah (Rp)", min_value=0, step=1000, value=50000)
#         trans_type = st.selectbox(
#             "Jenis", 
#             ["in", "out"], 
#             format_func=lambda x: "💰 Take In (Pemasukan)" if x == "in" else "📤 Take Out (Pengeluaran)"
#         )
        
#         submitted = st.form_submit_button("➕ Tambah", width='stretch')
        
#         if submitted:
#             if desc and amount > 0:
#                 # Pastikan transactions ada
#                 if 'transactions' not in st.session_state:
#                     st.session_state.transactions = []
#                 if 'next_id' not in st.session_state:
#                     st.session_state.next_id = 1
                
#                 st.session_state.transactions.append({
#                     "id": st.session_state.next_id,
#                     "desc": desc,
#                     "amount": amount,
#                     "type": trans_type,
#                     "date": datetime.now()
#                 })
#                 st.session_state.next_id += 1
#                 st.success("✅ Transaksi berhasil ditambahkan!")
#                 st.rerun()
#             else:
#                 st.error("⚠️ Isi deskripsi dan jumlah yang valid!")
    
#     st.sidebar.divider()
    
#     # Tombol reset
#     if st.sidebar.button("🔄 Reset Semua Data", width='stretch'):
#         if st.sidebar.button("⚠️ Konfirmasi Reset", width='stretch'):
#             st.session_state.transactions = []
#             st.session_state.next_id = 1
#             st.rerun()
    
#     # Export CSV
#     if st.sidebar.button("📥 Export CSV", width='stretch'):
#         df = get_df()
#         if not df.empty:
#             csv = df.to_csv(index=False)
#             st.sidebar.download_button(
#                 label="⬇️ Download CSV",
#                 data=csv,
#                 file_name=f"transactions_{datetime.now().strftime('%Y%m%d')}.csv",
#                 mime="text/csv"
#             )
#         else:
#             st.sidebar.warning("Belum ada data untuk diexport")
    
#     # Filter
#     st.sidebar.divider()
#     st.sidebar.header("🔍 Filter")
    
#     filter_type = st.sidebar.selectbox(
#         "Tampilkan",
#         ["Semua", "Take In", "Take Out"],
#         index=0
#     )
    
#     return filter_type

# # ============================================================
# # MAIN DASHBOARD
# # ============================================================
# def main():
#     # Inisialisasi data
#     init_data()
#     df = get_df()
    
#     # Header
#     col1, col2 = st.columns([3, 1])
#     with col1:
#         st.title("📊 Finance Dashboard")
#         st.caption("Take In / Take Out - Interactive Dashboard")
#     with col2:
#         st.metric("📅 Hari Ini", datetime.now().strftime("%d %B %Y"))
    
#     st.divider()
    
#     # Sidebar
#     filter_type = sidebar_form()
    
#     # Apply filter
#     if not df.empty:
#         if filter_type == "Take In":
#             df_filtered = df[df['type'] == 'in'] if 'type' in df.columns else df
#         elif filter_type == "Take Out":
#             df_filtered = df[df['type'] == 'out'] if 'type' in df.columns else df
#         else:
#             df_filtered = df
#     else:
#         df_filtered = df
    
#     # ============================================================
#     # CARDS SUMMARY
#     # ============================================================
#     total_in, total_out, balance, monthly_save = calculate_summary(df)
    
#     col1, col2, col3, col4 = st.columns(4)
    
#     with col1:
#         st.metric("💰 Total Take In", format_rupiah(total_in))
#     with col2:
#         st.metric("📤 Total Take Out", format_rupiah(total_out))
#     with col3:
#         st.metric("📊 Saldo", format_rupiah(balance))
#     with col4:
#         st.metric("📈 Monthly Save", format_rupiah(monthly_save))
    
#     st.divider()
    
#     # ============================================================
#     # ROW 2: CHART + PROYEKSI + HISTORI
#     # ============================================================
#     col_left, col_right = st.columns([3, 2])
    
#     with col_left:
#         # --- CHART ---
#         st.subheader("📈 Tren 30 Hari Terakhir")
        
#         if not df.empty and 'date' in df.columns:
#             # Siapkan data harian
#             cutoff = datetime.now() - timedelta(days=30)
#             df_recent = df[df['date'] >= cutoff].copy()
            
#             if not df_recent.empty and 'type' in df_recent.columns:
#                 df_recent['date_only'] = df_recent['date'].dt.date
                
#                 # Group by date
#                 daily = df_recent.groupby(['date_only', 'type'])['amount'].sum().unstack(fill_value=0)
                
#                 # Pastikan kolom 'in' dan 'out' ada
#                 if 'in' not in daily.columns:
#                     daily['in'] = 0
#                 if 'out' not in daily.columns:
#                     daily['out'] = 0
                
#                 daily = daily.reset_index()
#                 daily = daily.sort_values('date_only')
                
#                 # Plot dengan Plotly
#                 fig = go.Figure()
                
#                 fig.add_trace(go.Bar(
#                     x=daily['date_only'],
#                     y=daily['in'],
#                     name='Take In',
#                     marker_color='#1fb873',
#                     hovertemplate='%{y:,.0f}'
#                 ))
                
#                 fig.add_trace(go.Bar(
#                     x=daily['date_only'],
#                     y=daily['out'],
#                     name='Take Out',
#                     marker_color='#ef4444',
#                     hovertemplate='%{y:,.0f}'
#                 ))
                
#                 fig.update_layout(
#                     barmode='group',
#                     height=350,
#                     margin=dict(l=10, r=10, t=10, b=30),
#                     xaxis_title="Tanggal",
#                     yaxis_title="Jumlah (Rp)",
#                     yaxis_tickformat=',.0f',
#                     hovermode='x unified',
#                     legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5)
#                 )
                
#                 st.plotly_chart(fig, use_container_width=True)
#             else:
#                 st.info("Belum ada data 30 hari terakhir")
#         else:
#             st.info("Belum ada data untuk ditampilkan")
        
#         # --- PROYEKSI ---
#         st.subheader("🚀 Proyeksi Masa Depan")
        
#         # Hitung proyeksi dari monthly save
#         months_to_2027 = 18
#         end_2027 = monthly_save * months_to_2027
#         five_years = monthly_save * 60
        
#         col1, col2, col3 = st.columns(3)
#         col1.metric("Monthly Save", format_rupiah(monthly_save))
#         col2.metric("End of 2027", format_rupiah(end_2027))
#         col3.metric("Usia 35 (5 Tahun)", format_rupiah(five_years))
        
#         st.caption("⚡ Proyeksi berdasarkan rata-rata transaksi 30 hari terakhir")
    
#     with col_right:
#         # --- HISTORI ---
#         st.subheader(f"📜 Histori Transaksi ({len(df_filtered)})")
        
#         if not df_filtered.empty:
#             display_df = df_filtered.sort_values('date', ascending=False).copy()
#             display_df['type_label'] = display_df['type'].map({'in': '💰 Masuk', 'out': '📤 Keluar'})
#             display_df['amount_formatted'] = display_df['amount'].apply(format_rupiah)
#             display_df['date_formatted'] = display_df['date'].dt.strftime('%d %b %Y')
            
#             # Tampilkan dataframe
#             st.dataframe(
#                 display_df[['date_formatted', 'type_label', 'desc', 'amount_formatted']],
#                 column_config={
#                     "date_formatted": "Tanggal",
#                     "type_label": "Jenis",
#                     "desc": "Deskripsi",
#                     "amount_formatted": "Jumlah"
#                 },
#                 hide_index=True,
#                 use_container_width=True,
#                 height=300
#             )
            
#             # Hapus transaksi
#             with st.expander("🗑️ Hapus Transaksi", expanded=False):
#                 trans_options = display_df['id'].tolist()
#                 if trans_options:
#                     delete_id = st.selectbox(
#                         "Pilih transaksi untuk dihapus",
#                         options=trans_options,
#                         format_func=lambda x: f"{display_df[display_df['id']==x]['desc'].iloc[0]} - {format_rupiah(display_df[display_df['id']==x]['amount'].iloc[0])}"
#                     )
                    
#                     if st.button("❌ Hapus Transaksi Terpilih", width='stretch'):
#                         st.session_state.transactions = [t for t in st.session_state.transactions if t['id'] != delete_id]
#                         st.success("✅ Transaksi berhasil dihapus!")
#                         st.rerun()
#         else:
#             st.info("Belum ada transaksi. Tambahkan melalui sidebar!")
        
#         # --- Statistik tambahan ---
#         st.subheader("📊 Ringkasan Kategori")
        
#         if not df.empty and 'type' in df.columns:
#             # Top 5 pemasukan
#             top_in = df[df['type'] == 'in'].nlargest(5, 'amount')[['desc', 'amount']] if 'type' in df.columns else pd.DataFrame()
#             if not top_in.empty:
#                 st.caption("🏆 Top 5 Pemasukan")
#                 for _, row in top_in.iterrows():
#                     st.text(f"  {row['desc']}: {format_rupiah(row['amount'])}")
            
#             st.divider()
            
#             # Top 5 pengeluaran
#             top_out = df[df['type'] == 'out'].nlargest(5, 'amount')[['desc', 'amount']] if 'type' in df.columns else pd.DataFrame()
#             if not top_out.empty:
#                 st.caption("📉 Top 5 Pengeluaran")
#                 for _, row in top_out.iterrows():
#                     st.text(f"  {row['desc']}: {format_rupiah(row['amount'])}")
    
#     st.divider()
    
#     # Footer
#     st.caption(f"📊 Data tersimpan di session state • Terakhir diperbarui: {datetime.now().strftime('%H:%M:%S')}")

# # ============================================================
# # RUN APP
# # ============================================================
# if __name__ == "__main__":
#     main()