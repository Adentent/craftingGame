import tkinter as tk

root = tk.Tk()


def display_text_with_fonts(text: str):
    label = tk.Text(root)
    label.pack()

    lines = text.split("\n")
    for j in range(len(lines)):
        line = lines[j]
        label.insert("end", line + "\n")
        print(line)
        for i in range(len(line)):
            if "\u4e00" <= line[i] <= "\u9fff":  # 判断是否为中文字符
                label.tag_configure("chinese", font=("MiSans Normal", 12))
                label.tag_add("chinese", f"{j+1}.{i}", f"{j+1}.{i+1}")
            else:
                label.tag_configure("english", font=("Exo", 12))
                label.tag_add("english", f"{j+1}.{i}", f"{j+1}.{i+1}")


root.after(100, display_text_with_fonts, ("Hello, 你好\nHow are you?\n我很好"))

root.mainloop()
