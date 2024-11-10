# Benutzerhandbuch für WebWizz

## Einleitung
WebWizz ist ein Webservice, der zur Erstellung und Bearbeitung von Webseiten mithilfe künstlicher Intelligenz entwickelt wurde. Der Service bietet Tools zur Generierung, Konstruktion und Bearbeitung von HTML-Code sowie zur Verwaltung von Dateien und zur Konfiguration von Einstellungen. WebWizz ist Open Source auf GitHub (Lizenz: GNU-GPL 3.0).

# Erste Schritte

## Hauptfunktionen

### Navigation durch Seiten
In der Seitenleiste können Sie eine der folgenden Seiten auswählen:
- **About us ℹ️**: Informationen über das Projekt.
- **Account 👤**: Verwalten Ihres Kontos und Ihrer Dateien.
- **Settings ⚙️**: Konfigurieren von Parametern und Tokens.
- **Generate ✨**: Generieren von Webseiten mit Hilfe von KI.
- **Build 🛠️**: Konstruieren von Webseiten.
- **Edit 👨‍💻**: Bearbeiten von HTML-Code.

### Account-Seite 👤
Auf dieser Seite können Sie:
- **Ein neues Konto erstellen** oder **sich in ein bestehendes einloggen**.
- **Dateien hochladen** oder **manuell hinzufügen**.
- **Gespeicherte Dateien anzeigen und verwalten**.

### Einstellungsseite ⚙️
Hier können Sie:
- **Ihre Tokens für HuggingFace und Pixabay konfigurieren**. (Für eine bessere Leistung)

### Generate-Seite ✨
Auf dieser Seite können Sie:
- **Ein Thema und eine Beschreibung eingeben**, um eine Webseite zu generieren.
- **HTML-Code mithilfe von KI-Algorithmen generieren**.
- **Den generierten Code und die Seite selbst in der Vorschau anzeigen und herunterladen**.
- **Den Code in Ihrem Konto speichern**.

### Build-Seite 🛠️
Auf dieser Seite können Sie:
- **Elemente auf der Webseite hinzufügen, bearbeiten und löschen**.
    - Text mit verschiedenen Anpassungsoptionen hinzufügen. (Farbe, Hintergrund, Rahmen, etc.)
    - Bilder mit verschiedenen Anpassungsoptionen hinzufügen. (Größe, Rahmen, etc.)
    - Gruppen von Elementen erstellen.
    - Bestehende Elemente bearbeiten oder löschen.
- **Den fertigen HTML-Code speichern und herunterladen**.

### Edit-Seite 👨‍💻
Hier können Sie:
- **Eine bestehende HTML-Datei hochladen** oder **eine leere Datei erstellen**.
- **Den Code mit dem integrierten Editor bearbeiten**. (Der Editor kann vom Benutzer mithilfe des integrierten Menüs angepasst werden. Er autovervollständigt den Benutzercode und formatiert Klammern.)
- **Den KI-Assistenten verwenden**, um den Benutzercode zu generieren und zu bearbeiten, mit der Möglichkeit, alle vorgenommenen Änderungen zu sehen.
- **Die Seite durch Klicken auf die Schaltfläche "Code ausführen" in der Vorschau anzeigen**.
- **Den Quellcode der Seite speichern und herunterladen**.

# Installation und Ausführung (Lokale Erstellung)

1. **Repository klonen**:
   ```bash
   git clone https://github.com/Wafflelover404/WebWizz.git
   cd WebWizz
   ```

2. **Abhängigkeiten installieren**:
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Anwendung ausführen**:
   ```bash
   python3 -m streamlit run streamlit_app.py
   ```

### Tokens konfigurieren
Für volle Funktionalität benötigt WebWizz Tokens von HuggingFace und Pixabay.

1. **HuggingFace Token**:
   - Gehen Sie zur [HuggingFace Token-Einstellungsseite](https://huggingface.co/settings/tokens).
   - Registrieren Sie sich und erhalten Sie Ihren API-Schlüssel.

2. **Pixabay Token**:
   - Gehen Sie zur [Pixabay API-Dokumentationsseite](https://pixabay.com/api/docs/).
   - Registrieren Sie sich und erhalten Sie Ihren API-Schlüssel.
