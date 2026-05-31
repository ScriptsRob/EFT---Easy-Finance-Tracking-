# --- modules ---
import customtkinter as ctk
from PIL import Image 
import os, sys
import json as js
import currency_converter as c
import yfinance as yf
def resource_path(relative_path):

    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- screen ---
screen = ctk.CTk()
screen.geometry("1000x600")
screen.title('Easy Finance Tracking')
screen.resizable(0,0)

# --- images ---
safe_img = ctk.CTkImage(
    light_image=Image.open(resource_path("assets/safe.png")),
    size=(200, 200)
)
# --- Variables ---
COLOR_TXT = "#FFFFFF"

MONEY_FILE = 'money.json'
LOGS_FILE = 'logs.json'
SEETING_FILE = 'setting.json'

logs_path = ('D:/prom_project/logs.json')
money_path= ("D:/prom_project/money.json")

font_for_guis = ('Times News Roman',26,'bold')
font_for_text = ('Times News Roman',16,'bold')

system_currency = 'USD'
currencies = [
    "USD",
    "EUR",
    "GBP",
    "CAD",
    "AUD",
    "CHF",
    "JPY",
    "CNY",
    "PLN",
    "CZK",
    "HUF",
    "TRY",
    "ILS",
    "SGD",
    "NZD"
]


themes= ['Dark','Light','System']
state = 'bank'
btn_state= '+'
confirm_state = None
convertor = c.CurrencyConverter()
# --- functions ---
def change_sys_currency(v):
    global system_curreny, money_value
    new_currency = system_currency_option.get()

    converted_money_value = convertor.convert(money_value, system_curreny, new_currency)
    money_value = round(converted_money_value, 2)
    system_curreny = new_currency
    bank_text_label.configure(text=f"{money_value} {system_curreny}")

    with open(SEETING_FILE, "w", encoding="utf-8") as file:
        js.dump({'theme': theme_option.get() , 'currency': new_currency},file, indent=4)
    with open(MONEY_FILE, "w", encoding="utf-8") as file:
        js.dump({"money": money_value}, file, indent=4)
        

def search_for_news():
    news_textbox.delete("0.0", "end")
    ticker = news_search_entry.get().strip().upper()

    if not ticker:
        main_page_news()
        return
    try:
        stock = yf.Ticker(ticker)
        news_item = stock.news
        display_news_list(news_item)
        
    except Exception as e:
        news_textbox.insert("end", f"Error searching ticker '{ticker}': {str(e)}",'red')
def display_news_list(news_items):
    if not news_items:
        news_textbox.tag_config("red", foreground="red")
        news_textbox.insert("end", "No news items were found at this moment!",'red')
        return
            
    for i, item in enumerate(news_items):
        try:

            content = item.get('content', item)
            title = content.get('title', 'No Title Available')
            publisher = content.get('provider', content.get('publisher', 'Unknown Source'))
            news_textbox.insert("end", f" {i+1}) {title}\n\n")
            news_textbox.insert("end", f"(Source: {publisher})\n")
            news_textbox.insert("end", " "*50 + "\n\n")
        except KeyError:
            pass
def change_theme(v):
    try:
        THEME = theme_option.get()
        ctk.set_appearance_mode(THEME)
        with open(SEETING_FILE, "w", encoding="utf-8") as file:
            js.dump({'theme': THEME, 'currency': system_currency},file, indent=4)
            
    except Exception as e:
        print(e)

def main_page_news():
        news_textbox.delete("0.0", "end")
        try:

            main_search = yf.Search("Finance", news_count=10)
            news_items = main_search.news
            display_news_list(news_items)          
        except Exception as e:
            news_textbox.insert("end", f"Error loading main page news: {str(e)}")

def reset_money():
    global money_value
    if money_value != 0:
        os.remove(money_path)
        with open(MONEY_FILE, "w", encoding="utf-8") as file:
            js.dump({"money": 0}, file, indent=4)    
            bank_text_label.configure(text = 0)
            money_value= 0

        bank_textbox.configure(state = 'normal')
        bank_textbox.tag_config("red", foreground="red")
        bank_textbox.insert(1.0,"You've reseted your money balance \n\n", 'red')
        bank_textbox.configure(state = 'disabled')

