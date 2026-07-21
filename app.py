import json
import os
from threading import Thread, Event

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image

from runner_app import start_scanner


SETTINGS_FILE = "data/settings.json"
COIN_LIST_FILE = "data/coin_list.json"


class DetektifPribadi(App):

    def build(self):

        self.stop_event = Event()

        self.settings = self.load_settings()
        self.coin_list = self.load_coin_list()

        self.current_page = "home"

        self.root = Builder.load_file("kv/main.kv")

        return self.root

    # ==========================
    # SETTINGS
    # ==========================

    def load_settings(self):

        default = {
            "timeframe": "15",
            "scan_interval": 60,
            "telegram": True
        }

        if not os.path.exists(SETTINGS_FILE):
            return default

        try:

            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:

                data = json.load(f)

                if not data:
                    return default

                default.update(data)

                return default

        except Exception:

            return default

    # ==========================
    # COIN LIST
    # ==========================

    def load_coin_list(self):

        if not os.path.exists(COIN_LIST_FILE):
            return []

        try:

            with open(COIN_LIST_FILE, "r", encoding="utf-8") as f:

                data = json.load(f)

                if isinstance(data, list):
                    return data

                return []

        except Exception as e:

            print("❌ Gagal membaca coin_list :", e)

            return []

    def save_coin_list(self, coins):

        try:

            with open(COIN_LIST_FILE, "w", encoding="utf-8") as f:

                json.dump(
                    coins,
                    f,
                    indent=4,
                    ensure_ascii=False
                )

            self.coin_list = coins

            print("✅ Coin List berhasil disimpan")

        except Exception as e:

            print("❌ Gagal menyimpan Coin List :", e)

    # ==========================
    # COIN LOGO CACHE
    # ==========================

    def get_coin_logo(self, symbol):
        return None

        


    # ==========================
    # SIMPAN SETTINGS
    # ==========================

    def write_settings(self):

        try:

            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:

                json.dump(
                    self.settings,
                    f,
                    indent=4,
                    ensure_ascii=False
                )

            print("✅ Settings berhasil disimpan")

        except Exception as e:

            print("❌ Gagal menyimpan settings :", e)

    def save_settings(
        self,
        timeframe=None,
        scan_interval=None,
        telegram=None
    ):

        if timeframe is not None:
            self.settings["timeframe"] = str(timeframe)

        if scan_interval is not None:
            self.settings["scan_interval"] = int(scan_interval)

        if telegram is not None:
            self.settings["telegram"] = bool(telegram)

        self.write_settings()

    def open_settings(self):

        print("open setting")

        self.current_page = "settings"

    def close_settings(self):

        print("🏠 Kembali ke Home")

        self.current_page = "home"

    def show_settings_popup(self):

        layout = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=15
        )

        layout.add_widget(Label(text="TIMEFRAME"))

        tf = Spinner(
            text={
                "15": "15M",
                "60": "1H",
                "240": "4H",
                "1D": "1D"
            }.get(self.settings["timeframe"], "15M"),
            values=("15M", "1H", "4H", "1D"),
            size_hint=(1, None),
            height=45
        )

        layout.add_widget(tf)

        layout.add_widget(Label(text="SCAN INTERVAL (detik)"))

        interval = Spinner(
            text=str(self.settings["scan_interval"]),
            values=("30", "60", "120", "300"),
            size_hint=(1, None),
            height=45
        )

        layout.add_widget(interval)

        tombol = BoxLayout(
            size_hint=(1, None),
            height=50,
            spacing=10
        )

        popup = Popup(
            title="SETTINGS",
            content=layout,
            size_hint=(0.9, 0.6),
            auto_dismiss=False
        )

        def simpan(instance):

            tf_map = {
                "15M": "15",
                "1H": "60",
                "4H": "240",
                "1D": "1D"
            }

            self.save_settings(
                timeframe=tf_map[tf.text],
                scan_interval=int(interval.text)
            )

            self.root.ids.lbl_status.text = f"TimeFrame : {tf.text}"

            popup.dismiss()

        btn_save = Button(text="SIMPAN")
        btn_cancel = Button(text="BATAL")

        btn_save.bind(on_release=simpan)
        btn_cancel.bind(on_release=popup.dismiss)

        tombol.add_widget(btn_save)
        tombol.add_widget(btn_cancel)

        layout.add_widget(tombol)

        popup.open()

    def show_scan_result_popup(self):

        layout = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=10
        )

        scroll = ScrollView()

        daftar = GridLayout(
            cols=1,
            spacing=5,
            size_hint_y=None
        )

        daftar.bind(minimum_height=daftar.setter("height"))

        try:

            with open("data/scan_history.json", "r", encoding="utf-8") as f:
                data = json.load(f)

            scan_time = data.get("scan_time", "-")
            hasil = data.get("results", [])

            print("JUMLAH HASIL APK :", len(hasil))

        except:

            scan_time = "-"
            hasil = []

        daftar.add_widget(
            Label(
                text=f"📅 Scan : {scan_time}",
                size_hint_y=None,
                height=40
            )
    )

        daftar.add_widget(
            Label(
                text="",
                size_hint_y=None,
                height=10
            )
    )

        if not hasil:

            daftar.add_widget(
                Label(
                    text="Belum ada hasil scan.",
                    size_hint_y=None,
                    height=40
                )
            )

        else:

            for coin in hasil:

                baris = BoxLayout(
                    orientation="horizontal",
                    size_hint_y=None,
                    height=70,
                    spacing=10
                )

                logo_path = self.get_coin_logo(
                    coin["symbol"]
                )

                if logo_path:

                    gambar = Image(
                        source=logo_path,
                        size_hint=(None, None),
                        size=(50, 50)
                    )

                    baris.add_widget(gambar)

                teks = Label(
                    text=(
                        f"{coin['symbol']}\n"
                        f"Score : {coin['score']:.1f}/100"
                    ),
                    halign="left",
                    valign="middle"
                )

                baris.add_widget(teks)

                daftar.add_widget(baris)
                print("TAMPIL COIN :", coin["symbol"])
            

        scroll.add_widget(daftar)

        layout.add_widget(scroll)

        btn = Button(
            text="TUTUP",
            size_hint_y=None,
            height=50
        )

        popup = Popup(
            title="HASIL SCAN",
            content=layout,
            size_hint=(0.9, 0.8),
            auto_dismiss=False
        )

        btn.bind(on_release=popup.dismiss)

        layout.add_widget(btn)

        popup.open()


    # ==========================
    # COIN LIST
    # ==========================

    def show_coin_list_popup(self):

        layout = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=10
        )

        scroll = ScrollView(
            size_hint_y=1
        )

        daftar = GridLayout(
            cols=1,
            spacing=5,
            size_hint_y=None,
            size_hint_x=1
        )

        daftar.bind(minimum_height=daftar.setter("height"))

        checkbox_list = []

        for coin in self.coin_list:

            baris = BoxLayout(
                size_hint_y=None,
                height=42
            )

            cek = CheckBox(
                active=True,
                size_hint=(None, 1),
                width=45
            )

            lbl = Label(
                text=coin,
                halign="left",
                valign="middle"
            )

            lbl.bind(
                size=lambda instance, value:
                setattr(instance, "text_size", value)
            )

            checkbox_list.append((cek, coin))

            baris.add_widget(cek)
            baris.add_widget(lbl)

            daftar.add_widget(baris)

        scroll.add_widget(daftar)
        layout.add_widget(scroll)

        tombol = GridLayout(
            cols=2,
            spacing=8,
            size_hint_y=None,
            height=110
        )

        popup = Popup(
            title="COIN LIST",
            content=layout,
            size_hint=(0.92, 0.85),
            auto_dismiss=False
        )

        def tambah_coin(instance):

            input_popup = BoxLayout(
                orientation="vertical",
                spacing=10,
                padding=10
            )

            txt = TextInput(
                hint_text="Contoh : BTCUSDT"
            )

            input_popup.add_widget(txt)

            tombol2 = BoxLayout(
                size_hint_y=None,
                height=45,
                spacing=8
            )

            popup2 = Popup(
                title="Tambah Coin",
                content=input_popup,
                size_hint=(0.8, 0.35),
                auto_dismiss=False
            )

            def simpan_coin(x):

                coin = txt.text.strip().upper()

                if coin:

                    if coin not in self.coin_list:
                        self.coin_list.append(coin)
                        self.coin_list.sort()

                    self.save_coin_list(self.coin_list)

                popup2.dismiss()
                popup.dismiss()
                self.show_coin_list_popup()

            btn_ok = Button(text="SIMPAN")
            btn_batal = Button(text="BATAL")

            btn_ok.bind(on_release=simpan_coin)
            btn_batal.bind(on_release=popup2.dismiss)

            tombol2.add_widget(btn_ok)
            tombol2.add_widget(btn_batal)

            input_popup.add_widget(tombol2)

            popup2.open()

            

        def hapus_coin(instance):

            baru = []

            for cek, coin in checkbox_list:

                if not cek.active:
                    baru.append(coin)

            self.coin_list = baru

            self.save_coin_list(self.coin_list)

            popup.dismiss()
            self.show_coin_list_popup()

        btn_tambah = Button(text="Tambah Coin")
        btn_hapus = Button(text="Hapus Dipilih")
        btn_simpan = Button(text="Simpan")
        btn_tutup = Button(text="Tutup")

        btn_tambah.bind(on_release=tambah_coin)
        btn_hapus.bind(on_release=hapus_coin)

        btn_simpan.bind(
            on_release=lambda x: (
                self.save_coin_list(self.coin_list),
                popup.dismiss()
            )
        )

        btn_tutup.bind(on_release=popup.dismiss)

        tombol.add_widget(btn_tambah)
        tombol.add_widget(btn_hapus)
        tombol.add_widget(btn_simpan)
        tombol.add_widget(btn_tutup)

        layout.add_widget(tombol)

        popup.open()

            

    

    def is_home(self):
        return getattr(self, "current_page", "home") == "home"

    def is_settings(self):
        return getattr(self, "current_page", "home") == "settings"

    # ==========================
    # START
    # ==========================
    def start_scan(self):

        if hasattr(self, "scanner_thread") and self.scanner_thread.is_alive():
            print("Scanner sudah berjalan.")
            return

        self.stop_event.clear()

        self.root.ids.lbl_status.text = "STATUS : SCANNING"
        self.root.ids.lbl_status.color = (0, 1, 0, 1)

        self.scanner_thread = Thread(
            target=start_scanner,
            args=(
                self.settings["timeframe"],
                self.stop_event,
                self.settings["scan_interval"],
            ),
            daemon=True,
        )

        self.scanner_thread.start()

        print("START SCAN")

    # ==========================
    # STOP
    # ==========================
    def stop_scan(self):

        self.stop_event.set()

        self.root.ids.lbl_status.text = "STATUS : STOPPED"
        self.root.ids.lbl_status.color = (1, 0, 0, 1)

        print("STOP SCAN")


if __name__ == "__main__":
    DetektifPribadi().run()