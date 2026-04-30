import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import io

class WordCloudApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hash-based 文字雲產生器")
        self.root.geometry("800x600")

        # 1. 圖形化介面設計 (GUI)
        self.label = tk.Label(root, text="請輸入文字或讀入檔案：", font=("Arial", 12))
        self.label.pack(pady=5)

        self.text_area = scrolledtext.ScrolledText(root, width=90, height=10)
        self.text_area.pack(pady=5)

        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack(pady=10)

        self.load_btn = tk.Button(self.btn_frame, text="讀入純文字檔", command=self.load_file)
        self.load_btn.pack(side=tk.LEFT, padx=5)

        self.gen_btn = tk.Button(self.btn_frame, text="產生文字雲", command=self.generate_wordcloud, bg="red", fg="white")
        self.gen_btn.pack(side=tk.LEFT, padx=5)

        self.save_btn = tk.Button(self.btn_frame, text="儲存圖檔", command=self.save_image)
        self.save_btn.pack(side=tk.LEFT, padx=5)

        self.img_label = tk.Label(root)
        self.img_label.pack(expand=True)

        self.current_wc_image = None

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, f.read())

    def generate_wordcloud(self):
        raw_text = self.text_area.get(1.0, tk.END).strip()
        if not raw_text:
            messagebox.showwarning("警告", "請先輸入文字")
            return

        # 2. 運用 Hash 找出高頻率文字
        words = raw_text.lower().split()
        word_counts = {} # 這是一個 Hash Table [cite: 329]
        
        # 排除 Stop Words
        custom_stopwords = set(STOPWORDS)
        
        for w in words:
            clean_w = ''.join(e for e in w if e.isalnum())
            if clean_w and clean_w not in custom_stopwords:
                # 運用 Hash 存取與更新 [cite: 330, 331]
                word_counts[clean_w] = word_counts.get(clean_w, 0) + 1

        # 3. 繪製文字雲 (橫直交錯設計)
        wc = WordCloud(
            background_color="white",
            width=800,
            height=400,
            max_words=100,
            prefer_horizontal=0.6, # 設定橫直比例 (0.6 代表 60% 橫，40% 直)
            colormap='Reds_r' # 參考圖片範例一的色系
        ).generate_from_frequencies(word_counts)

        # 轉換為 TK 可顯示的格式
        img = wc.to_image()
        self.current_wc_image = img
        tk_img = ImageTk.PhotoImage(img)
        self.img_label.config(image=tk_img)
        self.img_label.image = tk_img

    def save_image(self):
        if self.current_wc_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png")
            if file_path:
                self.current_wc_image.save(file_path)
                messagebox.showinfo("成功", "圖檔已儲存")
        else:
            messagebox.showwarning("警告", "請先產生文字雲")

if __name__ == "__main__":
    root = tk.Tk()
    app = WordCloudApp(root)
    root.mainloop()
