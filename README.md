# Pragati AI 🏪🤖📊

> An intelligent, localized AI operational dashboard designed for local Kirana merchants and small business owners to automate receipt text extraction, organize transaction logs, and dispatch structured email receipts seamlessly.

---

## 📖 Table of Contents

* [About The Project](#-about-the-project)
* [Core Features & Capabilities](#-core-features--capabilities)
* [Complete Tech Stack](#-complete-tech-stack)
* [Project Architecture & Directory Structure](#-project-architecture--directory-structure)
* [Getting Started & Installation](#-getting-started--installation)
* [Configuration & API Setup](#-configuration--api-setup)
* [Usage Guide](#-usage-guide)
* [Future Roadmap](#-future-roadmap)
* [Contributing](#-contributing)
* [License](#-license)

---

## 🎯 About The Project

Small local retail merchants ("Kirana stores") process dozens of paper receipts, manual invoices, and daily transactions every day. Manual entry leads to human error, missed records, and lost administrative hours.

***Pragati AI** bridges this gap by combining optical character recognition (OCR), intelligent document cropping, local language processing, and automated communication tools into a simple, non-technical dashboard. Merchants can upload physical receipt images, instantly extract structured line items, organize sales data, and send digital summary receipts directly to customers via email.

---

## 🌟 Core Features & Capabilities

* **📄 Optical Character Recognition (OCR)**: 
  * Parses printed physical receipts and invoices into structured digital text using EasyOCR.
* **✂️ Intelligent Image Cropping & Preprocessing**: 
  * Automatically isolates receipts, cleans visual noise, and detects key text blocks (item names, prices, total amounts, timestamps).
* **✉️ Automated Email Receipt Dispatch**: 
  * Generates clean, formatted email receipts and delivers them directly to customer inboxes.
* **📊 Merchant Operations Dashboard**: 
  * Built with Streamlit for a fast, responsive, and mobile-friendly interface suited for fast-paced retail environments.
* **🔒 Privacy-Focused Local Processing**: 
  * Processes image data locally to ensure business records and customer transactions remain secure.

---

## 🛠️ Complete Tech Stack

### **Frontend & UI Layer**
* **Streamlit**: Interactive Python web framework for rendering real-time dashboards, image uploaders, and data previews.

### **Computer Vision & OCR**
* **EasyOCR**: Deep learning OCR engine for multi-language text extraction from noisy receipt images.
* **OpenCV (`cv2`) & Pillow (PIL)**: Image manipulation, thresholding, bounding box calculations, and regional cropping.

### **Backend & Automation**
* **Python 3.9+**: Core application logic, text cleaning heuristics, and data structure parsing.
* **SMTP / Email Services**: Standard library email dispatching for automated customer notifications.

---

## 🏗️ Project Architecture & Directory Structure

```text
Pragati-AI/
│
├── assets/                    # UI icons, sample receipt images, and screenshots
├── modules/                   # Internal Python helper modules
│   ├── ocr_engine.py          # EasyOCR text detection & parsing functions
│   ├── image_processor.py     # Image cropping, rotation, and cleaning utilities
│   └── email_service.py       # SMTP configuration and dispatch handler
│
├── app.py                     # Main Streamlit dashboard application entry point
├── requirements.txt           # Python dependencies and version specs