def show_confirm():
    global confirm_state
    confirm_state = 'yes'
    confirm_frame.place(relx=0.5, y=300, anchor='center')

def close_confirm():
    global confirm_state
    confirm_frame.place_forget()
    confirm_state = None 

def confirm(action,st):
    global confirm_state 
    try:
        if st == 'yes':
            confirm_frame.place_forget()
            action()
            confirm_state = None
        if st == 'No':
            action()
            
    except Exception as e:
        print(e)

def clear_logs():
    if bank_textbox.get('1.0',"end-1c"):
        try :
            bank_textbox.configure(state = 'normal')
            bank_textbox.delete(1.0, 'end')
            bank_textbox.configure(state = 'disabled')
            os.remove(logs_path)
            with open(LOGS_FILE, "w", encoding="utf-8") as file:
                js.dump({}, file, indent=4)
        except FileNotFoundError:
            pass
    
def currency_convert():
    try:
        num = cc_input_1_entry.get()
        converted_value =convertor.convert(num,cc_in_choice.get(),cc_out_choice.get())
        cc_output_label.configure(text=f"{converted_value:.0f}    { cc_out_choice.get()}")
    except ValueError:
        cc_output_label.configure(text= 'Write a number!')

def set_state_and_cash(new_state):
    global btn_state
    btn_state = new_state
    money_cashing()
    
def textbox_insert(entry_log, entry_val):
    bank_textbox.configure(state='normal')
    bank_textbox.insert("1.0", f"{entry_log} :{entry_val} \n\n")
    bank_textbox.configure(state='disabled')


def show_page(game_page):
    global state

    bank_frame.grid_forget()
    curency_frame.grid_forget()
    news_frame.grid_forget()
    settings_frame.grid_forget()
    confirm_frame.place_forget()
    state = game_page

    if state == 'bank':
        bank_frame.grid(row=1, column=0, padx=20, pady=30)
    if state == 'curency':
        curency_frame.grid(row=1, column=0, padx=20, pady=30)
    if state == 'news':
        news_frame.grid(row=1, column=0, padx=20, pady=30)
    if state == 'settings':
        settings_frame.grid(row=1, column=0, padx=20, pady=30)


def money_cashing():
    global money_value
    
    entry_log = bank_money_entry_log.get()
    entry_val = bank_money_entry.get()

    if entry_log and entry_val:
        try:
            money_value += int(entry_val)
                
            bank_text_label.configure(text=f"{money_value} {system_curreny}")
            textbox_insert(entry_log, entry_val)
            bank_money_entry.delete(0, "end")
            bank_money_entry_log.delete(0, "end")

            with open(MONEY_FILE, "w", encoding="utf-8") as file:
                js.dump({'money': money_value}, file, indent=4)

            with open(LOGS_FILE, "r", encoding="utf-8") as file:
                logs = js.load(file)

            logs[entry_log] = entry_val

            with open(LOGS_FILE, "w", encoding="utf-8") as file:
                js.dump(logs, file, indent=4)
        except ValueError:
            pass
        
# --- Json init ---
if not os.path.exists(MONEY_FILE):
    with open(MONEY_FILE, "w", encoding="utf-8") as file:
        js.dump({"money": 0}, file, indent=4)

if not os.path.exists(LOGS_FILE):
    with open(LOGS_FILE, "w", encoding="utf-8") as file:
        js.dump({}, file, indent=4)

with open(MONEY_FILE,"r",encoding="utf-8") as file:
    data = js.load(file)
money_value = data["money"]

if not os.path.exists(SEETING_FILE):
    with open(SEETING_FILE,'w',encoding='utf-8') as file:
        js.dump({'theme': 'dark', 'currency': system_currency},file,indent=4)

with open(SEETING_FILE, "r", encoding="utf-8") as file:
    settings= js.load(file)
system_curreny = settings['currency']
screen._set_appearance_mode(settings['theme'])

# --- frames ---
# --- choose page f rame---
windows_choice_frame = ctk.CTkFrame(screen,
                                    width=960,
                                    height=50,
                                    
)
windows_choice_frame.grid_propagate(False) 

windows_choice_frame.grid(row=0,
                          column=0,
                          padx=20,
                          pady=20,
)


