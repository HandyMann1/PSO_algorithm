import math
import tkinter as tk
from math import inf
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import main

swarm = None
current_best_eval = math.inf


def particles_creation():
    global swarm
    try:
        population = int(particles_count_spinbox.get())
        v_max = v_max_entry.get()
        lower_bound = min_pos_entry.get()
        upper_bound = max_pos_entry.get()
        swarm = main.generate_swarm(population, v_max, lower_bound, upper_bound)
        update_plot(swarm)

        iterations_counter_text.config(state=tk.NORMAL)
        iterations_counter_text.delete(1.0, tk.END)
        iterations_counter_text.insert(1.0, "0")
        iterations_counter_text.config(state=tk.DISABLED)
    except ValueError as e:
        print(f"Invalid input for particle creation: {e}")
        tk.messagebox.showerror("Input Error", "Введите подходящие значения.")


def particles_calculation():
    global swarm
    try:
        personal_coef = float(personal_coef_entry.get())
        social_coef = float(social_coef_entry.get())
        iteration_number = int(iteration_number_spinbox.get())
        v_max = float(v_max_entry.get())
        lower_bound = float(min_pos_entry.get())
        upper_bound = float(max_pos_entry.get())
        inertia = float(current_speed_entry.get())

        new_generation_counter_num = str(int(iterations_counter_text.get(1.0, tk.END)) + int(iteration_number))
        iterations_counter_text.config(state=tk.NORMAL)
        iterations_counter_text.delete(1.0, tk.END)
        iterations_counter_text.insert(1.0, new_generation_counter_num)
        iterations_counter_text.config(state=tk.DISABLED)

        swarm = main.PSO(swarm, iteration_number, personal_coef, social_coef, v_max, lower_bound, upper_bound, inertia,
                         modification_type.get(), int(iterations_counter_text.get(1.0, tk.END)))

        best_genes_formatted = (f'x[1]: {swarm.best_pos[0]}\n'
                                f'x[2]: {swarm.best_pos[1]}')
        best_solution_text.config(state=tk.NORMAL)
        best_solution_text.delete(1.0, tk.END)
        best_solution_text.insert("1.0", best_genes_formatted)
        best_solution_text.config(state=tk.DISABLED)

        best_min_value_text.config(state=tk.NORMAL)
        best_min_value_text.delete(1.0, tk.END)
        best_min_value_text.insert("1.0", 12.0 + swarm.best_solution)
        best_min_value_text.config(state=tk.DISABLED)

        update_plot(swarm)

    except ValueError as e:
        print(f"Invalid input for particles calculation: {e}")
        tk.messagebox.showerror("Input Error", "Введите подходящие значения.")


root = tk.Tk()
root.geometry("1600x900")

modification_type = tk.StringVar()

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=5)
root.rowconfigure(0, weight=1)

# create frames
left_frame = tk.Frame(root, borderwidth=2, relief="groove")
left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

parameters_frame = tk.Frame(left_frame, borderwidth=2, relief="groove")
parameters_frame.pack(pady=5, padx=5, fill='both', expand=True)

control_frame = tk.Frame(left_frame, borderwidth=2, relief="groove")
control_frame.pack(pady=5, padx=5, fill='both', expand=True)

results_frame = tk.Frame(left_frame, borderwidth=2, relief="groove")
results_frame.pack(pady=5, padx=5, fill='both', expand=True)


def create_label_entry(frame, label_text, default_value):
    row = frame.grid_size()[1]
    label = tk.Label(frame, text=label_text, font=("Helvetica", 12))
    label.grid(row=row, column=0, sticky="e")
    entry_var = tk.DoubleVar(frame)
    entry_var.set(default_value)
    entry = tk.Entry(frame, textvariable=entry_var)
    entry.grid(row=row, column=1)
    return entry_var


# parameters frame
func_name_lbl = tk.Label(parameters_frame,
                         text="Функция: -12x[2] + 4x[1]^2 + 4x[2]^2 -4x[1]x[2]",
                         font=("Helvetica", 12))
func_name_lbl.grid(row=0, columnspan=2)

current_speed_entry = create_label_entry(parameters_frame, "Коэффициент собственной скорости: ", 0.3)
particles_count_lbl = tk.Label(parameters_frame, text="Количество частиц: ", font=("Helvetica", 12))
particles_count_lbl.grid(row=3, column=0)
particles_default_value = tk.IntVar()
particles_default_value.set(50)
particles_count_spinbox = tk.Spinbox(parameters_frame, from_=1,
                                     to=inf,
                                     increment=1,
                                     textvariable=particles_default_value)
particles_count_spinbox.grid(row=3, column=1)
max_pos_entry = create_label_entry(parameters_frame, "Максимальное значение переменной: ", 10)
min_pos_entry = create_label_entry(parameters_frame, "Минимальное значение переменной: ", -10)
personal_coef_entry = create_label_entry(parameters_frame, "Коэфф. собственного лучшего значения: ", 0.5)
social_coef_entry = create_label_entry(parameters_frame, "Коэфф. глобального лучшего значения: ", 0.3)
v_max_entry = create_label_entry(parameters_frame, "Максимальная скорость: ", 15)

