import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import io
import jieba

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

        # --- 運用 jieba 進行中文斷詞，解決長句子問題 ---
        words_list = jieba.cut(raw_text) 
        cut_text = " ".join(words_list) # 斷好的詞用空格連起來
        
        # 2. 運用 Hash 找出高頻率文字
        word_counts = {} # 建立一個 Hash Table
        for w in cut_text.split():
            if w not in set(STOPWORDS): # 排除 Stop words
                word_counts[w] = word_counts.get(w, 0) + 1 # 運用 Hash 存取

        # 繪製文字雲
        wc = WordCloud(
            font_path="C:/Windows/Fonts/msjh.ttc", # 解決方框問題
            background_color="white",
            width=800,
            height=400,
            max_words=100,
            prefer_horizontal=0.6, # 設定橫直比例[cite: 1]
            colormap='Reds_r'
        ).generate_from_frequencies(word_counts) # 從算好的 Hash 頻率產生圖片

        # 轉換為 TK 顯示格式
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