# --- bank frame ---
bank_frame = ctk.CTkFrame(screen,
                          width=960,
                          height =450,
                          corner_radius=30,
                                    
)
bank_frame.grid_propagate(False) 
bank_frame.pack_propagate(False)
bank_frame.grid(row=1,
                column=0,
                padx=20,
                pady=30,
)
# --- curency frame ---
curency_frame = ctk.CTkFrame(screen,
                          width=960,
                          height =450,
                          corner_radius=30,
                                    
)
curency_frame.grid_propagate(False) 
curency_frame.pack_propagate(False)
curency_frame.grid(row=1,
                column=0,
                padx=20,
                pady=30,
)
# --- graph frame ---
news_frame = ctk.CTkFrame(screen,
                          width=960,
                          height =450,
                          corner_radius=30
                                    
)
news_frame.grid_propagate(False) 
news_frame.pack_propagate(False)
news_frame.grid(row=1,
                column=0,
                padx=20,
                pady=30,
)
# --- settings frame ---
settings_frame = ctk.CTkFrame(screen,
                          width=960,
                          height =450,
                          corner_radius=30,
                                    
)
settings_frame.grid_propagate(False) 
settings_frame.pack_propagate(False)
settings_frame.grid(row=1,
                column=0,
                padx=20,
                pady=30,
)
settings_funcs_frame = ctk.CTkFrame(settings_frame,
                          width=400,
                          height =420,
                          corner_radius=25,
                                    
)
settings_funcs_frame.grid_propagate(False) 
settings_funcs_frame.pack_propagate(False)
settings_funcs_frame.place(relx = 0.25,y=225,anchor ='center')

#--- Confirm Frame ---
confirm_frame = ctk.CTkFrame(screen,width=400,height=200,corner_radius=25,bg_color="transparent")
confirm_frame.grid_propagate(False) 
confirm_frame.pack_propagate(False)
confirm_frame.place(relx=0.5, y = 300, anchor = 'center')
confirm_frame.lift()

# --- widjets ---



#Menu 
# --- Home page btn ---
bank_page_btn = ctk.CTkButton(windows_choice_frame,
                              text='Bank',
                              command= lambda: show_page('bank')
)
bank_page_btn.grid(row=0,
                   column=0,
                   padx=40,
                   pady=10
)
# --- Currency Convertor btn ---
converotr_page_btn = ctk.CTkButton(windows_choice_frame,
                              text='Currency convertor',
                              command= lambda: show_page('curency')
)
converotr_page_btn.grid(row=0,
                   column=1,
                   padx=40,
                   pady=10
)
# --- Analysis btn ---
analysis_page_btn = ctk.CTkButton(windows_choice_frame,
                              text='News',
                              command= lambda: show_page('news')
)
analysis_page_btn.grid(row=0,
                   column=2,
                   padx=40,
                   pady=10
)
# --- Settings btn ---
settings_page_btn = ctk.CTkButton(windows_choice_frame,
                              text='Settings',
                              command= lambda: show_page('settings')
)
settings_page_btn.grid(row=0,
                   column=3,
                   padx=120,
                   pady=10
)


# === Bank Widjets ===
bank_label = ctk.CTkLabel(bank_frame,image=safe_img,text='')
bank_label.place(relx=0.5,y = 100,anchor="center" )

bank_text_label = ctk.CTkLabel(bank_frame,text=f"{money_value} {system_curreny}",font=('Arial',40,'bold'),text_color=COLOR_TXT)
bank_text_label.place(relx=0.5,y = 200,anchor="center" )
bank_money_entry_log = ctk.CTkEntry(bank_frame,
                                justify="center",
                                corner_radius=30 ,
                                width= 300,
                                height=50,
                                placeholder_text="Write the way you've got money"
)
bank_money_entry_log.place(relx=0.5,y = 340,anchor="center" )

bank_money_entry = ctk.CTkEntry(bank_frame,
                                justify="center",
                                corner_radius=30,
                                width= 200,
                                height=50,
                                placeholder_text="Write the amount of cash"
)
bank_money_entry.place(relx=0.5,y = 400,anchor="center")

bank_textbox = ctk.CTkTextbox(bank_frame,width = 300,height=435)
bank_textbox.place(relx=0.01,rely = 0.02 )
bank_textbox.configure(state='disabled')

