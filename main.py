import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

#functions for graphics
def principal():
    info = read_information()
    net_info = show_network_information(info)
    subnet_list = subnet_information(info)
    network_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")])
    if network_file:
        content = net_info + subnet_list
        with open(network_file, "w") as f:
            f.write(content)
        messagebox.showinfo("Archivo guardado", f"Archivo guardado en: {network_file}")
    label_show_network_information.config(text=net_info)
    label_show_subnetworks.config(text=subnet_list)

def read_information():
    # Obtener los valores de los campos de entrada
    first_octet = int(entry_octeto_1.get())
    second_octet = int(entry_octeto_2.get())
    third_octet = int(entry_octeto_3.get())
    fourth_octet = int(entry_octeto_4.get())
    network_mask_info = int(entry_mascara.get())
    new_mask_bits = int(entry_submascara.get())
    # Validar los números ingresados
    if 0 <= first_octet <= 255 and 0 <= second_octet <= 255 and 0 <= third_octet <= 255 and 0 <= fourth_octet <= 255 \
            and 0 <= network_mask_info <= 32 and network_mask_info <= new_mask_bits <= 32:
        # Realizar las acciones necesarias con los valores ingresados
        print("Información guardada correctamente.")
        print("Octetos:", first_octet, second_octet, third_octet, fourth_octet)
        print("Máscara:", network_mask_info)
        print("Submáscara:", new_mask_bits)
    else:
        print("Los números ingresados no son válidos.")
        # 1 - first octet, 2 - second octet, 3 - third octet, 4 - fourth octet
        # 5 - network mask number of bits, 6 - new number of bits for mask, 7 - jumps for subnet
    first_octet = bin(first_octet)[2:].zfill(8)
    second_octet = bin(second_octet)[2:].zfill(8)
    third_octet = bin(third_octet)[2:].zfill(8)
    fourth_octet = bin(fourth_octet)[2:].zfill(8)
    sn_jump = subnet_jump(network_mask_info, new_mask_bits)
    return [first_octet, second_octet, third_octet, fourth_octet, network_mask_info, new_mask_bits, sn_jump]

def subnet_jump(network_mask_info, new_mask_bits):
    # 1 - first octet, 2 - second octet, 3 - third octet, 4 - fourth octet
    # 5 - network mask number of bits, 6 - new number of bits for mask, 7 - jumps for subtnet
    bits_add = new_mask_bits - network_mask_info
    if bits_add == 1:
        subnet_jumps = 2 ** 7
    else:
        subnet_jumps = 0
        for i in range(bits_add):
            subnet_jumps += 2 ** (7-i)
    return subnet_jumps

def mask_address(mask_bits):
    network_mask_binary = (mask_bits) * "1" + (32 - mask_bits) * "0"
    octet_first = network_mask_binary[:8]
    octet_second = network_mask_binary[8:16]
    octet_third = network_mask_binary[16:24]
    octet_fourth = network_mask_binary[24:32]
    mask_address_text = f"->Máscara de subred es: {int(octet_first, 2)}.{int(octet_second, 2)}.{int(octet_third, 2)}.{int(octet_fourth, 2)}"
    return mask_address_text
def broadcast_address(address, mask_bits):
    broadcast_binary = address[:mask_bits] + (32 - mask_bits) * "1"
    octet_first = broadcast_binary[:8]
    octet_second = broadcast_binary[8:16]
    octet_third = broadcast_binary[16:24]
    octet_fourth = broadcast_binary[24:32]
    broadcast_address_text = f"->Dirección BROADCAST: {int(octet_first, 2)}.{int(octet_second, 2)}.{int(octet_third, 2)}.{int(octet_fourth, 2)}"
    return broadcast_address_text

def max_host_address(address, mask_bits):
    max_host_binary = address[:mask_bits] + (32 - mask_bits - 1) * "1" + "0"
    octet_first = max_host_binary[:8]
    octet_second = max_host_binary[8:16]
    octet_third = max_host_binary[16:24]
    octet_fourth = max_host_binary[24:32]
    max_host_address_text = f"->Dirección MÁXIMO HOST: {int(octet_first, 2)}.{int(octet_second, 2)}.{int(octet_third, 2)}.{int(octet_fourth, 2)}"
    return max_host_address_text

