import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime

class CurrencyConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("مبدل ارز پیشرفته")
        self.root.geometry("500x400")
        
        # تنظیم تم پیش‌فرض (روشن)
        self.dark_mode = False
        self.set_theme()
        
        # دریافت لیست ارزها و نرخ‌ها
        self.currencies, self.rates, self.last_update = self.get_exchange_rates()
        
        # ایجاد عناصر رابط کاربری
        self.create_widgets()
    
    def get_exchange_rates(self):
        try:
            # استفاده از API بانک مرکزی اروپا
            response = requests.get("https://api.exchangeratesapi.io/latest?base=EUR")
            data = response.json()
            
            # استخراج ارزها و نرخ‌ها
            currencies = list(data['rates'].keys())
            currencies.append('EUR')  # اضافه کردن یورو به لیست
            rates = data['rates']
            rates['EUR'] = 1.0  # نرخ یورو به یورو
            
            # تاریخ آخرین بروزرسانی
            last_update = datetime.strptime(data['date'], "%Y-%m-%d").strftime("%Y/%m/%d")
            
            return currencies, rates, last_update
            
        except Exception as e:
            messagebox.showwarning("خطا", "خطا در دریافت نرخ ارز. از نرخ‌های آفلاین استفاده می‌شود.")
            # نرخ‌های آفلاین در صورت عدم اتصال
            currencies = ['EUR', 'USD', 'IRR', 'GBP', 'JPY', 'CAD']
            rates = {
                'EUR': 1.0,
                'USD': 1.18,
                'IRR': 50000,
                'GBP': 0.86,
                'JPY': 130.5,
                'CAD': 1.48
            }
            last_update = "1402/05/15 (آفلاین)"
            return currencies, rates, last_update
    
    def set_theme(self):
        if self.dark_mode:
            # تم تاریک
            self.bg_color = '#2d2d2d'
            self.fg_color = '#ffffff'
            self.entry_bg = '#3d3d3d'
            self.button_bg = '#5d5d5d'
            self.combo_bg = '#4d4d4d'
        else:
            # تم روشن
            self.bg_color = '#f0f0f0'
            self.fg_color = '#000000'
            self.entry_bg = '#ffffff'
            self.button_bg = '#e0e0e0'
            self.combo_bg = '#ffffff'
        
        self.root.config(bg=self.bg_color)
        style = ttk.Style()
        style.configure('TCombobox', fieldbackground=self.combo_bg, background=self.combo_bg)
    
    def create_widgets(self):
        # عنوان برنامه
        title_label = tk.Label(self.root, text="مبدل ارز پیشرفته", 
                             font=('Arial', 16, 'bold'),
                             bg=self.bg_color, fg=self.fg_color)
        title_label.pack(pady=10)
        
        # تاریخ آخرین بروزرسانی
        update_label = tk.Label(self.root, 
                              text=f"آخرین بروزرسانی: {self.last_update}",
                              bg=self.bg_color, fg=self.fg_color)
        update_label.pack()
        
        # فریم برای ورودی مقدار
        amount_frame = tk.Frame(self.root, bg=self.bg_color)
        amount_frame.pack(pady=10)
        
        tk.Label(amount_frame, text="مقدار:", bg=self.bg_color, fg=self.fg_color).pack(side=tk.LEFT)
        self.amount_entry = tk.Entry(amount_frame, bg=self.entry_bg, fg=self.fg_color, width=20)
        self.amount_entry.pack(side=tk.LEFT, padx=5)
        
        # فریم برای انتخاب ارز مبدا و مقصد
        currency_frame = tk.Frame(self.root, bg=self.bg_color)
        currency_frame.pack(pady=10)
        
        tk.Label(currency_frame, text="از ارز:", bg=self.bg_color, fg=self.fg_color).grid(row=0, column=0, padx=5)
        self.from_currency = ttk.Combobox(currency_frame, values=self.currencies, state="readonly", width=15)
        self.from_currency.grid(row=0, column=1, padx=5)
        self.from_currency.set('EUR')
        
        tk.Label(currency_frame, text="به ارز:", bg=self.bg_color, fg=self.fg_color).grid(row=1, column=0, padx=5)
        self.to_currency = ttk.Combobox(currency_frame, values=self.currencies, state="readonly", width=15)
        self.to_currency.grid(row=1, column=1, padx=5)
        self.to_currency.set('IRR')
        
        # دکمه تبدیل معکوس
        reverse_button = tk.Button(currency_frame, text="↔ معکوس", 
                                 command=self.reverse_currencies,
                                 bg=self.button_bg, fg=self.fg_color)
        reverse_button.grid(row=0, column=2, rowspan=2, padx=10)
        
        # فریم برای دکمه‌ها
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(pady=15)
        
        # دکمه تبدیل
        convert_button = tk.Button(button_frame, text="تبدیل", 
                                 command=self.convert,
                                 bg=self.button_bg, fg=self.fg_color, width=10)
        convert_button.pack(side=tk.LEFT, padx=10)
        
        # دکمه تغییر تم
        theme_button = tk.Button(button_frame, text="تغییر تم", 
                               command=self.toggle_theme,
                               bg=self.button_bg, fg=self.fg_color, width=10)
        theme_button.pack(side=tk.LEFT, padx=10)
        
        # دکمه بروزرسانی نرخ‌ها
        refresh_button = tk.Button(button_frame, text="بروزرسانی", 
                                 command=self.refresh_rates,
                                 bg=self.button_bg, fg=self.fg_color, width=10)
        refresh_button.pack(side=tk.LEFT, padx=10)
        
        # نمایش نتیجه
        result_frame = tk.Frame(self.root, bg=self.bg_color)
        result_frame.pack(pady=10)
        
        self.result_label = tk.Label(result_frame, text="", 
                                   font=('Arial', 14, 'bold'),
                                   bg=self.bg_color, fg='#0066cc')
        self.result_label.pack()
        
        # نمایش نرخ تبدیل
        self.rate_label = tk.Label(result_frame, text="", 
                                  font=('Arial', 10),
                                  bg=self.bg_color, fg=self.fg_color)
        self.rate_label.pack()
    
    def refresh_rates(self):
        """بروزرسانی نرخ ارزها از API"""
        self.currencies, self.rates, self.last_update = self.get_exchange_rates()
        
        # به روزرسانی Comboboxها
        self.from_currency['values'] = self.currencies
        self.to_currency['values'] = self.currencies
        
        messagebox.showinfo("بروزرسانی", f"نرخ ارزها با موفقیت بروز شد.\nآخرین بروزرسانی: {self.last_update}")
    
    def reverse_currencies(self):
        """تبدیل معکوس ارز مبدا و مقصد"""
        from_curr = self.from_currency.get()
        to_curr = self.to_currency.get()
        self.from_currency.set(to_curr)
        self.to_currency.set(from_curr)
    
    def toggle_theme(self):
        """تغییر بین تم تاریک و روشن"""
        self.dark_mode = not self.dark_mode
        self.set_theme()
        
        # به روزرسانی ظاهر تمام ویجت‌ها
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.config(bg=self.bg_color)
                for child in widget.winfo_children():
                    if isinstance(child, (tk.Label, tk.Button)):
                        child.config(bg=self.bg_color, fg=self.fg_color)
                    elif isinstance(child, tk.Entry):
                        child.config(bg=self.entry_bg, fg=self.fg_color)
            elif isinstance(widget, (tk.Label, tk.Button)):
                widget.config(bg=self.bg_color, fg=self.fg_color)
        
        # تغییر رنگ نتیجه
        if self.dark_mode:
            self.result_label.config(fg='#4da6ff')
        else:
            self.result_label.config(fg='#0066cc')
    
    def convert(self):
        try:
            amount = float(self.amount_entry.get())
            from_curr = self.from_currency.get()
            to_curr = self.to_currency.get()
            
            if from_curr == to_curr:
                self.result_label.config(text=f"{amount} {from_curr} = {amount} {to_curr}")
                self.rate_label.config(text=f"نرخ تبدیل: 1 {from_curr} = 1 {to_curr}")
                return
            
            if from_curr not in self.rates or to_curr not in self.rates:
                messagebox.showerror("خطا", "ارز انتخاب شده پشتیبانی نمی‌شود.")
                return
            
            # محاسبه نرخ تبدیل
            if from_curr == 'EUR':
                rate = self.rates[to_curr]
            elif to_curr == 'EUR':
                rate = 1 / self.rates[from_curr]
            else:
                rate = self.rates[to_curr] / self.rates[from_curr]
            
            converted_amount = round(amount * rate, 2)
            
            # نمایش نتیجه با فرمت زیبا
            self.result_label.config(text=f"{amount:,.2f} {from_curr} = {converted_amount:,.2f} {to_curr}")
            self.rate_label.config(text=f"نرخ تبدیل: 1 {from_curr} = {rate:,.6f} {to_curr}")
            
        except ValueError:
            messagebox.showerror("خطا", "لطفا یک عدد معتبر وارد کنید.")
            self.result_label.config(text="")
            self.rate_label.config(text="")
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در تبدیل ارز: {str(e)}")
            self.result_label.config(text="")
            self.rate_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverter(root)
    root.mainloop()