bank_cashin_btn = ctk.CTkButton(bank_frame,width =50,height=50,text='+',font=font_for_guis,command=money_cashing)
bank_cashin_btn.place(relx=0.61,y = 375)

bank_textbox_clear_btn = ctk.CTkButton(bank_frame,text= 'Clear',width= 100, height=20,command= show_confirm )
bank_textbox_clear_btn.place(relx=0.2,y = 400,) 

bank_reset_money_btn = ctk.CTkButton(bank_frame,command=reset_money,text='Reset',width=40,height=40)
bank_reset_money_btn.place(relx=0.6,y = 230,) 
with open(LOGS_FILE, 'r', encoding='utf-8') as file:
    logs = js.load(file)

# --- logs insert ---
bank_textbox.configure(state='normal') 

for k, v in logs.items():
    bank_textbox.insert("1.0", f"{k} :{v} \n\n")

    
bank_textbox.configure(state='disabled')

# === CC widjets ===
cc_input_1_entry = ctk.CTkEntry(curency_frame,width=760,height=100,font=font_for_guis,corner_radius=25,justify='center')
cc_input_1_entry.place(relx=0.5,y = 80,anchor="center")

cc_in_choice = ctk.CTkComboBox(curency_frame,height=50,width=150,justify='center',values= currencies,font=font_for_guis,corner_radius=25)
cc_in_choice.place(relx=0.1,y = 180,anchor="center")

cc_out_choice = ctk.CTkComboBox(curency_frame,height=50,width=150,justify='center',values= currencies,font=font_for_guis,corner_radius=25)
cc_out_choice.place(relx=0.9,y = 180,anchor="center")

cc_convert_btn = ctk.CTkButton(curency_frame,height=50,width=150,corner_radius=25,text='Convert',font=font_for_guis,command=currency_convert)
cc_convert_btn.place(relx=0.5,y = 180,anchor="center")

cc_output_label = ctk.CTkLabel(curency_frame,height=50,width=150,text=' ',font=font_for_guis,)
cc_output_label.place(relx=0.5,y = 300,anchor="center")

# --- Confirm Menu widjets ---
text_label = ctk.CTkLabel(confirm_frame,text='Confirm?',font=font_for_guis)
text_label.place(x= 200,y= 50,anchor="center")

yes_btn = ctk.CTkButton(confirm_frame, text='Yes',font=font_for_guis,command = lambda: confirm(clear_logs,'yes'))
yes_btn.place(x= 120,y= 120,anchor="center")

no_btn = ctk.CTkButton(confirm_frame, text='No',font=font_for_guis,command = lambda: confirm(close_confirm,'No'))
no_btn.place(x= 280,y= 120,anchor="center")

# --- Settings Frame widjets ---
theme_label = ctk.CTkLabel(settings_funcs_frame,font=font_for_guis,text='Theme')
theme_label.place(relx = 0.2,y =10)

theme_option = ctk.CTkOptionMenu(settings_funcs_frame, values=themes,corner_radius=25, font=font_for_text,command=change_theme)
theme_option.place(relx = 0.1,y =50)

system_currency_label = ctk.CTkLabel(settings_funcs_frame,font=font_for_guis,text='Currency')
system_currency_label.place(relx = 0.6,y =10)

system_currency_option = ctk.CTkOptionMenu(settings_funcs_frame, values=currencies,corner_radius=25, font=font_for_text,command=change_sys_currency)
system_currency_option.place(relx = 0.55,y =50)

# --- News Frame widjets ---
news_search_entry = ctk.CTkEntry(news_frame,width=300,height=30,corner_radius=25)
news_search_entry.place(relx= 0.4, rely= 0.08, anchor = 'center')

news_search_btn = ctk.CTkButton(news_frame,width=100,height=30,corner_radius=25,text='Search',command=search_for_news)
news_search_btn.place(relx= 0.65, rely= 0.08, anchor = 'center')

news_textbox = ctk.CTkTextbox(news_frame,width=900,height=350,font=font_for_text)
news_textbox.place(relx= 0.5, rely= 0.55,anchor = 'center')

main_page_news()
# ====================================
bank_text_label.lift()
show_page('bank')

if __name__ == "__main__":
    screen.mainloop()