def min_host_address(address, mask_bits):
    min_host_binary = address[:mask_bits] + (32 - mask_bits - 1) * "0" + "1"
    octet_first = min_host_binary[:8]
    octet_second = min_host_binary[8:16]
    octet_third = min_host_binary[16:24]
    octet_fourth = min_host_binary[24:32]
    min_host_address_text = f"->Dirección MÍNIMO HOST: {int(octet_first, 2)}.{int(octet_second, 2)}.{int(octet_third, 2)}.{int(octet_fourth, 2)}"
    return min_host_address_text

def next_address(network_information):
    # 1 - first octet, 2 - second octet, 3 - third octet, 4 - fourth octet
    # 5 - network mask number of bits, 6 - new number of bits for mask, 7 - jumps for subtnet
    jump = 256 - network_information[6]
    octet_first = network_information[0]
    octet_second = network_information[1]
    octet_third = network_information[2]
    octet_fourth = network_information[3]
    intact_address = network_information[4] // 8
    if intact_address == 1 :
        network_information[1] = sum_binary(octet_second, jump)
    elif intact_address == 2 :
        network_information[2] = sum_binary(octet_third, jump)
    elif intact_address == 3 :
        network_information[3] = sum_binary(octet_fourth, jump)
    return network_information

def sum_binary(bin_1, dec_2):
    dec_1 = int(bin_1, 2)
    sum_dec = dec_1 + dec_2
    sum_bin = bin(sum_dec)[2:].zfill(8)
    return sum_bin

def show_network_information(network_information):
    # 1 - first octet, 2 - second octet, 3 - third octet, 4 - fourth octet
    # 5 - network mask number of bits, 6 - new number of bits for mask, 7 - jumps for subtnet
    # Show information
    net_information = "Se obtuvo la siguiente información de la red:"
    net_address = f"->Dirección de Red: {int(network_information[0], 2)}.{int(network_information[1], 2)}.{int(network_information[2], 2)}.{int(network_information[3], 2)}/{network_information[4]}."
    net_mask = mask_address(network_information[4])
    address = network_information[0] + network_information[1] + network_information[2] + network_information[3]
    net_min_host_address = min_host_address(address, network_information[4])
    net_max_host_address = max_host_address(address, network_information[4])
    net_broadcast_address = broadcast_address(address, network_information[4])
    net_mask_bits = f"->La máscara de red es de {network_information[4]} bits."
    net_host = f"->El número de hosts para la subred es {format((2 ** (32 - network_information[4])) - 2, ',')}."
    net_class = network_classifier(network_information[0])
    text_to_show = "\n" + net_information + "\n" + net_address + "\n" + net_mask + "\n" + net_min_host_address + "\n" + net_max_host_address + "\n" + net_broadcast_address + "\n" + net_mask_bits + "\n" + net_host + "\n" + net_class + "\n"
    return text_to_show

def show_subnetwork_information(network_information, subred_number):
    # 1 - first octet, 2 - second octet, 3 - third octet, 4 - fourth octet
    # 5 - network mask number of bits, 6 - new number of bits for mask, 7 - jumps for subtnet
    # Show information
    net_information = f"Información de la subred {subred_number} :"
    net_address = f"->Dirección de Red: {int(network_information[0], 2)}.{int(network_information[1], 2)}.{int(network_information[2], 2)}.{int(network_information[3], 2)}/{network_information[5]}."
    net_mask = mask_address(network_information[5])
    address = network_information[0] + network_information[1] + network_information[2] + network_information[3]
    net_min_host_address = min_host_address(address, network_information[5])
    net_max_host_address = max_host_address(address, network_information[5])
    net_broadcast_address = broadcast_address(address, network_information[5])
    net_mask_bits = f"->La máscara de red es de {network_information[5]} bits."
    net_host = f"->El número de hosts para la subred es {format((2 ** (32 - network_information[5])) - 2, ',')}."
    net_class = network_classifier(network_information[0])
    text_to_show_subnet = "\n\n" + net_information + "\n" + net_address + "\n" + net_mask + "\n" + net_min_host_address + "\n" + net_max_host_address + "\n" + net_broadcast_address + "\n" + net_mask_bits + "\n" + net_host + "\n" + net_class + "\n\n\n"
    return text_to_show_subnet

