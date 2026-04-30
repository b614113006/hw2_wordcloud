import os
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

def generate_wordcloud_cli():
    print("=== Hash-based 文字雲產生器 (終端機版) ===")
    
    # 1. 讀取輸入
    choice = input("選擇輸入方式：(1) 直接輸入文字 (2) 讀取 .txt 檔案路徑: ")
    
    raw_text = ""
    if choice == '1':
        print("請輸入文字（按 Enter 結束）：")
        raw_text = input("> ")
    elif choice == '2':
        file_path = input("請輸入檔案路徑 (例如: data.txt): ").strip()
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                raw_text = f.read()
        else:
            print("錯誤：找不到檔案！")
            return
    else:
        print("無效的選擇。")
        return

    if not raw_text.strip():
        print("警告：沒有輸入任何文字。")
        return

    # 2. 運用 Hash 找出高頻率文字
    words = raw_text.lower().split()
    word_counts = {}  # 這是你的 Hash Table
    
    custom_stopwords = set(STOPWORDS)
    
    for w in words:
        # 去除標點符號，只保留字母數字
        clean_w = ''.join(e for e in w if e.isalnum())
        if clean_w and clean_w not in custom_stopwords:
            # 運用 Hash 存取與更新
            word_counts[clean_w] = word_counts.get(clean_w, 0) + 1

    # 3. 顯示統計結果 (取代原本 GUI 的顯示)
    print("\n--- 文字頻率統計結果 (Hash Table) ---")
    # 按頻率排序顯示前 10 名
    sorted_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    for word, count in sorted_counts[:10]:
        print(f"[{word}]: {count} 次")
    print("------------------------------------\n")

    # 4. 產生文字雲圖檔
    wc = WordCloud(
        background_color="white",
        width=800,
        height=400,
        max_words=100,
        prefer_horizontal=0.6,
        colormap='Reds_r'
    ).generate_from_frequencies(word_counts)

    # 5. 儲存與預覽
    output_file = "wordcloud_output.png"
    wc.to_file(output_file)
    print(f"成功！文字雲圖檔已儲存為: {output_file}")
    
    # 如果環境支援彈出視窗（如 Windows/Mac 本機），可取消下行註解來預覽
    # plt.imshow(wc, interpolation='bilinear'); plt.axis("off"); plt.show()

if __name__ == "__main__":
    generate_wordcloud_cli()