# control frame
particles_creation_btn = tk.Button(control_frame, text="Создать частицы", command=lambda: particles_creation())
particles_creation_btn.grid(row=0, columnspan=2, pady=5)
iteration_number_lbl = tk.Label(control_frame, text="Количество итераций: ")
iteration_number_lbl.grid(row=1, column=0)

default_value_spinbox = tk.IntVar(control_frame)
default_value_spinbox.set(100)
iteration_number_spinbox = tk.Spinbox(control_frame,
                                      from_=1,
                                      to=inf,
                                      increment=1,
                                      textvariable=default_value_spinbox)
iteration_number_spinbox.grid(row=1, column=1)

iterations_counter_lbl = tk.Label(control_frame,
                                  text="Количество пройденных итераций: ")
iterations_counter_lbl.grid(row=2, column=0)

iterations_counter_text = tk.Text(control_frame,
                                  height=1,
                                  width=30)

iterations_counter_text.grid(row=2, column=1)
iterations_counter_text.insert("1.0", "0")
iterations_counter_text.config(state=tk.DISABLED)

calculate_particles_btn = tk.Button(control_frame, text="Рассчитать",
                                    command=lambda: particles_calculation())
calculate_particles_btn.grid(row=3, columnspan=2, pady=5)

# results frame
best_solution_lbl = tk.Label(results_frame,
                             text="Лучшее решение: ",
                             font=("Helvetica", 12))
best_solution_lbl.grid(row=0, columnspan=2)

best_solution_text = tk.Text(results_frame,
                             height=10,
                             width=50)
best_solution_text.grid(row=1, columnspan=2)
best_solution_text.config(state=tk.DISABLED)

best_min_value_lbl = tk.Label(results_frame,
                              text="Значение функции: ",
                              font=("Helvetica", 12))
best_min_value_lbl.grid(row=2, columnspan=2)

best_min_value_text = tk.Text(results_frame,
                              height=1,
                              width=30)
best_min_value_text.grid(row=3, columnspan=2)
best_min_value_text.config(state=tk.DISABLED)

# spreadsheet
graph_frame = tk.Frame(root, borderwidth=2, relief="groove")
graph_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
figure = Figure(figsize=(6, 4), dpi=100)
ax = figure.add_subplot(111)

ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_title("Координаты частиц роя")
ax.set_xlabel("X")
ax.set_ylabel("Y")

canvas = FigureCanvasTkAgg(figure, master=graph_frame)
canvas.draw()
canvas.get_tk_widget().pack(fill="both", expand=True)


def update_plot(swarm_func):
    for widget in graph_frame.winfo_children():
        widget.destroy()

    x_data = [particle.pos[0] for particle in swarm_func.particles]
    y_data = [particle.pos[1] for particle in swarm_func.particles]
    x_v = [particle.velocity[0] for particle in swarm_func.particles]
    y_v = [particle.velocity[1] for particle in swarm_func.particles]
    figure = Figure(figsize=(6, 4), dpi=100)
    ax = figure.add_subplot(111)

    lower_bound = float(min_pos_entry.get())
    upper_bound = float(max_pos_entry.get())
    ax.scatter(x_data, y_data, marker='o', color='g')

    for i in range(len(x_data)):
        ax.arrow(x_data[i], y_data[i], x_v[i] * 0.5, y_v[i] * 0.5,
                 head_width=0.2, head_length=0.3, width=0.01,
                 length_includes_head=True, color='k')

    ax.set_xlim(lower_bound, upper_bound)
    ax.set_ylim(lower_bound, upper_bound)
    ax.set_title("Координаты частиц роя")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    canvas = FigureCanvasTkAgg(figure, master=graph_frame)
    canvas.draw()

    canvas.get_tk_widget().pack(fill="both", expand=True)


def confirm_selection():
    modification_type.get()
    if modification_type.get() == 0:
        modification = "Обычный роевой алгоритм"
    else:
        modification = "Роевой алгоритм с модификацией сжатия"
    print(f"Выбранный тип модификации: {modification}")
    selection_window.destroy()


def open_selection_window():
    global selection_window
    selection_window = tk.Toplevel(root)
    selection_window.title("Выбрать тип модификации")

    global modification_type

    modification_label = tk.Label(selection_window, text="Выберите тип модификации скорости:")
    modification_label.pack(pady=10)

    basic_modification_radio = ttk.Radiobutton(selection_window, text="Обычный роевой алгоритм",
                                               variable=modification_type,
                                               value=False)
    cf_modification_radio = ttk.Radiobutton(selection_window, text="Роевой алгоритм с модификацией сжатия",
                                            variable=modification_type,
                                            value=True)
    basic_modification_radio.pack(pady=5)
    cf_modification_radio.pack(pady=5)

    confirm_button = ttk.Button(selection_window, text="Подтвердить", command=confirm_selection)
    confirm_button.pack(pady=20)


open_selection_button = tk.Button(parameters_frame, text="Выбрать тип модификации скорости",
                                  command=open_selection_window)
open_selection_button.grid(row=9, column=0, pady=10, columnspan=2)

root.mainloop()