def subnet_information(network_information):
    # 1 - first octet, 2 - second octet, 3 - third octet, 4 - fourth octet
    # 5 - network mask number of bits, 6 - new number of bits for mask, 7 - jumps for subtnet
    #network_information = next_address(network_information)
    subnet_jumps = subnet_jump(network_information[4], network_information[5])
    network_information.append(subnet_jumps)
    subnet_number = 256 // (256 - network_information[6])
    total_info = '\n'
    for i in range(subnet_number):
        total_info = total_info + show_subnetwork_information(network_information, i+1)
        network_information = next_address(network_information)
    return total_info

def network_classifier(first_octet):
    first_octet = int(first_octet,2)
    if 0 <= first_octet <= 127:
        return "->La red es de clase A"
    elif 128 <= first_octet <= 191:
        return "->La red es de clase B"
    elif 192 <= first_octet <= 223:
        return "->La red es de clase C"
    elif 224 <= first_octet <= 239:
        return "->La red es de clase D"
    elif 240 <= first_octet <= 255:
        return "->La red es de clase E"

def close_window():
    window.destroy()

# Crear la ventana
window = tk.Tk()
window.title("Interfaz para ingreso de números")
window.geometry("480x300")

# Etiquetas
label_octeto_1 = tk.Label(window, text="Primer octeto de la dirección de red:")
label_octeto_1.grid(row=0, column=0, pady=10, sticky='e')
label_octeto_2 = tk.Label(window, text="Segundo octeto de la dirección de red:")
label_octeto_2.grid(row=1, column=0, pady=10, sticky='e')
label_octeto_3 = tk.Label(window, text="Tercer octeto de la dirección de red:")
label_octeto_3.grid(row=2, column=0, pady=10, sticky='e')
label_octeto_4 = tk.Label(window, text="Cuarto octeto de la dirección de red:")
label_octeto_4.grid(row=3, column=0, pady=10, sticky='e')
label_mascara = tk.Label(window, text="Número de bits de la máscara de red actual:")
label_mascara.grid(row=4, column=0, pady=10, sticky='e')
label_submascara = tk.Label(window, text="Número de bits de la nueva máscara de red:")
label_submascara.grid(row=5, column=0, pady=10, sticky='e')

# Campos de entrada
entry_octeto_1 = tk.Entry(window)
entry_octeto_1.grid(row=0, column=1)
entry_octeto_2 = tk.Entry(window)
entry_octeto_2.grid(row=1, column=1)
entry_octeto_3 = tk.Entry(window)
entry_octeto_3.grid(row=2, column=1)
entry_octeto_4 = tk.Entry(window)
entry_octeto_4.grid(row=3, column=1)
entry_mascara = tk.Entry(window)
entry_mascara.grid(row=4, column=1)
entry_submascara = tk.Entry(window)
entry_submascara.grid(row=5, column=1)

# Configurar el botón para guardar la información
button_guardar = tk.Button(window, text="Guardar", command=principal)
button_guardar.grid(row=6, column=0, columnspan=1, pady=10, sticky='e')

button_close = tk.Button(window, text="Cerrar", command=close_window)
button_close.grid(row=6, column=1, pady=3, columnspan=1)

# Show results
label_show_network_information = tk.Label(window, text="")
label_show_network_information.grid(row=7, columnspan=2)

label_show_subnetworks = tk.Label(window, text="")
label_show_subnetworks.grid(row=8, columnspan=2)

# Ejecutar la ventana principal
window.mainloop()