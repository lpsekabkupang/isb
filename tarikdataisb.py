import streamlit as st
import pandas as pd
import cloudscraper
import io

# Daftar URL API Anda
api_urls = {
    "SIRUP": {
        "SIRUP-Program": "https://isb.lkpp.go.id/isb-2/api/6b2244da-3360-4d51-9d3a-ea2cf92a8cd8/csv/4607/RUP-ProgramMaster/tipe/4:12/parameter/2024:D322",
        "SIRUP-Kegiatan": "https://isb.lkpp.go.id/isb-2/api/b0fff987-5e39-4360-9012-beb80d9068e7/csv/4596/RUP-KegiatanMaster/tipe/4:12/parameter/2024:D322",
        "SIRUP-SubKegiatan": "https://isb.lkpp.go.id/isb-2/api/f56679d2-f3ad-4176-90a5-c2f695a39818/csv/4588/RUP-SubKegiatanMaster/tipe/4:12/parameter/2024:D322",
        "SIRUP_Penyedia": "https://isb.lkpp.go.id/isb-2/api/c3f9a95c-1892-4e32-b679-ed81c17d1d1f/csv/4605/RUP-PaketPenyedia-Terumumkan/tipe/4:12/parameter/2024:D322",
        "sirup_Swakelola": "https://isb.lkpp.go.id/isb-2/api/6757450f-37a8-4034-aeec-9b7018c32090/csv/4606/RUP-PaketSwakelola-Terumumkan/tipe/4:12/parameter/2024:D322"
    },
    "NonTender": {
        "NonTender_01_Pengumuman": "https://isb.lkpp.go.id/isb-2/api/a4d09935-86dd-4943-b02f-b28fc00282db/csv/4598/SPSE-NonTenderPengumuman/tipe/4:4/parameter/2024:551",
        "NonTender_02_Jadwal": "https://isb.lkpp.go.id/isb-2/api/024158c5-192e-44fa-90de-3f0ccb1d3226/csv/4623/SPSE-JadwalTahapanNonTender/tipe/4:4/parameter/2024:551",
        "NonTender_03_SPMKSPP": "https://isb.lkpp.go.id/isb-2/api/fb3220e5-f42f-4260-834c-9566c404ae95/csv/6892/SPSE-NonTenderEkontrak-SPMKSPP/tipe/4:4/parameter/2024:551",
        "NonTender_04_BAPBAST": "https://isb.lkpp.go.id/isb-2/api/e961bb7c-1c4d-4131-9c05-91d3b4cb0c2a/csv/6784/SPSE-NonTenderEkontrak-BAPBAST/tipe/4:4/parameter/2024:551",
        "NonTender_06_SPPBJ": "https://isb.lkpp.go.id/isb-2/api/ff0727ea-7000-48b1-8284-21814a036549/csv/6676/SPSE-NonTenderEkontrak-SPPBJ/tipe/4:4/parameter/2024:551",
        "NonTender_07_Kontrak": "https://isb.lkpp.go.id/isb-2/api/1d6812ef-dd52-4eb2-ac73-28fccad04e0d/csv/6568/SPSE-NonTenderEkontrak-Kontrak/tipe/4:4/parameter/2024:551",
        "NonTender_05_Selesai": "https://isb.lkpp.go.id/isb-2/api/b0e52676-cd76-429b-95fc-4132b988e018/csv/4601/SPSE-NonTenderSelesai/tipe/4:4/parameter/2024:551",
        "NonTender_08_Penilaian_Kinerja": "https://isb.lkpp.go.id/isb-2/api/36439997-5bb8-4df6-8482-4301c66285a7/csv/7697/SiKAP-PenilaianKinerjaPenyedia-NonTender/tipe/4:12/parameter/2024:D322"
    },
    "E-Catalogue": {
        "E-Catalogue_Products": "https://isb.lkpp.go.id/isb-2/api/9bb71bb7-391e-43a0-a030-ddccfb517567/csv/4592/Ecat-PaketEPurchasing/tipe/4:12/parameter/2024:D322"
    },
    "Tender": {  # Added Tender section
        "1_Pengumuman": "https://isb.lkpp.go.id/isb-2/api/b8de0ff2-ec8d-4a00-a3fc-06bf0b829e1e/csv/4602/SPSE-TenderPengumuman/tipe/4:4/parameter/2024:551",
        "2_Peserta_Tender": "https://isb.lkpp.go.id/isb-2/api/b8de0ff2-ec8d-4a00-a3fc-06bf0b829e1e/csv/4602/SPSE-TenderPengumuman/tipe/4:4/parameter/2024:551",
        "3_Tender_SMPKSPP": "https://isb.lkpp.go.id/isb-2/api/dec8df0d-e112-43f7-adab-9ad430f56c96/csv/4626/SPSE-PesertaTender/tipe/4:4/parameter/2024:551",
        "4_Tender_BAPBAST": "https://isb.lkpp.go.id/isb-2/api/c8164131-91e7-41d2-9596-1fc7117e7929/csv/6058/SPSE-TenderEkontrak-SPMKSPP/tipe/4:4/parameter/2024:551",
        "5_Tender_SPPBJ": "https://isb.lkpp.go.id/isb-2/api/95e24f6e-5181-481f-8db0-7a10d7dd031b/csv/5958/SPSE-TenderEkontrak-BAPBAST/tipe/4:4/parameter/2024:551",
        "6_Tender_EKontrak": "https://isb.lkpp.go.id/isb-2/api/63ed1e5a-43cd-4a61-831f-7824f689e986/csv/5858/SPSE-TenderEkontrak-SPPBJ/tipe/4:4/parameter/2024:551",
        "7_Tender_Selesai": "https://isb.lkpp.go.id/isb-2/api/027a5aee-56e6-407b-a2f5-d409575d0c8e/csv/5508/SPSE-TenderEkontrak-Kontrak/tipe/4:4/parameter/2024:551",
        "8_Tender_Selesai_Nilai": "https://isb.lkpp.go.id/isb-2/api/fa98c028-308c-4060-8acb-9ef85972c72f/csv/4599/SPSE-TenderSelesai/tipe/4:4/parameter/2024:551"
    }
}

