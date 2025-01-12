import tkinter as tk
from tkinter import ttk, messagebox, font
import pandas as pd
import random
from collections import defaultdict

class Medicine:
    def __init__(self, name, symptoms, instructions, effects, side_effects, ingredients, image_path):
        self.name = name
        self.symptoms = symptoms
        self.instructions = instructions
        self.effects = effects
        self.side_effects = side_effects
        self.ingredients = ingredients
        self.image_path = image_path

def load_medicine_db(filename):
    global medicine_db, all_symptoms
    medicine_db = []
    all_symptoms = set()
    df = pd.read_csv(filename)
    for _, row in df.iterrows():
        symptoms_list = row['symptoms'].split(';')
        medicine = Medicine(
            row['name'],
            symptoms_list,
            row['instructions'],
            row['effects'].split(';'),
            row['side_effects'].split(';'),
            row['ingredients'].split(';'),
            row['image_path']
        )
        medicine_db.append(medicine)
        all_symptoms.update(symptoms_list)
    status_label.config(text="데이터베이스 로드 성공")

def recommend_medicine_by_symptom(symptom):
    recommendations = [med for med in medicine_db if symptom in med.symptoms]
    
    if recommendations:
        selected_medicine = random.choice(recommendations)
        
        result_window = tk.Toplevel(root)
        result_window.title("추천 결과")
        result_window.geometry("1000x1000")

        canvas = tk.Canvas(result_window)
        scrollbar = ttk.Scrollbar(result_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        result_frame = ttk.Frame(scrollable_frame, padding="10", style="TFrame")
        result_frame.pack(fill="both", expand=True)
        
        result_title = ttk.Label(result_frame, text="추천 결과", font=title_font, style="TLabel")
        result_title.pack(pady=5)
        
        med_name = ttk.Label(result_frame, text=f"추천 약품: {selected_medicine.name}", font=label_font, foreground="red", style="TLabel")
        med_name.pack(anchor="center", pady=(5, 0))

        try:
            med_image = tk.PhotoImage(file=selected_medicine.image_path)
            med_image_label = tk.Label(result_frame, image=med_image)
            med_image_label.image = med_image  # 이미지 객체 저장
            med_image_label.pack(anchor="center", pady=5)
        except Exception as e:
            print(f"Error loading image: {e}")

        def show_details():
            details_window = tk.Toplevel(result_window)
            details_window.title(f"{selected_medicine.name} 정보")
            details_window.geometry("700x700")
            
            details_frame = ttk.Frame(details_window, padding="10", style="TFrame")
            details_frame.pack(fill="both", expand=True)
            
            med_instructions = ttk.Label(details_frame, text=f"복용 방법: {selected_medicine.instructions}", font=label_font, style="TLabel")
            med_instructions.pack(anchor="w")
            
            med_effects = ttk.Label(details_frame, text=f"효능: {', '.join(selected_medicine.effects)}", font=label_font, style="TLabel")
            med_effects.pack(anchor="w")
            
            med_side_effects = ttk.Label(details_frame, text=f"부작용: {', '.join(selected_medicine.side_effects)}", font=label_font, style="TLabel")
            med_side_effects.pack(anchor="w")
            
            med_ingredients = ttk.Label(details_frame, text=f"성분: {', '.join(selected_medicine.ingredients)}", font=label_font, style="TLabel")
            med_ingredients.pack(anchor="w")

        details_button = ttk.Button(result_frame, text="약 정보 확인하기", command=show_details, style='Green.TButton')
        details_button.pack(pady=10)
        
        def recommend_another():
            result_window.destroy()
            recommend_medicine_by_symptom(symptom)
        
        another_button = ttk.Button(result_frame, text="다시 추천 받기 🔄", command=recommend_another, style='Green.TButton')
        another_button.pack(pady=10)
        
    else:
        messagebox.showinfo("추천 결과", "해당 증상에 맞는 약을 찾을 수 없습니다.")

def keyword_selection():
    keyword_window = tk.Toplevel(root)
    keyword_window.title("증상 선택")
    keyword_window.geometry("700x700")
    
    keyword_frame = ttk.Frame(keyword_window, padding="10", style="TFrame")
    keyword_frame.pack(fill="both", expand=True)
    
    keyword_label = ttk.Label(keyword_frame, text="현재 증상을 선택해주세요:", font=label_font, style="TLabel")
    keyword_label.pack(pady=5)
    
    canvas = tk.Canvas(keyword_frame, bg="white", borderwidth=0)
    scrollbar = ttk.Scrollbar(keyword_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas, style="TFrame")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    button_frame = ttk.Frame(scrollable_frame, style="TFrame")
    button_frame.pack(expand=True)

    row = 0
    col = 0
    max_columns = 1  # Change this value to increase the number of columns

    for symptom in all_symptoms:
        keyword_button = ttk.Button(button_frame, text=symptom, command=lambda s=symptom: recommend_medicine_by_symptom(s), style='Green.TButton')
        keyword_button.grid(row=row, column=col, pady=5, padx=5)

        col += 1
        if col >= max_columns:
            col = 0
            row += 1

def display_all_medicines():
    symptom_dict = defaultdict(list)
    for med in medicine_db:
        for symptom in med.symptoms:
            symptom_dict[symptom].append(med)
    
    info_window = tk.Toplevel(root)
    info_window.title("상비약 정보")
    info_window.geometry("1000x800")
    
    info_frame = ttk.Frame(info_window, padding="10", style="TFrame")
    info_frame.pack(fill="both", expand=True)
    
    search_frame = ttk.Frame(info_frame, padding="10", style="TFrame")
    search_frame.pack(fill="x")
    
    search_label = ttk.Label(search_frame, text="약품 검색:", font=label_font, style="TLabel")
    search_label.pack(side="left")
    
    search_entry = ttk.Entry(search_frame, font=label_font)
    search_entry.pack(side="left", padx=5)
    
    search_button = ttk.Button(search_frame, text="검색", style='Green.TButton', command=lambda: search_medicines(search_entry.get()))
    search_button.pack(side="left", padx=5)
    
    listbox_frame = ttk.Frame(info_frame, style="TFrame")
    listbox_frame.pack(side="left", fill="y")
    
    details_frame = ttk.Frame(info_frame, padding="10", style="TFrame")
    details_frame.pack(side="right", fill="both", expand=True)
    
    def show_medicines(symptom):
        for widget in details_frame.winfo_children():
            widget.destroy()
        
        medicines = symptom_dict[symptom]
        for med in medicines:
            med_button = ttk.Button(details_frame, text=med.name, command=lambda m=med: show_medicine_details(m), style='Green.TButton')
            med_button.pack(pady=5, fill='x')
    
    def show_medicine_details(med):
        for widget in details_frame.winfo_children():
            widget.destroy()
        
        med_name = ttk.Label(details_frame, text=f"약품: {med.name}", font=label_font, foreground="red", style="TLabel")
        med_name.pack(anchor="w", pady=(5, 0))
        
        med_instructions = ttk.Label(details_frame, text=f"복용 방법: {med.instructions}", font=label_font, style="TLabel")
        med_instructions.pack(anchor="w")
        
        med_effects = ttk.Label(details_frame, text=f"효능: {', '.join(med.effects)}", font=label_font, style="TLabel")
        med_effects.pack(anchor="w")
        
        med_side_effects = ttk.Label(details_frame, text=f"부작용: {', '.join(med.side_effects)}", font=label_font, style="TLabel")
        med_side_effects.pack(anchor="w")
        
        med_ingredients = ttk.Label(details_frame, text=f"성분: {', '.join(med.ingredients)}", font=label_font, style="TLabel")
        med_ingredients.pack(anchor="w")
    
    def search_medicines(search_term):
        for widget in details_frame.winfo_children():
            widget.destroy()

        displayed_medicines = set()
        
        for symptom, meds in symptom_dict.items():
            for med in meds:
                if search_term.lower() in med.name.lower() and med.name not in displayed_medicines:
                    displayed_medicines.add(med.name)
                    med_button = ttk.Button(details_frame, text=med.name, command=lambda m=med: show_medicine_details(m), style='Green.TButton')
                    med_button.pack(pady=5, fill='x')
    
    for symptom in symptom_dict:
        symptom_button = ttk.Button(listbox_frame, text=symptom, command=lambda s=symptom: show_medicines(s), style='Green.TButton')
        symptom_button.pack(pady=5, fill='x')

# GUI 설정
root = tk.Tk()
root.title("상비약 추천 프로그램")
root.geometry("400x200")

# 스타일 설정
style = ttk.Style()
style.configure("TFrame", background="white")
style.configure("TLabel", background="white", font=("Helvetica", 12))
style.configure("Green.TButton", background="green", foreground="black", font=("Helvetica", 10, "bold"), padding=10, relief="raised")
style.configure("TButton", background="green", foreground="black", font=("Helvetica", 10, "bold"), padding=10, relief="raised")
style.map("Green.TButton", background=[('active', '#00FF00')], relief=[('active', 'sunken')])

# 폰트 설정
title_font = font.Font(family="Helvetica", size=16, weight="bold")
label_font = font.Font(family="Helvetica", size=12)
button_font = font.Font(family="Helvetica", size=10, weight="bold")

# 메인 프레임
main_frame = ttk.Frame(root, padding="10", style="TFrame")
main_frame.pack(padx=5, pady=5)

# 제목
title_label = ttk.Label(main_frame, text="상비약 추천 프로그램", font=title_font, style="TLabel")
title_label.grid(row=0, column=0, columnspan=2, pady=5)

# 키워드 선택 버튼
keyword_selection_button = ttk.Button(main_frame, text="추천받기", command=keyword_selection, style='Green.TButton')
keyword_selection_button.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

# 상비약 정보 버튼
medicine_info_button = ttk.Button(main_frame, text="상비약 정보", command=display_all_medicines, style='Green.TButton')
medicine_info_button.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

# 상태 표시줄
status_label = ttk.Label(root, text="", anchor="w", style="TLabel")
status_label.pack(side="bottom", fill="x")

# CSV 파일에서 상비약 데이터베이스 로드
try:
    load_medicine_db("medicine_db.csv")
except Exception as e:
    status_label.config(text=f"데이터베이스 로드 실패: {e}")

root.mainloop()
