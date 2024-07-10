import tkinter.messagebox as msg
from functools import partial
import customtkinter as tk
from HMS.model.entity.doctor import Doctor
from HMS.model.entity.patient import Patient
from HMS.controller.controller import Controller
from HMS.view.component.label_text import TextWithLabel
import HMS.view.patient.register as patient_registration
import HMS.view.patient.search as patient_search
import HMS.view.doctor.register as doctor_registration
import HMS.view.department.register as department_registration
import HMS.view.doctor.info_table as doctors_list
import HMS.view.patient.info_table as patients_list
from HMS.view.patient import patient_info


class Main:
    def __init__(self):
        self.win = tk.CTk()
        self.switch_var = tk.StringVar(value="on")
        self.right_buttons_list = []
        self.role = None
        self.logged_in = None
        self.win.title("HMS")
        self.win.geometry("600x400")
        tk.set_appearance_mode("dark")
        font_tuple = ("Vazir", 30,)
        tk.CTkLabel(self.win, text="ورود کاربر", font=font_tuple, fg_color="transparent").place(x=250, y=30)
        font_tuple = ("Vazir", 15,)
        self.login_user = TextWithLabel(self.win, text=": نام کاربری 👤", font_conf=font_tuple, x=320, y=90,
                                        distance=140, label_width=100, entry_width=130)
        self.login_pass = TextWithLabel(self.win, text=": کلمه عبور 🔐", x=320, y=125, font_conf=font_tuple,
                                        distance=140, label_width=100, entry_width=130, show='*')
        font_tuple = ("Vazir", 12,)
        tk.CTkButton(self.win, text="ورود", width=235, font=font_tuple, command=self.login).place(x=180, y=165)
        tk.CTkButton(self.win, text="فراموشی رمز عبور", font=font_tuple, width=235, command=self.login).place(x=180,
                                                                                                              y=195)
        tk.CTkButton(self.win, text="ثبت نام", width=235, font=font_tuple, command=self.login).place(x=180, y=225)

        self.win.mainloop()

    def login(self):
        username = self.login_user.text
        password = self.login_pass.text
        status, self.logged_in = Controller.login_check(username, password)
        if status:
            self.win.destroy()
            self.win = tk.CTk()
            self.win.title("HMS")
            w, h = self.win.winfo_screenwidth(), self.win.winfo_screenheight()
            self.win.geometry("%dx%d+0+0" % (w, h))
            self.raw()

            if self.logged_in.role == "Admin":
                self.admin_view()
            elif self.logged_in == "Doctor":
                pass
            elif self.logged_in == "Patient":
                pass
            self.win.mainloop()
        else:
            msg.showerror("Error", self.logged_in)

    def switch_event(self):
        if self.switch_var.get() == "off":
            tk.set_appearance_mode("light")
        else:
            tk.set_appearance_mode("dark")

    def logout(self):
        self.win.destroy()
        print("logged out")

    def raw(self):
        to_per = {"Admin": "مدیریت"}
        w, h = self.win.winfo_screenwidth(), self.win.winfo_screenheight()
        font_tuple = ("B Titr", 20,)

        tk.CTkLabel(self.win, text=f"سیستم مدیریت بیمارستان\n پنل {to_per[self.logged_in.role]}", bg_color="#374A69",
                    text_color="#E1F9FF", font=font_tuple, width=w, height=75).place(x=0, y=0)

        tk.CTkButton(self.win, text="خروج", font=font_tuple, bg_color="#374A69", command=self.win.destroy).place(x=20,
                                                                                                                 y=8)
        font_tuple = ("Sahel", 12,)
        switch = tk.CTkSwitch(self.win, text="حالت تیره🌓", command=self.switch_event, bg_color="#374A69",
                              font=font_tuple, variable=self.switch_var, onvalue="on", offvalue="off")
        switch.place(x=35, y=51)
        tk.CTkLabel(self.win, text="", bg_color="#C6CDDF", font=font_tuple, width=250, height=h).place(x=w - 250, y=75)
        self.right_panel()

    def on_button_click(self, button):
        list_ = ["پنل اصلی💢", "بیماران🦽", "پزشکان🩺", "🛌اتاق ها", "شیفت ها⏳",
                 "نوبت دهی 📆", "خدمات🧾", "دپارتمان ها🏢", "پرداخت ها💲"]
        w, h = self.win.winfo_screenwidth(), self.win.winfo_screenheight()
        for but in self.right_buttons_list:
            but.destroy()
            self.right_buttons_list = []

        match button:
            case "پنل اصلی💢":
                new_ = []
                self.clear_sc()
                self.admin_view()
            case "بیماران🦽":
                new_ = ["اضافه کردن بیمار➕", "لیست بیماران🗂", "ویرایش بیمار✏️", "جزئیات بیمار🔍"]
            case "پزشکان🩺":
                new_ = ["اضافه کردن پزشک➕", "لیست پزشکان🗂", "ویرایش دکتر✏️", "جزئیات دکتر🔍"]
            case "دپارتمان ها🏢":
                new_ = ["اضافه کردن دپارتمان➕", "لیست دپارتمان ها🗂", "ویرایش دپارتمان✏️", "جزئیات دپارتمان🔍"]
            case "خدمات🧾":
                new_ = ["اضافه کردن سرویس➕", "لیست سرویس ها🗂", "ویرایش سرویس✏️"]
            case _:
                new_ = []

        font_tuple = ("Sahel", 15,)
        y = 85
        for i in list_:
            rm1 = tk.CTkButton(self.win, text=i, width=220, font=font_tuple, fg_color="#248DB6",
                               hover_color="#0F6BAE", bg_color="#C6CDDF", hover=True,
                               command=partial(self.on_button_click, i))
            rm1.place(x=w - 236, y=y)
            self.right_buttons_list.append(rm1)
            if i == button:
                for new in new_:
                    y += 40
                    rm1 = tk.CTkButton(self.win, text=new, width=200, font=font_tuple, fg_color="#248BD6",
                                       hover_color="#83B8FF", bg_color="#C6CDDF", hover=True,
                                       command=partial(self.on_button_click2, new))
                    rm1.place(x=w - 218, y=y)
                    self.right_buttons_list.append(rm1)
            y += 40

    def on_button_click2(self, button):
        self.clear_sc()
        match button:
            case "اضافه کردن بیمار➕":
                patient_registration.registration(self)
            case "ویرایش بیمار✏️":
                patient_registration.registration(self)
            case "جزئیات بیمار🔍":
                patient_search.search_patient(self)
            case "اضافه کردن پزشک➕":
                doctor_registration.registration(self)
            case "اضافه کردن دپارتمان➕":
                department_registration.registration(self)
            case "لیست پزشکان🗂":
                doctors_list.view(self)
            case "لیست بیماران🗂":
                patients_list.view(self)

            case _:
                new_ = []
                print(new_)

    def search_patient(self):
        status, p_list = Controller.search_by_patient(self.name.text, self.family.text, self.user.text, self.phone.text,
                                                      self.gender.text, self.blood_type.text, self.birthday.text)

        print(status,p_list)
        if len(p_list) == 1:
            patient_info.PatientInfo.show(self,p_list[0])
        elif len(p_list)>1:
            patient_info.PatientInfo.show_menu(self,p_list)
        else:
            msg.showinfo("info","بیماری با این مشخصات یافت نشد")


    def right_panel(self):
        w, h = self.win.winfo_screenwidth(), self.win.winfo_screenheight()
        font_tuple = ("Sahel", 15,)
        list_ = ["پنل اصلی💢", "بیماران🦽", "پزشکان🩺", "اتاق ها🛌", "شیفت ها⏳", "نوبت دهی 📆", "خدمات🧾", "دپارتمان ها🏢",
                 "پرداخت ها💲"]

        y = 85
        for it in list_:
            rm1 = tk.CTkButton(self.win, text=it, width=220, font=font_tuple, fg_color="#248DB6",
                               hover_color="#0F6BAE", bg_color="#C6CDDF", hover=True,
                               command=partial(self.on_button_click, it))
            rm1.place(x=w - 236, y=y)
            self.right_buttons_list.append(rm1)
            y += 40

    def admin_view(self):
        status, doctors = Controller.find_all(Doctor)
        if status:
            doctors = len(doctors)
            doctors = f"پزشکان⚕️\n{doctors}"
        status, patients = Controller.find_all(Patient)
        if status:
            patients = len(patients)
            patients = f"بیماران🦽\n{patients}"

        _list = [doctors, patients, doctors, patients]

        font_tuple = ("B Titr", 20,)
        x = 20
        for i in _list:
            label = tk.CTkLabel(self.win, text=i, width=300, height=100, font=font_tuple, fg_color="#0F6BAE",
                                text_color="#D9E9FF", corner_radius=10)
            label.place(x=x, y=90)
            x += 315

    def add_admin(self):
        status, admin = Controller.add_person(self.name.text, self.family.text, self.user.text, self.password.text,
                                              self.passwrod2.text, self.birthday.text, "Admin", self.phone.text,
                                              self.email.text, self.address.text)

        if status:
            msg.showinfo("Info", "Admin Registered successfully")
        else:
            msg.showerror("Error", f"Admin Registered failed because of {admin} error")

        self.clear_sc()

    def add_patient(self):
        status, patient = Controller.add_patient(self.name.text, self.family.text, self.user.text, self.password.text,
                                                 self.password2.text, self.birthday.text, "Patient", self.phone.text,
                                                 self.email.text, self.address.text, self.gender.text,
                                                 self.blood_type.text)

        if status:
            msg.showinfo("Info", "Patient Registered successfully")
        else:
            msg.showerror("Error", f"Patient Registered failed because of {patient} error")

        self.clear_sc()

    def add_doctor(self):
        status, doctor = Controller.add_doctor(self.name.text, self.family.text, self.user.text, self.password.text,
                                               self.password2.text, self.birthday.text, "Doctor", self.phone.text,
                                               self.email.text, self.address.text, self.specialty.text,
                                               self.department.text,
                                               self.sub_specialty.text, self.experience.text)

        if status:
            msg.showinfo("Info", "Doctor Registered successfully")
        else:
            msg.showerror("Error", f"Doctor Registered failed because of {doctor} error")
        self.clear_sc()

    def add_department(self):
        status, department = Controller.add_department(self.name.text, self.head_id.text)
        if status:
            msg.showinfo("Info", "Department Registered successfully")
        else:
            msg.showerror("Error", f"Department Registered failed because of {department} error")

        self.clear_sc()

    def clear_sc(self):
        for child in self.win.winfo_children():
            child.destroy()
        self.raw()

        if self.logged_in.role == "Admin":
            self.admin_view()
        elif self.logged_in == "Doctor":
            pass
        elif self.logged_in == "Patient":
            pass