# Fungsi untuk menarik data dari API menggunakan cloudscraper
def fetch_data_from_api(url):
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)
    if response.status_code == 200:
        # Menggunakan io.StringIO untuk membaca data CSV dari string
        return pd.read_csv(io.StringIO(response.content.decode('utf-8')), on_bad_lines='skip')
    else:
        st.error(f"Error {response.status_code} fetching data from {url}")
        return None

# Membuat menu dengan Streamlit
st.title("Download Data API LKPP")
menu_options = st.sidebar.selectbox("Pilih API", list(api_urls.keys()) + ["Download Semua Data"])

if menu_options == "Download Semua Data":
    # Mendownload semua data dari semua API
    all_data = {}
    for main_key, sub_apis in api_urls.items():
        for sub_key, url in sub_apis.items():
            df = fetch_data_from_api(url)
            if df is not None:
                all_data[f"{main_key} - {sub_key}"] = df

    if all_data:
        # Membuat file Excel dengan setiap API di sheet yang berbeda
        with io.BytesIO() as output:
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                for sheet_name, df in all_data.items():
                    # Truncate sheet names to 31 characters
                    truncated_sheet_name = sheet_name[:31]
                    df.to_excel(writer, sheet_name=truncated_sheet_name, index=False)
            
            output.seek(0)
            st.download_button(label="Download Semua Data",
                               data=output,
                               file_name="Semua_Data_API.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
else:
    # Menampilkan data dari API yang dipilih
    sub_api_options = list(api_urls[menu_options].keys())
    sub_api_selection = st.sidebar.selectbox("Pilih Sub-API", sub_api_options)
    api_url = api_urls[menu_options][sub_api_selection]
    data = fetch_data_from_api(api_url)
    if data is not None:
        st.write(data)

